import pytest

from utils.ip import is_power_of_two, get_next_ip, get_netmask, is_netmask

def test_is_power_of_two_returns_bool():
    assert isinstance(is_power_of_two('2'), bool)
    assert isinstance(is_power_of_two('3'), bool)
    assert isinstance(is_power_of_two(64), bool)
    assert isinstance(is_power_of_two(65), bool)

def test_is_power_of_two_returns_false_on_nonbinary_input():
    assert is_power_of_two('192') == False
    assert is_power_of_two('3') == False
    assert is_power_of_two(6) == False
    assert is_power_of_two(1023) == False

def test_is_power_of_two_returns_true_on_binary_input():
    assert is_power_of_two('128') == True
    assert is_power_of_two('64') == True
    assert is_power_of_two(1) == True
    assert is_power_of_two(1024) == True

def test_get_next_ip_returns_string_on_valid_input():
    assert isinstance(get_next_ip('192.168.1.1'), str)
    assert isinstance(get_next_ip('1.1.1.1'), str)
    assert isinstance(get_next_ip('255.255.255.254'), str)

def test_get_next_ip_returns_none_on_invalid_input():
    assert get_next_ip('not_an_ip') is None
    assert get_next_ip('1.1.1.1.1') is None
    assert get_next_ip('255.255.255.255') is None

def test_get_next_ip_returns_valid_ip_on_valid_input():
    assert get_next_ip('192.168.1.1') == '192.168.1.2'
    assert get_next_ip('192.168.1.123 ') == '192.168.1.124'
    assert get_next_ip(' 1.1.1.1') == '1.1.1.2'
    assert get_next_ip('255.255.255.254') == '255.255.255.255'
    assert get_next_ip('255.255.0.255') == '255.255.1.0'

def test_get_netmask_returns_none_on_invalid_input():
    assert get_netmask('not_an_netmask') is None
    assert get_netmask('0.0.0.0') is None
    assert get_netmask('255.255.255.255') is None
    assert get_netmask('1.1.1.1.1') is None
    assert get_netmask(0) is None
    assert get_netmask(32) is None
    assert get_netmask(33) is None
    assert get_netmask('192.168.1.1') is None
    assert get_netmask('255.255.0.255') is None

def test_get_netmask_returns_string_on_valid_input():
    assert isinstance(get_netmask('255.255.255.128'), str)
    assert isinstance(get_netmask('255.255.254.0'), str)
    assert isinstance(get_netmask('255.255.255.0'), str)
    assert isinstance(get_netmask('255.0.0.0'), str)
    assert isinstance(get_netmask(1), str)
    assert isinstance(get_netmask(16), str)
    assert isinstance(get_netmask(31), str)

def test_get_netmask_returns_valid_output_on_valid_input():
    assert get_netmask('255.255.255.128') == '255.255.255.128'
    assert get_netmask('255.255.254.0 ') == '255.255.254.0'
    assert get_netmask('255.255.255.0') == '255.255.255.0'
    assert get_netmask(' 255.0.0.0') == '255.0.0.0'
    assert get_netmask(8) == '255.0.0.0'
    assert get_netmask(22) == '255.255.252.0'

def test_is_netmask_returns_false_on_invalid_input():
    assert is_netmask('not_an_netmask') == False
    assert is_netmask('0.0.0.0') == False
    assert is_netmask(' 255.255.255.255') == False
    assert is_netmask('1.1.1.1.1 ') == False
    assert is_netmask(0) == False
    assert is_netmask(32) == False
    assert is_netmask(33) == False
    assert is_netmask('192.168.1.1') == False
    assert is_netmask('255.255.0.255') == False

def test_is_netmask_returns_true_on_valid_input():
    assert is_netmask('255.255.255.128 ') == True
    assert is_netmask('255.255.254.0') == True
    assert is_netmask(' 255.255.255.0') == True
    assert is_netmask('255.0.0.0') == True
    assert is_netmask(8) == True
    assert is_netmask(22) == True

if __name__ == '__main__':
    pytest.main()
