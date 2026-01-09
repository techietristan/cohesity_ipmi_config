from models import NodeSeriesEnum

class ParseError(Exception):
    pass

def get_node_series(user_input: str) -> NodeSeriesEnum:
    try:
        lower_input: str = str(user_input).lower()
        stripped_input: str = lower_input.strip()
        digits_only: str = stripped_input.strip('c')
        first_digit: int = int(digits_only[0])

        if first_digit not in [ enum.value for enum in NodeSeriesEnum ]:
            raise ParseError

        return NodeSeriesEnum(first_digit)
    except ValueError:
        raise ParseError

    