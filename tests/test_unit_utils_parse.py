import pytest

from models import NodeSeriesEnum
from utils.parse import get_node_series, ParseError

def test_get_node_series_returns_enum():
    assert isinstance(get_node_series('C5026'), NodeSeriesEnum)

def test_get_node_series_returns_correct_enum():
    assert get_node_series('C5026') == NodeSeriesEnum(5)
    assert get_node_series('c5026') == NodeSeriesEnum(5)
    assert get_node_series('5026') == NodeSeriesEnum(5)
    assert get_node_series('5026') == NodeSeriesEnum(5)
    assert get_node_series('5') == NodeSeriesEnum(5)
    assert get_node_series(5) == NodeSeriesEnum(5)
    assert get_node_series('C6045') == NodeSeriesEnum(6)
    assert get_node_series('c6045') == NodeSeriesEnum(6)
    assert get_node_series(' C6045') == NodeSeriesEnum(6)
    assert get_node_series('c6045 ') == NodeSeriesEnum(6)
    assert get_node_series(' 6045 ') == NodeSeriesEnum(6)
    assert get_node_series(' 6045 ') == NodeSeriesEnum(6)
    assert get_node_series('6') == NodeSeriesEnum(6)
    assert get_node_series(6) == NodeSeriesEnum(6)

def test_get_node_series_raises_error_on_invalid_input():
    with pytest.raises(ParseError):
        get_node_series('C4026')
    with pytest.raises(ParseError):
        get_node_series('c4026')
    with pytest.raises(ParseError):
        get_node_series('4026')
    with pytest.raises(ParseError):
        get_node_series('C7045')
    with pytest.raises(ParseError):
        get_node_series('c7045')
    with pytest.raises(ParseError):
        get_node_series('7045')
    with pytest.raises(ParseError):
        get_node_series(1)
    with pytest.raises(ParseError):
        get_node_series(True)
    with pytest.raises(ParseError):
        get_node_series(7.034)

if __name__ == '__main__':
    pytest.main()
