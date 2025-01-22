import cProfile

Node = tuple[int, int, int]


class Cidr4MergerError(Exception):
    pass


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_node(cidr4: str) -> Node:
    ip_address, mask_len = cidr4.strip().split("/")
    mask_len = int(mask_len)
    a, b, c, d = list(map(int, ip_address.split(".")))
    ip = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    added_ips_number = 0
    return ip, mask_len, added_ips_number


def sort_nodes(nodes: list[Node]) -> list[Node]:
    return sorted(nodes)


def get_net_addr(ip: int, mask_len: int) -> int:
    mask = ((1 << mask_len) - 1) << (32 - mask_len)
    net_addr = ip & mask
    return net_addr


def get_parent_ip(ip: int, mask_len: int) -> int:
    if mask_len == 0:
        raise Cidr4MergerError("The top of the tree has no parent!")
    return get_net_addr(ip, mask_len - 1)


def make_parent(a: Node, b: Node) -> Node:
    ip, mask_len, added_ips_number = None
    return ip, mask_len, added_ips_number


def make_cidr4(ip, mask_len) -> str:
    lst = [str(ip >> (i << 3) & 0xFF) for i in reversed(range(4))]
    ip_address = ".".join(lst)
    return f"{ip_address}/{mask_len}"


def merge_nodes(nodes_to_merge: list[Node], required_len: int) -> list[Node]:
    nodes = [x for x in nodes_to_merge]
    # преобразовать список нод в список туплов: родитель (ip, mask len, added ips), d_ip = кол-во добавляемых адресов
    # найти подходящего родителя (с минимальным значением d_ip), затем мержить два узла:
    # 1) если в соседних ветках
    # 2) если один из узлов находится в подсети у другого
    # повторить пока не достигнем нужного кол-ва узлов

    return nodes


def main():
    file = "cidr4.txt"
    required_len = 20

    data = get_data(file)
    nodes = list(map(cidr4_to_node, data))

    nodes = sort_nodes(nodes)
    merged_nodes = merge_nodes(nodes, required_len)

    cidr4s = []
    sum_added_ips = 0
    for ip_value, mask_len, added_ips, _ in merged_nodes:
        cidr4s.append(make_cidr4(ip_value, mask_len))
        sum_added_ips += added_ips

    cidr4s_str = "\n".join(cidr4s)
    print(
        f"Исходный список длины {len(nodes)} сокращен до {len(cidr4s)}\n"
        f"Количество добавленных ip адресов: {sum_added_ips:_}\n"
        f"Список объединенных cidr4:\n"
        f"{cidr4s_str}"
    )


if __name__ == "__main__":
    cProfile.run("main()")
