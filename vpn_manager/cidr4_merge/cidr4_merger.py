import cProfile

from vpn_manager.cidr4_merge import Cidr4MergerError

from .util import cidr4_to_node, get_data, make_cidr4

Node = tuple[int, int]


class EnsureNoSubnetError(Cidr4MergerError):
    pass


class EnsureNoNeighborsError(Cidr4MergerError):
    pass


def find_subnets(nodes: list[Node]) -> list[tuple[Node, Node]]:
    subnets = []
    for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        parent_node, dip = merge_nodes(a, b)
        if parent_node == a or parent_node == b:
            subnets.append((a, b))
    return subnets


def ensure_no_subnets(nodes: list[Node]):
    if subnets := find_subnets(nodes):
        raise EnsureNoSubnetError(f"There are subnets! {subnets=}")


def find_neighbors(nodes: list[Node]) -> list[tuple[int, Node, Node]]:
    neighbors = []
    for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        parent_node, dip = merge_nodes(a, b)
        if parent_node[1] + 1 == a[1] == b[1]:
            neighbors.append((i, a, b))
    return neighbors


def ensure_no_neighbors(nodes: list[Node]):
    if neighbors := find_neighbors(nodes):
        raise EnsureNoNeighborsError(f"There are neighbors! {neighbors=}")


def merge_nodes(a: Node, b: Node) -> tuple[Node, int]:
    def find_parent(a, b):
        ia, la = a
        ib, lb = b
        min_l = min(la, lb)
        mask = ((1 << min_l) - 1) << (32 - min_l)
        while ia & mask != ib & mask:
            min_l -= 1
            mask = (mask << 1) & ((1 << 32) - 1)
        return ia & mask, min_l

    def calc_dip(l1, lp):
        m = lp + 1
        res = 1 << (l1 - m)
        res -= 1
        res <<= 32 - l1
        return res

    p = find_parent(a, b)
    dip = calc_dip(a[1], p[1]) + calc_dip(b[1], p[1])
    return p, dip


def solution(nodes: list[Node], req_len: int) -> tuple[list[Node], int]:
    sum_dip = 0
    while len(nodes) > req_len:
        min_t = None, None, float("inf")
        for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
            p, dip = merge_nodes(a, b)
            if dip < min_t[2]:
                min_t = i, p, dip
            if dip == 0:
                break
        i, p, dip = min_t
        nodes = nodes[:i] + [p] + nodes[i + 2 :]
        sum_dip += dip

    while nbs := find_neighbors(nodes):
        i, a, b = nbs[0]
        p, dip = merge_nodes(a, b)
        nodes = nodes[:i] + [p] + nodes[i + 2 :]
        sum_dip += dip

    return nodes, sum_dip


def main():
    required_len = 20
    data = get_data()
    nodes = sorted(map(cidr4_to_node, data))
    ensure_no_subnets(nodes)
    ensure_no_neighbors(nodes)
    merged_nodes, sum_dip = solution(nodes, required_len)
    cidr4s = [make_cidr4(ip, mask_len) for ip, mask_len in merged_nodes]
    print(cidr4s, sum_dip, sep="\n")


if __name__ == "__main__":
    cProfile.run("main()")
