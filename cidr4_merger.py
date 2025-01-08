import ipaddress
from ipaddress import IPv4Address
from typing import List, Tuple


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_binary(cidr4: str) -> Tuple[str, int]:
    ip_str, vlsm = cidr4.strip().split("/")
    vlsm = int(vlsm)
    ipv4 = IPv4Address(ip_str)
    binary_ip = bin(int(ipv4))[2:]
    binary_ip = binary_ip.zfill(32)
    return binary_ip, vlsm


def binary_to_cidr4(binary_ip: str, vlsm: int) -> str:
    int_ip = int(binary_ip, 2)
    ip_str = str(ipaddress.IPv4Address(int_ip))
    return f"{ip_str}/{vlsm}"


def main():
    file = "cidr4.txt"
    data = get_data(file)
    bin_ips = list(map(cidr4_to_binary, data))
    for b in bin_ips[:5]:
        print(b)


if __name__ == "__main__":
    assert cidr4_to_binary("4.78.139.0/24") == ("00000100010011101000101100000000", 24)
    assert binary_to_cidr4("00000100010011101000101100000000", 24) == "4.78.139.0/24"

    main()
