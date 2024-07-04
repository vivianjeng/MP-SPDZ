import pytest, statistics

import mpcstats_lib
from .lib import execute_elem_filter_test, execute_join_test, execute_stat_func_test

player_data_4x2_2_party = [
    # party 0
    [
        [0, 1, 2, 3],  # column 0
        [170, 160, 152, 180],  # column 1
    ],
    # party 1
    [
        [3, 0, 4, 5],
        [50, 60, 70, 100],
    ]
]

def test_correlation_success():
    execute_stat_func_test(
        mpcstats_lib.correlation,
        statistics.correlation,
        num_params = 2,
        player_data = player_data_4x2_2_party,
        selected_col = 1,
        tolerance = 0.01,
    )

def test_covariance_success():
    execute_stat_func_test(
        mpcstats_lib.covariance,
        statistics.covariance,
        num_params = 2,
        player_data = player_data_4x2_2_party,
        selected_col = 1,
        tolerance = 0.01,
    )

def test_geometric_mean_success():
    execute_stat_func_test(
        mpcstats_lib.geometric_mean,
        statistics.geometric_mean,
        num_params = 1,
        player_data = player_data_4x2_2_party,
        selected_col = 1,
        tolerance = 0.01,
    )

def test_median_success():
    execute_stat_func_test(
        mpcstats_lib.median,
        statistics.median,
        num_params = 1,
        player_data = player_data_4x2_2_party,
        selected_col = 1,
        tolerance = 0.01,
    )

def test_where_success():
    M = mpcstats_lib.MAGIC_NUMBER

    player_data = [
        [
            [-123, 0, 20, 40],
            [0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
    ]
    def test(elem_filter_gen, exp):
        execute_elem_filter_test(
            func = mpcstats_lib.where,
            elem_filter_gen = elem_filter_gen,
            player_data = player_data,
            selected_col = 0,
            exp = exp,
        )

    test(
        lambda col: [n < -123 for n in col],
        [M, M, M, M],
    )
    test(
        lambda col: [n < 0 for n in col],
        [-123, M, M, M],
    )
    test(
        lambda col: [n == 0 for n in col],
        [M, 0, M, M],
    )
    test(
        lambda col: [n >= 20 for n in col],
        [M, M, 20, 40],
    )
    test(
        lambda col: [n >= 40 for n in col],
        [M, M, M, 40],
    )
    test(
        lambda col: [n > 40 for n in col],
        [M, M, M, M],
    )

def test_join_success():
    M = mpcstats_lib.MAGIC_NUMBER

    # 1. 0 and 3 of col 0 mat 1 match 3 and 0 in col 0 mat 2
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
                [152, 160, 170, 180],
            ],
            [
                [3, 0, 4],
                [50, 60, 70],
            ],
        ],
        0,
        0,
        [
            [0, 1, 2, 3],
            [152, 160, 170, 180],
            [0, M, M, 3],
            [60, M, M, 50],
        ],
    )

    # 2. the same as 1 except that mat 2 has 3 columns
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
                [152, 160, 170, 180],
            ],
            [
                [3, 0, 4],
                [50, 60, 70],
                [12, 34, 56],
            ],
        ],
        0,
        0,
        [
            [0, 1, 2, 3],
            [152, 160, 170, 180],
            [0, M, M, 3],
            [60, M, M, 50],
            [34, M, M, 12],
        ],
    )

    # 3. col 0 mat 1 and col 1 mat 2 have no elems in common
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
                [152, 160, 170, 180],
            ],
            [
                [3, 0, 4],
                [50, 60, 70],
            ],
        ],
        0,
        1,
        [
            [0, 1, 2, 3],
            [152, 160, 170, 180],
            [M, M, M, M],
            [M, M, M, M],
        ],
    )

    # 4. Every element in col 0 mat 1 has a match in col 0 mat 2
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
                [152, 160, 170, 180],
            ],
            [
                [3, 1, 0, 2],
                [50, 60, 70, 80],
            ],
        ],
        0,
        0,
        [
            [0, 1, 2, 3],
            [152, 160, 170, 180],
            [0, 1, 2, 3],
            [70, 60, 80, 50],
        ],
    )

    # 5. mat 2 has 1 column only
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
                [152, 160, 170, 180],
            ],
            [
                [9, 11, 0, 2],
            ],
        ],
        0,
        0,
        [
            [0, 1, 2, 3],
            [152, 160, 170, 180],
            [0, M, 2, M],
        ],
    )

    # 6. mat 1 has 1 column only <- fails
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1, 2, 3],
            ],
            [
                [3, 0, 1],
                [50, 60, 70],
            ],
        ],
        0,
        0,
        [
            [0, 1, 2, 3],
            [0, 1, M, 3],
            [60, 70, M, 50],
        ],
    )

    # 7. mat 2 has more rows than mat 1
    execute_join_test(
        mpcstats_lib.join,
        [
            [
                [0, 1],
                [10, 20],
            ],
            [
                [3, 1, 9],
                [50, 60, 70],
            ],
        ],
        0,
        0,
        [
            [0, 1],
            [10, 20],
            [M, 1],
            [M, 60],
        ],
    )
