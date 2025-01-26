from vpn_manager.cidr4_merge.util import cidr4_to_node, make_cidr4


def test_true():
    assert True


def test_cidr4_to_node():
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24)
    assert cidr4_to_node("0.0.0.0/32") == (0, 32)

    assert cidr4_to_node("23.234.30.0/24") == (401219072, 24)
    assert cidr4_to_node("172.217.0.0/19") == (2899902464, 19)
    assert cidr4_to_node("23.225.141.0/24") == (400657664, 24)
    assert cidr4_to_node("31.13.94.0/23") == (520969728, 23)

    assert cidr4_to_node("0.0.0.0/2") == (0, 2)
    assert cidr4_to_node("64.0.0.0/2") == (1073741824, 2)
    assert cidr4_to_node("128.0.0.0/2") == (2147483648, 2)
    assert cidr4_to_node("192.0.0.0/2") == (3221225472, 2)


def test_make_cidr4():
    assert make_cidr4(72256256, 24) == "4.78.139.0/24"
    assert make_cidr4(0, 32) == "0.0.0.0/32"

    assert make_cidr4(401219072, 24) == "23.234.30.0/24"
    assert make_cidr4(2899902464, 19) == "172.217.0.0/19"
    assert make_cidr4(400657664, 24) == "23.225.141.0/24"
    assert make_cidr4(520969728, 23) == "31.13.94.0/23"
