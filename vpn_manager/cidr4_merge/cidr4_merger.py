import cProfile

from .util import cidr4_to_node, get_data, make_cidr4

Node = tuple[int, int]


class Cidr4MergerError(Exception):
    pass


def find_parent(a: Node, b: Node) -> Node:
    ia, la = a
    ib, lb = b
    min_l = min(la, lb)
    mask = ((1 << min_l) - 1) << (32 - min_l)
    while ia & mask != ib & mask:
        min_l -= 1
        mask = (mask << 1) & ((1 << 32) - 1)
    return ia & mask, min_l


def calc_dip(la: int, lb: int, lp: int) -> int:
    def dip(l1, lp):
        m = lp + 1
        res = 1 << (l1 - m)
        res -= 1
        res <<= 32 - l1
        return res

    return dip(la, lp) + dip(lb, lp)


def merge_two_nodes(node_a: Node, node_b: Node) -> tuple[Node, int]:
    parent_node = find_parent(node_a, node_b)
    dip = calc_dip(node_a[1], node_b[1], parent_node[1])
    return parent_node, dip


def merge_nodes(nodes: list[Node], required_len: int) -> tuple[list[Node], int]:
    sum_dip = 0
    while len(nodes) > required_len:
        min_tuple = None, None, float("inf")
        for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
            parent_node, dip = merge_two_nodes(a, b)
            if dip < min_tuple[2]:
                min_tuple = i, parent_node, dip
        idx, parent_node, dip = min_tuple
        nodes = nodes[:idx] + [parent_node] + nodes[idx + 2 :]
        sum_dip += dip

    while neighbors := find_neighbors(nodes):
        idx, a, b = neighbors[0]
        parent_node, dip = merge_two_nodes(a, b)
        nodes = nodes[:idx] + [parent_node] + nodes[idx + 2 :]
        sum_dip += dip

    return nodes, sum_dip


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


def find_neighbors(nodes: list[Node]) -> list[tuple[int, Node, Node]]:
    neighbors = []
    for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        parent_node, dip = merge_two_nodes(a, b)
        if parent_node[1] + 1 == a[1] == b[1]:
            neighbors.append((i, a, b))
    return neighbors


def ensure_no_neighbors(nodes: list[Node]):
    if neighbors := find_neighbors(nodes):
        raise Cidr4MergerError(f"There are neighbors! {neighbors=}")


def main():
    required_len = 20
    data = get_data()
    nodes = sorted(map(cidr4_to_node, data))
    ensure_no_subnets(nodes)
    ensure_no_neighbors(nodes)
    merged_nodes, sum_dip = merge_nodes(nodes, required_len)
    cidr4s = [make_cidr4(ip, mask_len) for ip, mask_len in merged_nodes]
    print(cidr4s, sum_dip, sep="\n")


if __name__ == "__main__":
    cProfile.run("main()")
