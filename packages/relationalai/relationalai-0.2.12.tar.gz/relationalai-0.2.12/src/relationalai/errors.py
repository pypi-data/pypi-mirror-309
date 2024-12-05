import ast
from collections import defaultdict
import io
import textwrap
from typing import Any, List, Tuple
from .metamodel import Action, Task
from . import debugging
from rich.console import Console

#--------------------------------------------------
# Print helpers
#--------------------------------------------------

def rich_str(string:str, style:str|None = None) -> str:
    output = io.StringIO()
    console = Console(file=output, force_terminal=True)
    console.print(string, style=style)
    return output.getvalue()

def body_text(console, body:str):
    body = textwrap.dedent(body)
    for line in body.splitlines():
        if not line.startswith("  "):
            console.print(line)
        else:
            console.print(line, soft_wrap=True)

def mark_source(source, start_line:int, end_line:int, indent=8, highlight="yellow", highlight_lines = []):
    final_lines = []
    all_lines = source.source.splitlines()
    max_line = source.line + len(all_lines)
    line_number_len = len(str(max_line))
    for ix, line in enumerate(source.source.splitlines()):
        cur = line
        cur_indent = indent if ix > 0 else 0
        line_number = source.line + ix
        color = "dim white"
        if (line_number >= start_line and line_number <= end_line) or line_number in highlight_lines:
            color = highlight + " bold"
        cur = f"{' '*cur_indent}[{color}]  {line_number :>{line_number_len}} |  {cur}[/{color}]"
        final_lines.append(cur)
    return "\n".join(final_lines)

def print_source_error(source, name:str, content:str):
    fixed_content_length = len(name) + len(source.file) + len(str(source.line)) + 2  # 2 for the spaces around the dash
    num_dashes = 74 - fixed_content_length
    dashes = '-' * num_dashes
    console = Console(width=80)
    console.print(f"[red]--- {name} {dashes} {source.file}: {source.line}")
    body_text(console, content)
    console.print()
    console.print(f'[red]{"-" * 80}')
    console.print()

def print_error(name:str, content:str):
    fixed_content_length = len(name) + 2  # 2 for the spaces around the dash
    num_dashes = 76 - fixed_content_length
    dashes = '-' * num_dashes
    console = Console(width=80)
    console.print(f"[red]--- {name} {dashes}")
    body_text(console, content)
    console.print()
    console.print(f'[red]{"-" * 80}')
    console.print()

#--------------------------------------------------
# Transformers
#--------------------------------------------------

class IfToWithTransformer(ast.NodeTransformer):
    def visit_If(self, node):
        with_node = ast.With(
            items=[ast.withitem(context_expr=node.test, ctx=ast.Load(), optional_vars=None)],
            body=node.body,
            lineno=node.lineno,
            type_comment=None)
        return with_node

class WithDynamic(ast.NodeTransformer):
    def visit_With(self, node):
        content = ast.unparse(node.items[0].context_expr).replace(")", "dynamic=True)")
        with_node = ast.With(
            items=[ast.withitem(context_expr=ast.Name(id=content), ctx=ast.Load(), optional_vars=node.items[0].optional_vars)],
            body=[],
            lineno=node.lineno,
            type_comment=None)
        return with_node

class SetToMethod(ast.NodeTransformer):
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Attribute):
            keyword = ast.keyword(arg=node.targets[0].attr, value=node.value)
            return ast.Expr(value=ast.Call(
                func=ast.Attribute(value=node.targets[0].value, attr="set", ctx=ast.Load()),
                args=[],
                keywords=[keyword],
                lineno=node.lineno,
                type_comment=None))
        return node

class AssignToCompare(ast.NodeTransformer):
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Attribute) and len(node.targets) == 1:
            compare_node = ast.Compare(
                left=node.targets[0],
                ops=[ast.Eq()],
                comparators=[node.value]
            )
            expr_node = ast.Expr(value=compare_node)
            ast.copy_location(expr_node, node)
            if hasattr(node, 'type_comment'):
                expr_node.type_comment = node.type_comment

            return expr_node
        return node

#--------------------------------------------------
# Finders
#--------------------------------------------------

