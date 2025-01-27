```python
def find_subnets(nodes: list[Node]) -> list[tuple[Node, Node]]:
    subnets = []
    for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        parent_node, dip = merge_two_nodes(a, b)
        if parent_node == a or parent_node == b:
            subnets.append((a, b))
    return subnets


def ensure_no_subnets(nodes: list[Node]):
    if subnets := find_subnets(nodes):
        raise Cidr4MergerError(f"There are subnets! {subnets=}")
```


```python
def find_neighbors(nodes: list[Node]) -> list[tuple[Node, Node]]:
    neighbors = []
    for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        parent_node, dip = merge_two_nodes(a, b)
        if parent_node[1] + 1 == a[1] == b[1]:
            neighbors.append((a, b))
    return neighbors


def ensure_no_neighbors(nodes: list[Node]):
    if neighbors := find_neighbors(nodes):
        raise Cidr4MergerError(f"There are neighbors! {neighbors=}")
```
