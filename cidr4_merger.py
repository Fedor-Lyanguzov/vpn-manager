from copy import deepcopy
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
    ip_str = str(IPv4Address(int_ip))
    return f"{ip_str}/{vlsm}"


def reduce_bin_ip(bin_ip: str, vlsm: int) -> Tuple[str, int]:
    if vlsm == 0:
        return "0" * 32, vlsm
    new_vlsm = vlsm - 1
    new_bin_ip = bin_ip[:new_vlsm] + "0" * (32 - new_vlsm)
    if new_bin_ip == "0" * 32:
        return "0" * 32, 0
    return new_bin_ip, new_vlsm


def rough_merge_ips(
    bin_ips: List[Tuple[str, int]], req_len: int
) -> List[Tuple[str, int]]:
    ips = deepcopy(bin_ips)
    reduction_limit_reached = False
    while len(ips) > req_len and not reduction_limit_reached:
        max_vlsm = max(ips, key=lambda x: x[1])[1]
        ips_to_reduce = []
        merged_ips = []
        for ip_vlsm in ips:
            if ip_vlsm[1] == max_vlsm:
                ips_to_reduce.append(ip_vlsm)
            else:
                merged_ips.append(ip_vlsm)
        reduced_ips = map(lambda x: reduce_bin_ip(*x), ips_to_reduce)
        reduced_ips = set(reduced_ips)
        reduced_ips = filter(lambda x: "1" in x[0], reduced_ips)
        merged_ips.extend(list(reduced_ips))
        if len(merged_ips) > req_len:
            ips = merged_ips
        else:
            reduction_limit_reached = True
    return ips


def main():
    file = "cidr4.txt"
    data = get_data(file)
    bin_ips = list(map(cidr4_to_binary, data))
    rough_merged_bin_ips = rough_merge_ips(bin_ips, 20)
    print(f"{len(rough_merged_bin_ips)=}")
    sorted_ips = sorted(rough_merged_bin_ips)
    for ip in sorted_ips:
        print(ip)


if __name__ == "__main__":
    assert cidr4_to_binary("4.78.139.0/24") == ("00000100010011101000101100000000", 24)
    assert binary_to_cidr4("00000100010011101000101100000000", 24) == "4.78.139.0/24"

    assert reduce_bin_ip("00000100010011101000101100000000", 24) == (
        "00000100010011101000101000000000",
        23,
    )
    assert reduce_bin_ip("10000000000000000000000000000000", 1) == ("0" * 32, 0)
    assert reduce_bin_ip("10000000000000000000000000000000", 0) == ("0" * 32, 0)
    assert reduce_bin_ip("0" * 32, 0) == ("0" * 32, 0)

    main()