class PropertyFinder(ast.NodeVisitor):
    def __init__(self, start_line, properties):
        self.errors = []
        self.start_line = start_line
        self.properties = properties
        self.found_properties_lines = []  # To store lines where properties are found
        self.dynamic_properties = []  # To store dynamic properties

    def to_line_numbers(self, node):
        return (node.lineno, node.end_lineno)

    def visit_Attribute(self, node):
        if node.attr in self.properties:
            line_numbers = self.to_line_numbers(node)
            if line_numbers[0] >= self.start_line:
                self.found_properties_lines.append(node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check if this is a call to 'getattr'
        if (isinstance(node.func, ast.Name) and node.func.id == 'getattr' and
                len(node.args) >= 2):
            if isinstance(node.args[1], ast.Str):
                property_name = node.args[1].s
                if property_name in self.properties:
                    line_numbers = self.to_line_numbers(node)
                    if line_numbers[0] >= self.start_line:
                        self.found_properties_lines.append(node.lineno)
            else:
                line_numbers = self.to_line_numbers(node)
                if line_numbers[0] >= self.start_line:
                    self.dynamic_properties.append(node.lineno)
        self.generic_visit(node)

#--------------------------------------------------
# Exceptions
#--------------------------------------------------

class RAIException(Exception):
    def __init__(self, message:str):
        self.message = message

    def __str__(self):
        return self.message

class RelQueryError(Exception):
    def __init__(self, problems):
        super().__init__("Rel query error")
        self.problems = problems

    def pprint(self):
        body = "\n\n".join(f'{problem["error_code"]}\n{problem["report"]}\n{problem["message"]}'
                           for problem in self.problems)
        return f"Rel query error\n{body}"

#--------------------------------------------------
# Errors
#--------------------------------------------------

class Errors:
    @staticmethod
    def call_source(steps=None):
        if steps is None:
            return debugging.capture_code_info()
        return debugging.capture_code_info(steps + 1)

    #--------------------------------------------------
    # DSL invalid python errors
    #--------------------------------------------------

    @staticmethod
    def invalid_if(task:Task|Action, start_line:int, end_line:int):
        source = debugging.get_source(task)
        if not source:
            return

        marked = mark_source(source, start_line, end_line)
        updated = mark_source(source.modify(IfToWithTransformer()), start_line, end_line, highlight="green")
        dynamic = mark_source(source.modify(WithDynamic()), source.line, end_line, highlight="green")

        content = f"""
        In a RelationalAI query, using an if statement dynamically modifies the structure of the query itself, rather than adding a conditional.

        {marked}

        If you're trying to do an action based on a condition, use a [green]with[/green] statement instead.

        {updated}

        If you are trying to create a dynamic query where parts are conditional, add the [green]dynamic=True[/green] flag to the query like so:

        {dynamic}
        """
        print_source_error(source, "Invalid if", content)

    @staticmethod
    def invalid_loop(task:Task|Action, start_line:int, end_line:int):
        source = debugging.get_source(task)
        if not source:
            return

        marked = mark_source(source, start_line, end_line)
        dynamic = mark_source(source.modify(WithDynamic()), source.line, end_line, highlight="green")

        content = f"""
        In a RelationalAI query, using a loop statement would dynamically modify the query itself, like a macro.

        {marked}

        If that's the goal, you can add the [green]dynamic=True[/green] flag to the query:

        {dynamic}
        """
        print_source_error(source, "Invalid loop", content)

    @staticmethod
    def invalid_try(task:Task|Action, start_line:int, end_line:int):
        source = debugging.get_source(task)
        if not source:
            return

        marked = mark_source(source, start_line, end_line)
        dynamic = mark_source(source.modify(WithDynamic()), source.line, end_line, highlight="green")

        content = f"""
        In a RelationalAI query, using a try statement will have no effect unless a macro-like function is being called and can fail.

        {marked}

        If macro-like behavior is the goal, you can add the [green]dynamic=True[/green] flag to the query:

        {dynamic}
        """
        print_source_error(source, "Invalid try", content)

    @staticmethod
    def set_on_instance(source, name, value):
        marked = mark_source(source, source.line, source.line)
        dynamic = mark_source(source.modify(SetToMethod()), source.line, source.line, highlight="green")
        compare = mark_source(source.modify(AssignToCompare()), source.line, source.line, highlight="green")

        content = f"""
        You can't set properties directly on a RAI object.

        {marked}

        If you are trying to set the value of a property use [green]set()[/green]:

        {dynamic}

        Or maybe you meant [green]==[/green] instead?

        {compare}
        """
        print_source_error(source, "Invalid property set", content)

    @staticmethod
    def invalid_bool(source):
        marked = mark_source(source, source.line, source.line)
        content = f"""
        In a RelationalAI query, the truth values of Producer objects are unknown
        until the query has been evaluated. You may not use Producers in boolean
        expressions, such as those involving [green]if[/green], [green]while[/green], [green]and[/green], [green]or[/green], and [green]not[/green]:

        {marked}

        Producer objects include:

        - [green]Instance[/green] objects, such as [green]person[/green].
        - [green]InstanceProperty[/green] objects, such as [green]person.age[/green].
        - [green]Expresion[/green] objects, such as [green]person.age >= 18[/green].
        """
        print_source_error(source, "Invalid boolean expression with Producer", content)

    #--------------------------------------------------
    # DSL scope errors
    #--------------------------------------------------

    @staticmethod
    def out_of_context(source):
        marked = mark_source(source, source.line, source.line)
        content = f"""
        Looks like this [yellow]object[/yellow] is being used outside of a rule or query.

        {marked}
        """
        print_source_error(source, "Outside of context", content)
        exit()

    @staticmethod
    def variable_out_of_context(source, name:str, is_property=False):
        marked = mark_source(source, source.line, source.line)
        content = f"""
        Looks like a variable representing [yellow bold]{name}[/yellow bold] is being used outside of the rule or query it was defined in.

        {marked}
        """
        print_source_error(source, "Variable out of context", content)
        raise RAIException("Variable out of context") from None


    #--------------------------------------------------
    # DSL reserved errors
    #--------------------------------------------------

    @staticmethod
    def reserved_property(source, property_name:str):
        marked = mark_source(source, source.line, source.line)
        content = f"""
        The property '{property_name}' is a reserved property name on RelationalAI types.

        {marked}
        """
        print_source_error(source, "Reserved property name", content)
        exit()

    #--------------------------------------------------
    # Rel errors
    #--------------------------------------------------

    @staticmethod
    def rel_undefineds(undefineds:List[Tuple[str, Any]]):
        # group by source
        source_map = defaultdict(list)
        for (name, source) in undefineds:
            source_map[source.source].append((source, name))

        for names in source_map.values():
            source = names[0][0]
            props = ", ".join([f"[yellow]{name}[/yellow]" for (_, name) in names])
            prop_line = f"property {props} has" if len(names) == 1 else f"properties {props} have"
            found = PropertyFinder(source.line, [name for (_, name) in names])
            if source.block:
                found.visit(source.block)
            found_lines = found.found_properties_lines or found.dynamic_properties
            marked = mark_source(source, -1, -1, indent=12, highlight_lines=found_lines)
            content = f"""
            The {prop_line} never been set or added to and so will always cause the rule or query to fail.

            {marked}
            """
            print_source_error(source, "Uninitialized property", content)
        raise RAIException("Uninitialized property") from None

    #--------------------------------------------------
    # Snowflake errors
    #--------------------------------------------------

    @staticmethod
    def snowflake_app_missing(app_name):
        content = f"""
        The [yellow]{app_name}[/yellow] app doesn't appear to be installed in this snowflake account.

        If it's installed under a different name, run [green]`rai init`[/green] on the command line and you can set the app name.
        """
        print_error("Couldn't find RelationalAI", content)
        raise RAIException("Couldn't find RelationalAI snowflake application") from None

    @staticmethod
    def snowflake_import_missing(source, import_name:str, model_name:str):
        marked = mark_source(source, source.line, source.line)
        content = f"""
        The Snowflake object [yellow]{import_name}[/yellow] hasn't been imported into RAI.

        {marked}

        You can create an import for it using the rai cli:

          [green]rai imports:stream --source {import_name} --model {model_name}[/green]
        """
        print_source_error(source, "Couldn't find import", content)
        raise RAIException("Couldn't find import") from None

    @staticmethod
    def snowflake_change_tracking_not_enabled(obj:str, sql:str):
        content = f"""
        Change tracking isn't enabled for [yellow]{obj}[/yellow].

        To enable change tracking, you'll need to run the following SQL:

        [green]{sql}[/green]
        """
        print_error("Change tracking not enabled", content)
        raise RAIException("Change tracking not enabled") from None

    #--------------------------------------------------
    # Engine errors
    #--------------------------------------------------

    @staticmethod
    def engine_not_found(name:str, message:str):
        content = f"""
        The engine [yellow]{name}[/yellow] isn't available. You can start the engine with the following command:

        [green]rai engines:create --name {name}[/green]
        """
        print_error("Engine unavailable", content)
        raise RAIException(message) from None