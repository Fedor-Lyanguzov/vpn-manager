import cProfile
import math
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
    return list(map(cidr4_to_node, data))


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


def get_group_with_max_mask_len(nodes: list[Node]) -> list[Node]:
    max_mask_len = max(nodes, key=lambda x: x[1])[1]
    return list(filter(lambda x: x[1] == max_mask_len, nodes))


def get_parent(a: Node, b: Node = None) -> Node:
    ip_value = get_parent_mask(a)
    mask_len = a[1] - 1
    added_ips_number = a[2] + 2 ** (32 - a[1])
    if b:
        assert have_same_parent(a, b), "ноды должны быть соседями"
        added_ips_number = a[2] + b[2]
    return ip_value, mask_len, added_ips_number


def reduce_nodes(nodes: list[Node]) -> list[Node]:
    group = get_group_with_max_mask_len(nodes)

    neighbours = []
    loners = []
    i = 0
    while i < len(group) - 1:
        a = group[i]
        b = group[i + 1]
        if have_same_parent(a, b):
            neighbours.append((a, b))
            i += 2
        else:
            loners.append(a)
            i += 1
    if i == len(group) - 1:
        loners.append(group[i])

    if neighbours:
        zipped = zip(neighbours, map(lambda x: get_parent(x[0], x[1]), neighbours))
        min_zipped = min(zipped, key=lambda x: x[1][2])
        (a, b), parent = min_zipped
        nodes.remove(a)
        nodes.remove(b)
        nodes.append(parent)
    elif loners:
        zipped = zip(loners, map(get_parent, loners))
        min_zipped = min(zipped, key=lambda x: x[1][2])
        a, parent = min_zipped
        nodes.remove(a)
        nodes.append(parent)
    else:
        assert False, "Error"

    return sort_nodes(nodes)


def merge_nodes(nodes: list[Node], required_len: int) -> list[Node]:
    while len(nodes) > required_len:
        nodes = reduce_nodes(nodes)
    return nodes


def node_to_cidr4(node: Node) -> str:
    ip_value, mask_len, _ = node
    lst = [str(ip_value >> (i << 3) & 0xFF) for i in reversed(range(4))]
    ip = ".".join(lst)
    return f"{ip}/{mask_len}"


def answer(nodes: list[Node], required_len: int) -> tuple[list[str], int]:
    nodes = sort_nodes(nodes)
    merged_nodes = merge_nodes(nodes, required_len)

    cidr4s = []
    sum_added_ips = 0
    for node in merged_nodes:
        cidr4s.append(node_to_cidr4(node))
        sum_added_ips += node[2]
    return cidr4s, sum_added_ips


def main():
    file = "cidr4.txt"
    required_len = 20

    data = get_data(file)
    nodes = data_to_nodes(data)
    cidr4s, sum_added_ips = answer(nodes, required_len)

    cidr4s_str = "\n".join(cidr4s)
    print(
        f"Исходный список длины {len(nodes)} сокращен до {len(cidr4s)}\n"
        f"Количество добавленных ip адресов: {sum_added_ips:_}\n"
        f"Список объединенных cidr4:\n"
        f"{cidr4s_str}"
    )


if __name__ == "__main__":
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24, 0)
    assert cidr4_to_node("0.0.0.0/32") == (0, 32, 0)

    assert node_to_cidr4((72256256, 24, 0)) == "4.78.139.0/24"
    assert node_to_cidr4((0, 32, 10)) == "0.0.0.0/32"

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

    assert get_group_with_max_mask_len(
        [
            (2899902464, 19, 0),
            (520969728, 23, 0),
            (400657664, 24, 0),
            (401219072, 24, 0),
        ]
    ) == [(400657664, 24, 0), (401219072, 24, 0)]
    assert get_group_with_max_mask_len(
        [
            (401219072, 24, 0),
            (2899902464, 19, 0),
            (520969728, 23, 0),
        ]
    ) == [(401219072, 24, 0)]

    assert get_parent((0, 2, 12), (1073741824, 2, 3)) == (0, 1, 15)
    assert get_parent((2147483648, 2, 1), (3221225472, 2, 2)) == (2147483648, 1, 3)

    assert reduce_nodes(
        [
            (0, 2, 12),
            (1073741824, 2, 3),
        ]
    ) == [
        (0, 1, 15),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12),
            (1073741824, 2, 3),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ]
    ) == [
        (2147483648, 1, 3),
        (0, 2, 12),
        (1073741824, 2, 3),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12),
            (2147483648, 1, 0),
        ]
    ) == [
        (0, 1, 12 + 2**30),
        (2147483648, 1, 0),
    ]

    assert reduce_nodes(
        [
            (0, 1, 12 + 2**30),
            (2147483648, 1, 0),
        ]
    ) == [
        (0, 0, 12 + 2**30),
    ]

    assert merge_nodes(
        [
            (0, 2, 12),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ],
        2,
    ) == [
        (2147483648, 1, 3),
        (0, 2, 12),
    ]

    assert merge_nodes(
        [
            (0, 2, 12),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ],
        1,
    ) == [(0, 0, 15 + 2**30)]

    assert answer(
        [
            (0, 2, 0),
            (2147483648, 2, 0),
            (3221225472, 2, 12),
        ],
        2,
    ) == (["128.0.0.0/1", "0.0.0.0/2"], 12)

    assert answer(
        [
            (0, 2, 0),
            (2147483648, 2, 0),
        ],
        1,
    ) == (["0.0.0.0/0"], 2**31)

    cProfile.run("main()")
