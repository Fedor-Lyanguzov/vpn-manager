import cProfile
from collections import defaultdict
from copy import deepcopy
from ipaddress import IPv4Address
from typing import List, Set, Tuple


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_node(cidr4: str) -> Tuple[int, int, int]:
    ip, mask_len = cidr4.strip().split("/")
    mask_len = int(mask_len)
    added_ips_number = 0
    a, b, c, d = ip.split(".")
    a, b, c, d = int(a), int(b), int(c), int(d)
    ip_value = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    return ip_value, mask_len, added_ips_number


def main():
    file = "cidr4.txt"
    required_len = 15

    data = get_data(file)
    nodes = sorted(map(cidr4_to_node, data))
    for n in nodes:
        print(n)


if __name__ == "__main__":
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24, 0)

    main()
    # cProfile.run("main()")
