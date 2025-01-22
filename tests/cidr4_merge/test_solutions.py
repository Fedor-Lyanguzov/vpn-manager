from vpn_manager.cidr4_merge.fast import solution as fast
from vpn_manager.cidr4_merge.precise import solution as precise, f
from vpn_manager.cidr4_merge.util import *


def test_true():
    assert True

#cidrs = list(map(cidr4_to_node, get_data()))

def test_fast_single_lifting():
    assert ([(0, 30)], 0) ==\
        fast([(0, 31), (2, 31)], 1)
    assert ([(0, 29)], 2) ==\
        fast([(0, 30), (4, 31)], 1)
    assert ([(0, 29)], 3) ==\
        fast([(0, 30), (4, 32)], 1)
    
def test_fast_double_lifting():
    assert ([(0, 29)], 4) ==\
        fast([(0, 31), (4, 31)], 1)
        
        
def test_fast_subnets():
    assert ([(0, 30)], 0) ==\
        fast([(0, 30), (0, 31)], 1)
    assert ([(0, 29)], 0) ==\
        fast([(0, 29), (4, 31)], 1)


def test_precise_single_lifting():
    assert ([(0, 30)], 0) ==\
        precise([(0, 31), (2, 31)], 1)
    assert ([(0, 29)], 2) ==\
        precise([(0, 30), (4, 31)], 1)
    assert ([(0, 29)], 3) ==\
        precise([(0, 30), (4, 32)], 1)
    
def test_precise_double_lifting():
    assert ([(0, 29)], 4) ==\
        precise([(0, 31), (4, 31)], 1)
        
        
def test_precise_subnets():
    assert ([(0, 30)], 0) ==\
        precise([(0, 30), (0, 31)], 1)
    assert ([(0, 29)], 0) ==\
        precise([(0, 29), (4, 31)], 1)
        
def test_precise_f_single_lifting():
    assert (0, (0, 30, 0)) ==\
        f((0, 31, 0), (2, 31, 0))
    assert (2, (0, 29, 2)) ==\
        f((0, 30, 0), (4, 31, 0))
    assert (3, (0, 29, 3)) ==\
        f((0, 30, 0), (4, 32, 0))
