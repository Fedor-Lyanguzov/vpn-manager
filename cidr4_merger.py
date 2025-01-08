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


def reduce_bin_ip(bin_ip: str, vlsm: int) -> Tuple[str, int]:
    if vlsm == 0:
        return bin_ip, vlsm
    new_vlsm = vlsm - 1
    new_bin_ip = bin_ip[:new_vlsm] + "0" * (32 - new_vlsm)
    return new_bin_ip, new_vlsm


def main():
    file = "cidr4.txt"
    data = get_data(file)
    bin_ips = list(map(cidr4_to_binary, data))
    for b in bin_ips[:5]:
        print(b)


if __name__ == "__main__":
    assert cidr4_to_binary("4.78.139.0/24") == ("00000100010011101000101100000000", 24)
    assert binary_to_cidr4("00000100010011101000101100000000", 24) == "4.78.139.0/24"
    assert reduce_bin_ip("00000100010011101000101100000000", 24) == (
        "00000100010011101000101000000000",
        23,
    )
    assert reduce_bin_ip("10000000000000000000000000000000", 1) == (
        "00000000000000000000000000000000",
        0,
    )
    assert reduce_bin_ip("10000000000000000000000000000000", 0) == (
        "10000000000000000000000000000000",
        0,
    )

    main()
