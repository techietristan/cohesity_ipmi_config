import os, sys

def exit_with_code(exit_code: int) -> None:
        try:
            sys.exit(exit_code)
        except SystemExit:
            os._exit(exit_code)