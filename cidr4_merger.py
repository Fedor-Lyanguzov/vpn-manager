from copy import deepcopy
from typing import List

from netaddr import IPNetwork, cidr_merge


def get_ips(input_file) -> List[IPNetwork]:
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return [IPNetwork(line) for line in data]


def reduce_prefixlen(ip: IPNetwork, step=1) -> IPNetwork:
    """Reduce the CIDR prefix len by step"""
    new_ip = IPNetwork(ip)
    new_ip.prefixlen -= step
    return IPNetwork(new_ip.cidr)


def merge_ips(ips_to_reduce: List[IPNetwork], max_len, step=1) -> List[IPNetwork]:
    ips = deepcopy(ips_to_reduce)
    reduction_limit_reached = False
    while len(ips) > max_len and not reduction_limit_reached:
        reduced_ips = map(reduce_prefixlen, ips)
        merged_ips = cidr_merge(reduced_ips)
        if len(merged_ips) > 1:
            ips = merged_ips
        else:
            reduction_limit_reached = True
            print("The reduction limit has been reached")
    return ips


def main():
    file = "cidr4.txt"
    ips = get_ips(file)
    print(f"{len(ips)=}")
    merged_ips = merge_ips(ips, 10)
    print(f"{len(merged_ips)=}")
    print(", ".join([str(x) for x in merged_ips]))


if __name__ == "__main__":
    assert reduce_prefixlen(IPNetwork("4.78.139.0/24")) == IPNetwork("4.78.138.0/23")
    main()
