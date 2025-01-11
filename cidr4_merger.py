import cProfile
from typing import Optional

Node = tuple[int, int, int]


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_node(cidr4: str) -> Node:
    ip, mask_len = cidr4.strip().split("/")
    mask_len = int(mask_len)
    added_ips_number = 0
    a, b, c, d = list(map(int, ip.split(".")))
    ip_value = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    return ip_value, mask_len, added_ips_number


def sort_nodes(nodes: list[Node]) -> list[Node]:
    return sorted(nodes, key=lambda x: (x[1], x[0]))


def data_to_nodes(data: list[str]) -> list[Node]:
    return sort_nodes(map(cidr4_to_node, data))


def get_mask(node: Node) -> int:
    value, mask_len, _ = node
    x = (2**mask_len - 1) << (32 - mask_len)
    mask = value & x
    return mask


def get_parent_mask(node: Node) -> Optional[int]:
    if node[1] == 0:
        return None
    return get_mask((node[0], node[1] - 1, node[2]))


def have_same_parent(a: Node, b: Node) -> bool:
    return a[1] == b[1] and get_parent_mask(a) == get_parent_mask(b)


def merge_nodes(nodes: list[Node]) -> list[Node]:
    pass


def main():
    file = "cidr4.txt"
    required_len = 15

    data = get_data(file)
    nodes = data_to_nodes(data)
    for n in nodes:
        print(n)


if __name__ == "__main__":
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24, 0)
    assert cidr4_to_node("0.0.0.0/32") == (0, 32, 0)

    bin_a = "10011000000000001000010000010000"
    assert len(bin_a) == 32
    value_a = int(bin_a, 2)

    bin_b = "10011100000000000000000000101011"
    assert len(bin_b) == 32
    value_b = int(bin_b, 2)

    bin_c = "10011000000000000000000000000000"
    assert len(bin_c) == 32
    value_c = int(bin_c, 2)

    bin_d = "11111100000000000000000000000000"
    assert len(bin_c) == 32
    value_d = int(bin_d, 2)

    assert get_mask((value_a, 5, 0)) == value_c
    assert get_mask((value_b, 5, 0)) == value_c
    assert get_mask((0, 1, 0)) == 0
    assert get_mask((0, 0, 0)) == 0

    assert get_parent_mask((value_a, 6, 0)) == value_c
    assert get_parent_mask((value_b, 6, 0)) == value_c
    assert get_parent_mask((0, 1, 0)) == 0
    assert get_parent_mask((0, 0, 0)) is None

    assert have_same_parent((value_a, 6, 0), (value_b, 6, 0)) is True
    assert have_same_parent((value_a, 6, 0), (value_b, 5, 0)) is False
    assert have_same_parent((value_a, 6, 0), (value_d, 6, 0)) is False
    assert have_same_parent((value_a, 6, 0), (0, 1, 0)) is False
    assert have_same_parent((value_a, 6, 0), (0, 0, 0)) is False

    assert sort_nodes(
        [
            (401219072, 24, 0),
            (2899902464, 19, 0),
            (400657664, 24, 0),
            (520969728, 23, 0),
        ]
    ) == [
        (2899902464, 19, 0),
        (520969728, 23, 0),
        (400657664, 24, 0),
        (401219072, 24, 0),
    ]

    main()
    # cProfile.run("main()")
