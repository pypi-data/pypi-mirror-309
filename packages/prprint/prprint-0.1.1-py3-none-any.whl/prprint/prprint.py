from pprint import pprint, PrettyPrinter, pp
from typing import IO

class clr:
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    
class ppr(PrettyPrinter):
    indent = 4
    depth = 1
    def __init__(self, indent: int = 4, width: int = 80, depth: int | None = None, stream: IO[str] | None = None, *, compact: bool = False, sort_dicts: bool = False, underscore_numbers: bool = True) -> None:
        super().__init__(indent, width, depth, stream, compact=compact, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)
        indent = 8
        underscore_numbers = True
        depth = 1
    
    def pprint(self, obj):
        print('')
        super().pprint(obj)
        print('')
        
def pprint(obj):
    printer = ppr()
    printer.pprint(obj)