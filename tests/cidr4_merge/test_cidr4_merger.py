import pytest

from vpn_manager.cidr4_merge.cidr4_merger import (
    Cidr4MergerError,
    cidr4_to_node,
    get_net_addr,
    get_parent_ip,
    make_cidr4,
    make_parent,
    sort_nodes,
)


def test_true():
    assert True


bin_a = "10011000000000001000010000010000"
assert len(bin_a) == 32
ip_a = int(bin_a, 2)

bin_b = "10011100000000000000000000101011"
assert len(bin_b) == 32
ip_b = int(bin_b, 2)

bin_c = "10011000000000000000000000000000"
assert len(bin_c) == 32
ip_c = int(bin_c, 2)

bin_d = "11111100000000000000000000000000"
assert len(bin_c) == 32
ip_d = int(bin_d, 2)


def test_cidr4_to_node():
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24, 0)
    assert cidr4_to_node("0.0.0.0/32") == (0, 32, 0)

    assert cidr4_to_node("23.234.30.0/24") == (401219072, 24, 0)
    assert cidr4_to_node("172.217.0.0/19") == (2899902464, 19, 0)
    assert cidr4_to_node("23.225.141.0/24") == (400657664, 24, 0)
    assert cidr4_to_node("31.13.94.0/23") == (520969728, 23, 0)

    assert cidr4_to_node("0.0.0.0/2") == (0, 2, 0)
    assert cidr4_to_node("64.0.0.0/2") == (1073741824, 2, 0)
    assert cidr4_to_node("128.0.0.0/2") == (2147483648, 2, 0)
    assert cidr4_to_node("192.0.0.0/2") == (3221225472, 2, 0)


def test_make_cidr4():
    assert make_cidr4(72256256, 24) == "4.78.139.0/24"
    assert make_cidr4(0, 32) == "0.0.0.0/32"

    assert make_cidr4(401219072, 24) == "23.234.30.0/24"
    assert make_cidr4(2899902464, 19) == "172.217.0.0/19"
    assert make_cidr4(400657664, 24) == "23.225.141.0/24"
    assert make_cidr4(520969728, 23) == "31.13.94.0/23"


def test_get_net_addr():
    assert get_net_addr(ip_a, 5) == ip_c
    assert get_net_addr(ip_b, 5) == ip_c
    assert get_net_addr(0, 1) == 0
    assert get_net_addr(0, 0) == 0


def test_get_parent_mask():
    assert get_parent_ip(ip_a, 6) == ip_c
    assert get_parent_ip(ip_b, 6) == ip_c
    assert get_parent_ip(0, 1) == 0

    with pytest.raises(Exception) as exc_info:
        get_parent_ip(0, 0)
    assert str(exc_info.value) == "The top of the tree has no parent!"
    assert exc_info.type is Cidr4MergerError


def test_sort_nodes():
    assert sort_nodes(
        [
            (401219072, 24, 0),
            (2899902464, 19, 0),
            (400657664, 24, 0),
            (520969728, 23, 0),
        ]
    ) == [
        (400657664, 24, 0),
        (401219072, 24, 0),
        (520969728, 23, 0),
        (2899902464, 19, 0),
    ]


@pytest.mark.skip(reason="broken")
def test_make_parent():
    assert make_parent((0, 2, 12, 0), (1073741824, 2, 3, 0)) == (0, 1, 15, 0)
    assert make_parent(
        (2147483648, 2, 1, 2147483648), (3221225472, 2, 2, 2147483648)
    ) == (2147483648, 1, 3, 0)

    with pytest.raises(Exception) as exc_info:
        make_parent((0, 2, 12, 0), (3221225472, 2, 2, 2147483648))
    assert str(exc_info.value) == "Nodes must be neighbors!"
    assert exc_info.type is Cidr4MergerError
