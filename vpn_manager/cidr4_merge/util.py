mask = [((1 << i) - 1) << (32 - i) for i in range(33)]


def get_data(input_file='cidr4.txt'):
    with open(input_file, "r") as file:
        return file.read().splitlines()


def cidr4_to_node(cidr4: str):
    ip_address, mask_len = cidr4.strip().split("/")
    mask_len = int(mask_len)
    a, b, c, d = list(map(int, ip_address.split(".")))
    ip = a * 256**3 + b * 256**2 + c * 256**1 + d * 256**0
    return ip, mask_len


def make_cidr4(ip, mask_len) -> str:
    lst = [str(ip >> (i << 3) & 0xFF) for i in reversed(range(4))]
    ip_address = ".".join(lst)
    return f"{ip_address}/{mask_len}"
