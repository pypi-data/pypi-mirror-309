# `relationalai.std.graphs.Compute`

The `Compute` class serves as a namespace for graph functions.
You do not create `Compute` objects directly.
A `Compute` instance is automatically instantiated when you create a [`Graph`](../Graph/README.md) object.
You access a graph's `Compute` instance via the [`Graph.compute`](../Graph/compute.md) attribute.

```python
class relationalai.std.graphs.Compute(graph: Graph)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `graph` | [`Graph`](../Graph/README.md) | The graph on which the `Compute` namespace is instantiated. |

## Methods
- [`Compute.adamic_adar()`](./adamic_adar.md)
- [`Compute.avg_degree()`](./avg_degree.md)
- [`Compute.avg_indegree()`](./avg_indegree.md)
- [`Compute.avg_outdegree()`](./avg_outdegree.md)
- [`Compute.betweeness_centrality()`](./betweeness_centrality.md)
- [`Compute.common_neighbor()`](./common_neighbor.md)
- [`Compute.cosine_similarity()`](./cosine_similarity.md)
- [`Compute.degree()`](./degree.md)
- [`Compute.degree_centrality()`](./degree_centrality.md)
- [`Compute.eigenvector_centrality()`](./eigenvector_centrality.md)
- [`Compute.indegree()`](./indegree.md)
- [`Compute.is_connected()`](./is_connected.md)
- [`Compute.is_reachable()`](./is_reachable.md)
- [`Compute.is_triangle()`](./is_triangle.md)
- [`Compute.label_propagation()`](./label_propagation.md)
- [`Compute.local_clustering_coefficient()`](./local_clustering_coefficient.md)
- [`Compute.louvain()`](./louvain.md)
- [`Compute.max_degree()`](./max_degree.md)
- [`Compute.max_indegree()`](./max_indegree.md)
- [`Compute.max_outdegree()`](./max_outdegree.md)
- [`Compute.min_degree()`](./min_degree.md)
- [`Compute.min_indegree()`](./min_indegree.md)
- [`Compute.min_outdegree()`](./min_outdegree.md)
- [`Compute.num_edges()`](./num_edges.md)
- [`Compute.num_nodes()`](./num_nodes.md)
- [`Compute.num_triangles()`](./num_triangles.md)
- [`Compute.outdegree()`](./outdegree.md)
- [`Compute.pagerank()`](./pagerank.md)
- [`Compute.preferential_attachment()`](./preferential_attachment.md)
- [`Compute.reachable_from()`](./reachable_from.md)
- [`Compute.triangles()`](./triangles.md)
- [`Compute.weakly_connected_component()`](./weakly_connected_component.md)
- [`Compute.weighted_cosine_similarity()`](./weighted_cosine_similarity.md)
- [`Compute.weighted_degree_centrality()`](./weighted_degree_centrality.md)
- [`Compute.weighted_jaccard_similarity()`](./weighted_jaccard_similarity.md)

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    alice.set(follows=carol)
    bob.set(follows=alice)
    carol.set(follows=alice).set(follows=bob)

# Create a graph and add the `Person.follows` property to the set of edges.
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Compute the PageRank of each person in the graph.
with model.query() as select:
    person = Person()
    # The `pagerank` function is in the `graph.compute` namespace.
    pagerank = graph.compute.pagerank(person)
    response = select(person.name, pagerank)

print(response.results)
# Output:
#     name         v
# 0  Alice  0.397402
# 1    Bob  0.214806
# 2  Carol  0.387792
```
