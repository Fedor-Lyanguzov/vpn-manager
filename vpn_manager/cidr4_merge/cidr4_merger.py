import cProfile

Node = tuple[int, int]


class Cidr4MergerError(Exception):
    pass


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_node(cidr4: str) -> Node:
    ip_address, mask_len = cidr4.strip().split("/")
    a, b, c, d = list(map(int, ip_address.split(".")))
    ip = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    mask_len = int(mask_len)
    return ip, mask_len


def sort_nodes(nodes: list[Node]) -> list[Node]:
    return sorted(nodes)


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


def make_cidr4(ip, mask_len) -> str:
    lst = [str(ip >> (i << 3) & 0xFF) for i in reversed(range(4))]
    ip_address = ".".join(lst)
    return f"{ip_address}/{mask_len}"


def merge_nodes(nodes_to_merge: list[Node], required_len: int) -> list[Node]:
    nodes = [x for x in nodes_to_merge]
    # Преобразовать список нод в список туплов: родитель (ip, mask len), кол-во добавляемых адресов d_ip
    # найти подходящего родителя (с минимальным значением d_ip) и индекс
    # затем мержить два узла:
    # - т.е. удалить элемент с индексом i
    # - еще раз удалить элемент с индексом i
    # - добавить родителя перед элементом с индексом i
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
