import pytest

from cidr4_merger import (
    Cidr4MergerError,
    cidr4_to_node,
    find_neighbours_singles,
    get_group_with_max_mask_len,
    get_net_addr,
    get_parent_ip,
    have_same_parent,
    lift_lonely_node,
    make_cidr4,
    make_groups,
    make_parent,
    merge_neighbors,
    merge_nodes_cycle,
    merge_nodes_deprecated,
    merge_nodes_recursion,
    reduce_nodes,
    sort_nodes,
)

from .cidr4_data_for_tests import test_cidr4_data


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
    assert cidr4_to_node("4.78.139.0/24") == (72256256, 24, 0, 72256000)
    assert cidr4_to_node("0.0.0.0/32") == (0, 32, 0, 0)

    assert cidr4_to_node("23.234.30.0/24") == (401219072, 24, 0, 401219072)
    assert cidr4_to_node("172.217.0.0/19") == (2899902464, 19, 0, 2899902464)
    assert cidr4_to_node("23.225.141.0/24") == (400657664, 24, 0, 400657408)
    assert cidr4_to_node("31.13.94.0/23") == (520969728, 23, 0, 520969216)

    assert cidr4_to_node("0.0.0.0/2") == (0, 2, 0, 0)
    assert cidr4_to_node("64.0.0.0/2") == (1073741824, 2, 0, 0)
    assert cidr4_to_node("128.0.0.0/2") == (2147483648, 2, 0, 2147483648)
    assert cidr4_to_node("192.0.0.0/2") == (3221225472, 2, 0, 2147483648)


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


def test_have_same_parent():
    assert have_same_parent(ip_c, 6, ip_c, 6) is True
    assert have_same_parent(ip_c, 6, ip_c, 5) is False
    assert have_same_parent(ip_a, 6, ip_d, 6) is False
    assert have_same_parent(ip_a, 6, 0, 1) is False
    assert have_same_parent(ip_a, 6, 0, 0) is False


def test_sort_nodes():
    assert sort_nodes(
        [
            (401219072, 24, 0, 401219072),
            (2899902464, 19, 0, 2899902464),
            (400657664, 24, 0, 400657408),
            (520969728, 23, 0, 520969216),
        ]
    ) == [
        (2899902464, 19, 0, 2899902464),
        (520969728, 23, 0, 520969216),
        (400657664, 24, 0, 400657408),
        (401219072, 24, 0, 401219072),
    ]


def test_get_group_with_max_mask_len():
    assert get_group_with_max_mask_len(
        [
            (2899902464, 19, 0, 2899902464),
            (520969728, 23, 0, 520969216),
            (400657664, 24, 0, 400657408),
            (401219072, 24, 0, 401219072),
        ]
    ) == [(400657664, 24, 0, 400657408), (401219072, 24, 0, 401219072)]

    assert get_group_with_max_mask_len(
        [
            (401219072, 24, 0, 401219072),
            (2899902464, 19, 0, 2899902464),
            (520969728, 23, 0, 520969216),
        ]
    ) == [(401219072, 24, 0, 401219072)]


def test_make_parent():
    assert make_parent((0, 2, 12, 0), (1073741824, 2, 3, 0)) == (0, 1, 15, 0)
    assert make_parent(
        (2147483648, 2, 1, 2147483648), (3221225472, 2, 2, 2147483648)
    ) == (2147483648, 1, 3, 0)

    with pytest.raises(Exception) as exc_info:
        make_parent((0, 2, 12, 0), (3221225472, 2, 2, 2147483648))
    assert str(exc_info.value) == "Nodes must be neighbors!"
    assert exc_info.type is Cidr4MergerError


def test_reduce_nodes():
    assert reduce_nodes(
        [
            (0, 2, 12, 0),
            (1073741824, 2, 3, 0),
        ]
    ) == [
        (0, 1, 15, 0),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12, 0),
            (1073741824, 2, 3, 0),
            (2147483648, 2, 1, 2147483648),
            (3221225472, 2, 2, 2147483648),
        ]
    ) == [
        (2147483648, 1, 3, 0),
        (0, 2, 12, 0),
        (1073741824, 2, 3, 0),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12, 0),
            (2147483648, 1, 0, 0),
        ]
    ) == [
        (0, 1, 12 + 2**30, 0),
        (2147483648, 1, 0, 0),
    ]

    with pytest.raises(Exception) as exc_info:
        reduce_nodes(
            [
                (0, 1, 12 + 2**30, 0),
                (2147483648, 1, 0, 0),
            ]
        )
    assert exc_info.type is Cidr4MergerError
    assert str(exc_info.value) == "The top of the tree has no parent!"


def test_merge_nodes_deprecated():
    assert merge_nodes_deprecated(
        [
            (0, 2, 12, 0),
            (2147483648, 2, 1, 2147483648),
            (3221225472, 2, 2, 2147483648),
        ],
        2,
    ) == [
        (2147483648, 1, 3, 0),
        (0, 2, 12, 0),
    ]

    with pytest.raises(Exception) as exc_info:
        merge_nodes_deprecated(
            [
                (0, 2, 12, 0),
                (2147483648, 2, 1, 2147483648),
                (3221225472, 2, 2, 2147483648),
            ],
            1,
        )
    assert exc_info.type is Cidr4MergerError
    assert str(exc_info.value) == "The top of the tree has no parent!"


