import cProfile

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


def data_to_nodes(data: list[str]) -> list[Node]:
    return sorted(map(cidr4_to_node, data))


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

    main()
    # cProfile.run("main()")
