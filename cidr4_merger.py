from copy import deepcopy
from ipaddress import IPv4Address
from typing import List, Tuple


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def cidr4_to_binary(cidr4: str) -> str:
    ip_str, vlsm = cidr4.strip().split("/")
    vlsm = int(vlsm)
    ipv4 = IPv4Address(ip_str)
    binary_ip = bin(int(ipv4))[2:]
    binary_ip = binary_ip.zfill(32)
    binary = binary_ip[:vlsm]
    return binary


def binary_to_cidr4(binary: str) -> str:
    vlsm = len(binary)
    binary_ip = binary + "0" * (32 - vlsm)
    int_ip = int(binary_ip, 2)
    ip = IPv4Address(int_ip)
    return f"{ip}/{vlsm}"


def reduce_binary(binary: str) -> str:
    if len(binary) == 0:
        return ""
    new_binary = binary[:-1]
    if "1" not in new_binary:
        return ""
    return new_binary


def rough_merge_binaries(binaries: List[str], req_len: int) -> List[str]:
    ips = set(deepcopy(binaries))
    non_reducible_ips = set()
    reduction_limit_reached = False
    while (
        len(ips) > 0
        and len(ips) + len(non_reducible_ips) > req_len
        and not reduction_limit_reached
    ):
        max_vlsm = len(max(ips, key=lambda x: len(x)))
        reduced_ips = set()
        merged_ips = set()
        for ip in ips:
            if len(ip) == max_vlsm:
                reduced_ip = reduce_binary(ip)
                if len(reduced_ip) > 0:
                    reduced_ips.add(reduced_ip)
                else:
                    non_reducible_ips.add(ip)
            else:
                merged_ips.add(ip)
        merged_ips.update(reduced_ips)
        if len(merged_ips) + len(non_reducible_ips) > req_len:
            ips = merged_ips
        else:
            reduction_limit_reached = True

    ips.update(non_reducible_ips)
    return sorted(ips)


def main():
    file = "cidr4.txt"
    required_len = 20

    data = get_data(file)
    bin_ips = list(map(cidr4_to_binary, data))
    rough_merged_bin_ips = rough_merge_binaries(bin_ips, required_len)
    print(f"{len(rough_merged_bin_ips)=}")
    for ip in rough_merged_bin_ips:
        print(ip)


if __name__ == "__main__":
    assert cidr4_to_binary("4.78.139.0/24") == "000001000100111010001011"
    assert cidr4_to_binary("128.0.0.0/1") == "1"
    assert cidr4_to_binary("0.0.0.0/0") == ""

    assert binary_to_cidr4("000001000100111010001011") == "4.78.139.0/24"
    assert binary_to_cidr4("1") == "128.0.0.0/1"
    assert binary_to_cidr4("") == "0.0.0.0/0"

    assert reduce_binary("000001000100111010001011") == "00000100010011101000101"
    assert reduce_binary("1") == ""
    assert reduce_binary("0") == ""
    assert reduce_binary("") == ""
    assert reduce_binary("0001") == ""
    assert reduce_binary("0000") == ""

    main()
