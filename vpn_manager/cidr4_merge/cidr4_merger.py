import cProfile

from .util import cidr4_to_node, get_data, make_cidr4

Node = tuple[int, int]


class Cidr4MergerError(Exception):
    pass


def find_parent(a: Node, b: Node) -> Node:
    ip_a, mask_len_a = a
    ip_b, mask_len_b = b
    mask_len = min(mask_len_a, mask_len_b)
    mask = ((1 << mask_len) - 1) << (32 - mask_len)
    while ip_a & mask != ip_b & mask:
        mask_len -= 1
        mask = (mask << 1) & ((1 << 32) - 1)
    ip = ip_a & mask
    parent_node = ip, mask_len
    if parent_node == a or parent_node == b:
        raise Cidr4MergerError(
            f"Error! Trying to find common parent of network and subnet! {parent_node=}, {a=}, {b=}."
        )
    return parent_node


def calc_dip(mask_len_a: int, mask_len_b: int, mask_len_p: int) -> int:
    def dip(mla, mlp):
        m = mlp + 1
        res = 1 << (mla - m)
        res -= 1
        res <<= 32 - mla
        return res

    return dip(mask_len_a, mask_len_p) + dip(mask_len_b, mask_len_p)


def merge_two_nodes(node_a: Node, node_b: Node) -> tuple[Node, int]:
    parent_node = find_parent(node_a, node_b)
    dip = calc_dip(node_a[1], node_b[1], parent_node[1])
    return parent_node, dip


def merge_nodes(nodes: list[Node], required_len: int) -> tuple[list[Node], int]:
    sum_dip = 0
    while len(nodes) > required_len:
        min_tuple = None, (None, float("inf"))
        for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
            parent_node, dip = merge_two_nodes(a, b)
            if dip < min_tuple[1][1]:
                min_tuple = i, (parent_node, dip)
        idx, (parent_node, dip) = min_tuple
        nodes = nodes[:idx] + [parent_node] + nodes[idx + 2 :]
        sum_dip += dip

        # for i, (a, b) in enumerate(zip(nodes, nodes[1:])):
        #     parent_node, dip = merge_two_nodes(a, b)
        #     assert parent_node != a
        #     assert parent_node != b

    return nodes, sum_dip


def main():
    required_len = 20
    data = get_data()
    nodes = sorted(map(cidr4_to_node, data))
    merged_nodes, sum_dip = merge_nodes(nodes, required_len)
    cidr4s = [make_cidr4(ip, mask_len) for ip, mask_len in merged_nodes]
    print(sorted(cidr4s), sum_dip, sep="\n")


if __name__ == "__main__":
    cProfile.run("main()")
