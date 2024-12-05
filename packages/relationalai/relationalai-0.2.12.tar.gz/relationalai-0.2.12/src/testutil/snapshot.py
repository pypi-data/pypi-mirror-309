import io
import logging
import os
from pathlib import Path
from typing import Callable

import rich
from rich.syntax import Syntax

from relationalai import debugging
from relationalai.debugging import logger
from relationalai.errors import RelQueryError

def path_to_slug(path: Path, base_path:str|Path):
    return str(path.relative_to(base_path)).replace("/", "__").replace(".py", "")

class QueryTextLogger(logging.Handler):
    def __init__(self):
        super().__init__()
        # compilation events that get 'results' added to them
        self.blocks = []
    
    def emit(self, record):
        d = record.msg
        if isinstance(d, dict):
            if d["event"] == "compilation":
                self.blocks.append({**d})
            elif d["event"] == "time" and d["type"] == "query":
                self.blocks[-1]["results"] = d["results"]

def validate_block_snapshots(
        file_path: Path,
        snapshot,
        get_snapshot_str: Callable, # given a block, return the snapshot string
        snapshot_prefix:str,
        model_kwargs:dict|None = None
    ):
    with open(file_path, "r") as file:
        code = file.read()
        # @TODO: Consider suppressing stdout
        
        # install logger to capture Rel compilation
        query_logger = QueryTextLogger()
        logger.addHandler(query_logger)
        
        exec(code, model_kwargs, None)
        
        logger.removeHandler(query_logger)
        
        block_index = 0
        for block in query_logger.blocks:
            try:
                cmp_string = get_snapshot_str(block)
                if cmp_string is not None:
                    snapshot.assert_match(cmp_string, f"{snapshot_prefix}{block_index}.txt")
                    # only counting blocks that actually assert something
                    block_index += 1
            except RelQueryError as err:
                err.pprint()
                raise err from None
            except AssertionError as err:
                lines = str(err).splitlines()
                if len(lines) < 3:
                    raise
                header, info, _, *body = lines
                with io.StringIO() as buf:
                    console = rich.console.Console(file=buf, force_terminal=True)
                    console.print(header)
                    console.print(info)

                    source_info = debugging.get_source(block["task"])
                    assert source_info and source_info.line is not None
                    source = debugging.find_block_in(code, source_info.line, str(file_path))

                    console.print()
                    base = os.getcwd()
                    console.print("In", f"./{file_path.relative_to(base)}" if file_path.is_relative_to(base) else file_path)
                    if source.source:
                        console.print(Syntax(source.source, "python", dedent=True, line_numbers=True, start_line=source.line, padding=1))

                    console.print('\n'.join(body))
                    raise Exception(buf.getvalue()) from None