def test_make_groups():
    nodes = [
        (2398793728, 20, 0, 2398789632),
        (2899943424, 20, 0, 2899943424),
        (3627728896, 20, 0, 3627728896),
        (520963072, 22, 0, 520962048),
        (1089054720, 22, 0, 1089054720),
        (2899902464, 19, 0, 2899902464),
        (2915221504, 19, 0, 2915221504),
    ]
    assert dict(make_groups(nodes)) == {
        20: [
            (2398793728, 20, 0, 2398789632),
            (2899943424, 20, 0, 2899943424),
            (3627728896, 20, 0, 3627728896),
        ],
        22: [(520963072, 22, 0, 520962048), (1089054720, 22, 0, 1089054720)],
        19: [(2899902464, 19, 0, 2899902464), (2915221504, 19, 0, 2915221504)],
    }


@pytest.fixture
def nodes_only_neighbours():
    return [
        (0, 2, 12, 0),
        (1073741824, 2, 3, 0),
        (2147483648, 2, 1, 2147483648),
        (3221225472, 2, 2, 2147483648),
    ]


@pytest.fixture
def nodes_only_singles():
    return [
        (0, 2, 12, 0),
        (2147483648, 2, 1, 2147483648),
    ]


@pytest.fixture
def nodes_with_neighbours_n_singles():
    return [
        (0, 2, 12, 0),
        (1073741824, 2, 3, 0),
        (2147483648, 2, 1, 2147483648),
    ]


@pytest.fixture
def groups_only_neighbours(nodes_only_neighbours):
    return make_groups(nodes_only_neighbours)


@pytest.fixture
def groups_only_singles(nodes_only_singles):
    return make_groups(nodes_only_singles)


@pytest.fixture
def groups_with_neighbours_n_singles(nodes_with_neighbours_n_singles):
    return make_groups(nodes_with_neighbours_n_singles)


def test_find_neighbours_singles(
    groups_only_neighbours,
    groups_only_singles,
    groups_with_neighbours_n_singles,
):
    assert find_neighbours_singles(groups_only_neighbours) == (
        [
            ((0, 2, 12, 0), (1073741824, 2, 3, 0)),
            ((2147483648, 2, 1, 2147483648), (3221225472, 2, 2, 2147483648)),
        ],
        [],
    )

    assert find_neighbours_singles(groups_only_singles) == (
        [],
        [(0, 2, 12, 0), (2147483648, 2, 1, 2147483648)],
    )

    assert find_neighbours_singles(groups_with_neighbours_n_singles) == (
        [((0, 2, 12, 0), (1073741824, 2, 3, 0))],
        [(2147483648, 2, 1, 2147483648)],
    )


def test_merge_neighbors__only_neighbours(nodes_only_neighbours):
    new_nodes = merge_neighbors(
        nodes_only_neighbours,
        [
            ((0, 2, 12, 0), (1073741824, 2, 3, 0)),
            ((2147483648, 2, 1, 2147483648), (3221225472, 2, 2, 2147483648)),
        ],
    )
    assert new_nodes == [
        (0, 1, 15, 0),
        (2147483648, 1, 3, 0),
    ]


def test_merge_neighbors__neighbours_n_singles(nodes_with_neighbours_n_singles):
    new_nodes = merge_neighbors(
        nodes_with_neighbours_n_singles,
        [((0, 2, 12, 0), (1073741824, 2, 3, 0))],
    )
    assert new_nodes == [
        (0, 1, 15, 0),
        (2147483648, 2, 1, 2147483648),
    ]


def test_lift_lonely_node(nodes_only_singles):
    singles = [(0, 2, 12, 0), (2147483648, 2, 1, 2147483648)]
    new_nodes = lift_lonely_node(nodes_only_singles, singles)
    assert new_nodes == [(2147483648, 1, 1073741825, 0), (0, 2, 12, 0)]


def test_merge_nodes_recursion():
    assert merge_nodes_recursion(
        [
            (0, 2, 12, 0),
            (2147483648, 2, 1, 2147483648),
            (3221225472, 2, 2, 2147483648),
        ],
        2,
    ) == [
        (2147483648, 1, 3, 0),
        (0, 2, 12, 0),
    ]

    with pytest.raises(Exception) as exc_info:
        merge_nodes_recursion(
            [
                (0, 2, 12, 0),
                (2147483648, 2, 1, 2147483648),
                (3221225472, 2, 2, 2147483648),
            ],
            1,
        )
    assert exc_info.type is Cidr4MergerError
    assert str(exc_info.value) == "The top of the tree has no parent!"


def test_merge_nodes_cycle():
    assert merge_nodes_cycle(
        [
            (0, 2, 12, 0),
            (2147483648, 2, 1, 2147483648),
            (3221225472, 2, 2, 2147483648),
        ],
        2,
    ) == [
        (2147483648, 1, 3, 0),
        (0, 2, 12, 0),
    ]

    with pytest.raises(Exception) as exc_info:
        merge_nodes_cycle(
            [
                (0, 2, 12, 0),
                (2147483648, 2, 1, 2147483648),
                (3221225472, 2, 2, 2147483648),
            ],
            1,
        )
    assert exc_info.type is Cidr4MergerError
    assert str(exc_info.value) == "The top of the tree has no parent!"


def test_merge_nodes_recursion_vs_cycle():
    required_len = 20

    test_data = test_cidr4_data.strip().splitlines()
    test_nodes = list(map(cidr4_to_node, test_data))
    test_nodes = sort_nodes(test_nodes)

    merged_nodes_recursion = merge_nodes_recursion(test_nodes, required_len)
    merged_nodes_cycle = merge_nodes_cycle(test_nodes, required_len)

    assert merged_nodes_recursion == merged_nodes_cycle
