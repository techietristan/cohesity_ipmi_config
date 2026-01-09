import pytest

from pydantic_settings import BaseSettings
from utils.hostname import get_next_hostname

class TestConfig(BaseSettings):
    node_letters: list[str] | None = ['a', 'b', 'c', 'd']
    
test_config = TestConfig()
def test_get_next_hostname_returns_string():
    assert isinstance(get_next_hostname(test_config, 'hostname123'), str)
    assert isinstance(get_next_hostname(test_config, 'hostname123a'), str)
    assert isinstance(get_next_hostname(test_config, 'hostname123b'), str)

def test_get_next_hostname_returns_none_on_invalid_input():
    assert get_next_hostname(test_config, 'hostname') == None
    assert get_next_hostname(test_config, 'host name') == None
    assert get_next_hostname(test_config, 32) == None

def test_get_next_hostname_returns_valid_hostname_on_valid_input():
    assert get_next_hostname(test_config, 'hostname123') == 'hostname124'
    assert get_next_hostname(test_config, 'hostname123a') == 'hostname123b'
    assert get_next_hostname(test_config, 'hostname123d') == 'hostname124a'
    assert get_next_hostname(test_config, ' hostname123') == 'hostname124'
    assert get_next_hostname(test_config, 'hostname123a ') == 'hostname123b'
    assert get_next_hostname(test_config, ' hostname123d ') == 'hostname124a'
    assert get_next_hostname(test_config, ' hostname-123') == 'hostname-124'
    assert get_next_hostname(test_config, 'hostname_123a ') == 'hostname_123b'

if __name__ == '__main__':
    pytest.main()
