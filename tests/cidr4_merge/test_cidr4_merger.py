from vpn_manager.cidr4_merge.cidr4_merger import (
    find_neighbors,
    merge_nodes,
    solution,
)


def test_true():
    assert True


def test_merge_nodes():
    assert merge_nodes((0, 32), (1, 32)) == ((0, 31), 0)
    assert merge_nodes((0, 32), (2, 32)) == ((0, 30), 2)
    assert merge_nodes((0, 32), (5, 32)) == ((0, 29), 6)
    assert merge_nodes((3, 32), (4, 32)) == ((0, 29), 6)
    assert merge_nodes((0, 32), (4, 30)) == ((0, 29), 3)
    assert merge_nodes((0, 32), (6, 31)) == ((0, 29), 5)


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


def test_solution():
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
