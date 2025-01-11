import cProfile
from collections import defaultdict
from copy import deepcopy
from ipaddress import IPv4Address
from typing import List, Set


def get_data(input_file):
    with open(input_file, "r") as file:
        data = file.read().splitlines()
    return data


def main():
    file = "cidr4.txt"
    required_len = 15

    data = get_data(file)


if __name__ == "__main__":
    main()
    # cProfile.run("main()")
