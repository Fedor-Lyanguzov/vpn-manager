from vpn_manager.cidr4_merge.cidr4_merger import (
    calc_dip,
    cidr4_to_node,
    find_neighbors,
    find_parent,
    make_cidr4,
    merge_two_nodes,
    solution,
)


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


def test_find_parent():
    assert find_parent((0, 2), (1073741824, 2)) == (0, 1)
    assert find_parent((2147483648, 2), (3221225472, 2)) == (2147483648, 1)
    assert find_parent((0, 2), (3221225472, 2)) == (0, 0)
    assert find_parent((1, 32), (6, 32)) == (0, 29)

    assert find_parent((0, 32), (0, 29)) == (0, 29)
    assert find_parent((0, 1), (1073741824, 2)) == (0, 1)
    assert find_parent((0, 0), (3221225472, 2)) == (0, 0)


def test_calc_dip():
    assert calc_dip(32, 32, 31) == 0
    assert calc_dip(32, 32, 30) == 2
    assert calc_dip(32, 32, 29) == 6
    assert calc_dip(32, 30, 29) == 3
    assert calc_dip(32, 31, 29) == 5
    assert calc_dip(32, 31, 29) == 5

    assert calc_dip(2, 2, 1) == 0
    assert calc_dip(2, 2, 0) == 2**31
    assert calc_dip(3, 3, 1) == 2**30


def test_merge_two_nodes():
    assert merge_two_nodes((0, 32), (1, 32)) == ((0, 31), 0)
    assert merge_two_nodes((0, 32), (2, 32)) == ((0, 30), 2)
    assert merge_two_nodes((0, 32), (5, 32)) == ((0, 29), 6)
    assert merge_two_nodes((3, 32), (4, 32)) == ((0, 29), 6)
    assert merge_two_nodes((0, 32), (4, 30)) == ((0, 29), 3)
    assert merge_two_nodes((0, 32), (6, 31)) == ((0, 29), 5)


def test_find_neighbors():
    assert find_neighbors([(0, 32), (2, 32), (4, 32), (6, 32)]) == []
    assert find_neighbors([(0, 32), (1, 32)]) == [(0, (0, 32), (1, 32))]
    assert find_neighbors(
        [
            (0, 32),
            (1, 32),
            (6, 32),
            (7, 32),
        ]
    ) == [
        (0, (0, 32), (1, 32)),
        (2, (6, 32), (7, 32)),
    ]
    assert find_neighbors(
        [
            (0, 32),
            (1, 32),
            (6, 32),
        ]
    ) == [
        (0, (0, 32), (1, 32)),
    ]


def test_merge_nodes():
    assert solution(
        [
            (0, 32),
            (3, 32),
            (4, 32),
        ],
        2,
    ) == ([(0, 30), (4, 32)], 2)

    assert solution(
        [
            (0, 32),
            (3, 32),
            (4, 32),
            (7, 32),
        ],
        2,
    ) == ([(0, 29)], 4)

    assert solution(
        [
            (0, 32),
            (3, 32),
            (4, 32),
            (7, 32),
        ],
        1,
    ) == ([(0, 29)], 4)
