# pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.std.graphs import Graph
from relationalai.std.aggregates import sum
import rich

#--------------------------------------------------
# Types
#--------------------------------------------------

model = rai.Model("MyCoolDatabase")
model._config.set("compiler.use_multi_valued", True)

Person = model.Type("Person")
Criminal = model.Type("Criminal")
Transaction = model.Type("Transaction")

#--------------------------------------------------
# Load data
#--------------------------------------------------

with model.rule():
    joe = Person.add(name="Joe")
    jane = Person.add(name="Jane")
    bob = Person.add(name="Bob")
    dylan = Person.add(Criminal, name="Dylan")
    dave = Person.add(name="Dave")

    joe.knows.add(jane)
    jane.knows.add(bob)
    bob.knows.extend([joe, dylan])
    dylan.knows.add(joe)

    Transaction.add(from_=joe, to=jane, amount=100)
    Transaction.add(from_=joe, to=jane, amount=1000)
    Transaction.add(from_=joe, to=jane, amount=10)
    Transaction.add(from_=joe, to=bob, amount=10)

#--------------------------------------------------
# Graph
#--------------------------------------------------

graph = Graph(model)
Node, Edge = graph.Node, graph.Edge

Node.extend(Person, label=Person.name)
Node.extend(Criminal, criminal=True)
Edge.extend(Person.knows, label="knows")

with model.rule():
    t = Transaction()
    weight = sum(t, t.amount, per=[t.from_, t.to])
    Edge.add(t.from_, t.to, label="Transfer", weight=weight)

with model.rule():
    n = Node()
    rank = graph.compute.pagerank(n)
    n.set(rank=rank * 5)

#--------------------------------------------------
# Go
#--------------------------------------------------

data = graph.fetch()
rich.print(data)
graph.visualize(three=True, style={
    "node": {
        "color": lambda x: "red" if x.get("criminal") else "blue",
        "size": lambda x: (x.get("rank", 1) * 2) ** 2
    },
    "edge": {
        "color": "yellow",
    }
}).display()