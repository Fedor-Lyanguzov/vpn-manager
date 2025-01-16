from cidr4_merger import (
    answer,
    cidr4_to_node,
    get_group_with_max_mask_len,
    get_net_addr,
    get_parent,
    get_parent_mask,
    have_same_parent,
    merge_nodes,
    node_to_cidr4,
    reduce_nodes,
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


def test_node_to_cidr4():
    assert node_to_cidr4(72256256, 24) == "4.78.139.0/24"
    assert node_to_cidr4(0, 32) == "0.0.0.0/32"


def test_get_net_addr():
    assert get_net_addr(ip_a, 5) == ip_c
    assert get_net_addr(ip_b, 5) == ip_c
    assert get_net_addr(0, 1) == 0
    assert get_net_addr(0, 0) == 0


def test_get_parent_mask():
    assert get_parent_mask(ip_a, 6) == ip_c
    assert get_parent_mask(ip_b, 6) == ip_c
    assert get_parent_mask(0, 1) == 0
    assert get_parent_mask(0, 0) is None


def test_have_same_parent():
    assert have_same_parent(ip_a, 6, ip_b, 6) is True
    assert have_same_parent(ip_a, 6, ip_b, 5) is False
    assert have_same_parent(ip_a, 6, ip_d, 6) is False
    assert have_same_parent(ip_a, 6, 0, 1) is False
    assert have_same_parent(ip_a, 6, 0, 0) is False


def test_sort_nodes():
    assert sort_nodes(
        [
            (401219072, 24, 0),
            (2899902464, 19, 0),
            (400657664, 24, 0),
            (520969728, 23, 0),
        ]
    ) == [
        (2899902464, 19, 0),
        (520969728, 23, 0),
        (400657664, 24, 0),
        (401219072, 24, 0),
    ]


def test_get_group_with_max_mask_len():
    assert get_group_with_max_mask_len(
        [
            (2899902464, 19, 0),
            (520969728, 23, 0),
            (400657664, 24, 0),
            (401219072, 24, 0),
        ]
    ) == [(400657664, 24, 0), (401219072, 24, 0)]

    assert get_group_with_max_mask_len(
        [
            (401219072, 24, 0),
            (2899902464, 19, 0),
            (520969728, 23, 0),
        ]
    ) == [(401219072, 24, 0)]


def test_get_parent():
    assert get_parent((0, 2, 12), (1073741824, 2, 3)) == (0, 1, 15)
    assert get_parent((2147483648, 2, 1), (3221225472, 2, 2)) == (2147483648, 1, 3)


def test_reduce_nodes():
    assert reduce_nodes(
        [
            (0, 2, 12),
            (1073741824, 2, 3),
        ]
    ) == [
        (0, 1, 15),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12),
            (1073741824, 2, 3),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ]
    ) == [
        (2147483648, 1, 3),
        (0, 2, 12),
        (1073741824, 2, 3),
    ]

    assert reduce_nodes(
        [
            (0, 2, 12),
            (2147483648, 1, 0),
        ]
    ) == [
        (0, 1, 12 + 2**30),
        (2147483648, 1, 0),
    ]

    assert reduce_nodes(
        [
            (0, 1, 12 + 2**30),
            (2147483648, 1, 0),
        ]
    ) == [
        (0, 0, 12 + 2**30),
    ]


def test_merge_nodes():
    assert merge_nodes(
        [
            (0, 2, 12),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ],
        2,
    ) == [
        (2147483648, 1, 3),
        (0, 2, 12),
    ]

    assert merge_nodes(
        [
            (0, 2, 12),
            (2147483648, 2, 1),
            (3221225472, 2, 2),
        ],
        1,
    ) == [(0, 0, 15 + 2**30)]


def test_answer():
    assert answer(
        [
            (0, 2, 0),
            (2147483648, 2, 0),
            (3221225472, 2, 12),
        ],
        2,
    ) == (["128.0.0.0/1", "0.0.0.0/2"], 12)

    assert answer(
        [
            (0, 2, 0),
            (2147483648, 2, 0),
        ],
        1,
    ) == (["0.0.0.0/0"], 2**31)
