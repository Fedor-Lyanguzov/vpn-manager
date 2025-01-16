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
    a, b, c, d = list(map(int, ip.split(".")))
    ip_value = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    added_ips_number = 0
    return ip_value, mask_len, added_ips_number


def sort_nodes(nodes: list[Node]) -> list[Node]:
    return sorted(nodes, key=lambda x: (x[1], x[0]))


def get_net_addr(ip: int, mask_len: int) -> int:
    mask = ((1 << mask_len) - 1) << (32 - mask_len)
    net_addr = ip & mask
    return net_addr


def get_parent_mask(ip: int, mask_len: int) -> Optional[int]:
    if mask_len == 0:
        return None
    return get_net_addr(ip, mask_len - 1)


def have_same_parent(ip_a, mask_len_a, ip_b, mask_len_b) -> bool:
    return mask_len_a == mask_len_b and get_parent_mask(
        ip_a, mask_len_a
    ) == get_parent_mask(ip_b, mask_len_b)


def get_group_with_max_mask_len(nodes: list[Node]) -> list[Node]:
    max_mask_len = max(nodes, key=lambda x: x[1])[1]
    return list(filter(lambda x: x[1] == max_mask_len, nodes))


def get_parent(a: Node, b: Optional[Node] = None) -> Node:
    ip_a, mask_len_a, added_ips_number_a = a
    ip = get_parent_mask(ip_a, mask_len_a)
    mask_len = mask_len_a - 1
    added_ips_number = added_ips_number_a + 2 ** (32 - mask_len_a)
    if b:
        ip_b, mask_len_b, added_ips_b = b
        assert have_same_parent(ip_a, mask_len_a, ip_b, mask_len_b)
        added_ips_number = added_ips_number_a + added_ips_b
    return ip, mask_len, added_ips_number


def reduce_nodes(nodes: list[Node]) -> list[Node]:
    group = get_group_with_max_mask_len(nodes)

    neighbours = []
    loners = []
    i = 0
    while i < len(group) - 1:
        a, b = group[i], group[i + 1]
        ip_a, mask_len_a, _ = a
        ip_b, mask_len_b, _ = b
        if have_same_parent(ip_a, mask_len_a, ip_b, mask_len_b):
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


def node_to_cidr4(ip_value, mask_len) -> str:
    lst = [str(ip_value >> (i << 3) & 0xFF) for i in reversed(range(4))]
    ip = ".".join(lst)
    return f"{ip}/{mask_len}"


def answer(nodes: list[Node], required_len: int) -> tuple[list[str], int]:
    nodes = sort_nodes(nodes)
    merged_nodes = merge_nodes(nodes, required_len)

    cidr4s = []
    sum_added_ips = 0
    for ip_value, mask_len, added_ips in merged_nodes:
        cidr4s.append(node_to_cidr4(ip_value, mask_len))
        sum_added_ips += added_ips
    return cidr4s, sum_added_ips


def main():
    file = "cidr4.txt"
    required_len = 20

    data = get_data(file)
    nodes = list(map(cidr4_to_node, data))
    cidr4s, sum_added_ips = answer(nodes, required_len)

    cidr4s_str = "\n".join(cidr4s)
    print(
        f"Исходный список длины {len(nodes)} сокращен до {len(cidr4s)}\n"
        f"Количество добавленных ip адресов: {sum_added_ips:_}\n"
        f"Список объединенных cidr4:\n"
        f"{cidr4s_str}"
    )


if __name__ == "__main__":
    cProfile.run("main()")
