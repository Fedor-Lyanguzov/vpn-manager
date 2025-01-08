from copy import deepcopy
from ipaddress import IPv4Address
from typing import List, Tuple
from itertools import groupby
from collections import defaultdict
import cProfile


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
    binary = binary_ip[:vlsm] + "0" * (32 - vlsm)
    return binary


def binary_to_cidr4(binary: str) -> str:
    vlsm = binary.rfind("1") + 1 if "1" in binary else 0
    int_ip = int(binary, 2)
    ip = IPv4Address(int_ip)
    return f"{ip}/{vlsm}"


def reduce_binary(binary: str) -> str:
    assert len(binary) == 32
    vlsm = binary.rfind("1")
    if vlsm == -1:
        return binary
    return binary[:vlsm] + "0" + binary[vlsm + 1 :]


def get_mask(binary: str) -> str:
    i = binary.rfind("1")
    return binary[: i + 1]


def rough_merge_binaries(binaries: List[str], req_len: int) -> List[str]:
    ips = set(deepcopy(binaries))
    reduction_limit_reached = False
    max_vlsm = float("inf")
    while len(ips) > req_len and not reduction_limit_reached and max_vlsm != -1:
        ip_with_max_vlsm = max(ips, key=lambda x: x.rfind("1"))
        max_vlsm = ip_with_max_vlsm.rfind("1")
        reduced_ips = set()
        merged_ips = set()
        for ip in ips:
            if ip.rfind("1") == max_vlsm:
                reduced_ips.add(reduce_binary(ip))
            else:
                merged_ips.add(ip)

        filtered_set = set()
        for r_ip in reduced_ips:
            mask = get_mask(r_ip)
            for ip in merged_ips:
                if ip.startswith(mask):
                    filtered_set.add(r_ip)

        reduced_ips -= filtered_set
        merged_ips.update(reduced_ips)

        if len(merged_ips) > req_len:
            ips = merged_ips
        else:
            reduction_limit_reached = True

    return sorted(ips)


def smooth_merge_binaries(binaries: List[str], req_len: int) -> List[str]:
    non_reducible_ips = set()
    ips = set()
    for ip in binaries:
        if "1" not in reduce_binary(ip):
            non_reducible_ips.add(ip)
        else:
            ips.add(ip)

    while len(ips) > 0 and len(ips) + len(non_reducible_ips) > req_len:
        # print(f"{req_len=} {len(ips) + len(non_reducible_ips)=}")

        group_dict = defaultdict(list)
        for ip in ips:
            group_dict[ip.rfind("1")].append(ip)

        max_len = max(group_dict)
        lst = group_dict[max_len]
        for x, y in zip(lst, lst[1:]):
            i = x.rfind("1")
            if y.startswith(x[:i]):
                ips.remove(x)
                ips.remove(y)
                ips.add(reduce_binary(x))
                break
        else:
            x = lst[0]
            ips.remove(x)
            ips.add(reduce_binary(x))

        _ips = ips | non_reducible_ips
        non_reducible_ips = set()
        ips = set()
        for ip in _ips:
            if "1" not in reduce_binary(ip):
                non_reducible_ips.add(ip)
            else:
                ips.add(ip)

    ips.update(non_reducible_ips)
    return sorted(ips)


def main():
    file = "cidr4.txt"
    required_len = 20

    data = get_data(file)
    bin_ips = list(map(cidr4_to_binary, data))
    # for ip in bin_ips:
    #     print(ip)
    # print("#" * 128)

    rough_merged_bin_ips = rough_merge_binaries(bin_ips, required_len)
    print(f"{len(rough_merged_bin_ips)=}")
    for ip in rough_merged_bin_ips:
        print(ip)

    # print("#" * 128)
    #
    # smooth_merged_bin_ips = smooth_merge_binaries(rough_merged_bin_ips, required_len)
    # print(f"{len(smooth_merged_bin_ips)=}")
    # for ip in smooth_merged_bin_ips:
    #     print(ip)

    # smooth_merged_bin_ips = smooth_merge_binaries(bin_ips, required_len)
    # print(f"{len(smooth_merged_bin_ips)=}")
    # for ip in smooth_merged_bin_ips:
    #     print(ip)


if __name__ == "__main__":
    assert cidr4_to_binary("4.78.139.0/24") == "00000100010011101000101100000000"
    assert cidr4_to_binary("128.0.0.0/1") == "10000000000000000000000000000000"
    assert cidr4_to_binary("0.0.0.0/0") == "0" * 32
    assert cidr4_to_binary("0.8.0.0/13") == "00000000000010000000000000000000"

    assert binary_to_cidr4("00000100010011101000101100000000") == "4.78.139.0/24"
    assert binary_to_cidr4("10000000000000000000000000000000") == "128.0.0.0/1"
    assert binary_to_cidr4("00000000000000000000000000000000") == "0.0.0.0/0"
    assert binary_to_cidr4("00000000000010000000000000000000") == "0.8.0.0/13"

    assert (
        reduce_binary("00000100010011101000101100000000")
        == "00000100010011101000101000000000"
    )
    assert reduce_binary("10000000000000000000000000000000") == "0" * 32
    assert reduce_binary("0" * 32) == "0" * 32
    assert reduce_binary("00000000000010000000000000000000") == "0" * 32

    assert get_mask("00000100010011101000101100000000") == "000001000100111010001011"
    assert get_mask("10000000000000000000000000000000") == "1"
    assert get_mask("00000000000000000000000000000000") == ""
    assert get_mask("00000000000010000000000000000000") == "0000000000001"

    main()
    # cProfile.run("main()")
