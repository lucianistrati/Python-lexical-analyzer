import re

python_program = """"""

def lexical_analyzer():
    """

    :return:
    current_token_type: string (the data type of the token or if it is reserved)
    current_token_length: int (the lenght of the token itself)
    current_token_line: string (the line in the program that contains the token)
    first_character_token: a pointer towards the first letter of the word
    error_msg: string (when an error occurs)
    """


class LexicalAnalyzer():
    PYTHON_KEYWORDS_LIST = ["False", "await", "else", "import", "pass", "None",
                              "break", "except", "in", "raise", "True", "class",
                              "finally", "is", "return", "and", "continue", "for",
                              "lambda", "try","as","def", "from", "nonlocal",
                              "while", "assert","del", "global", "not", "with",
                              "async", "elif", "if", "or", "yield"]

    TOKEN_TYPES_LIST = ["identifier", "keyword", "str", "int", "float",
                        "complex", "list", "tuple", "range", "dict", "set",
                        "frozenset", "bool", "bytes", "bytearray", "memoryview",
                        "comment", "whitespace", "operator", "separator",
                        "error", "invalid_token"]

    DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    SMALL_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                     "m", "n",
                     "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    CAPITAL_LETTERS = [letter.capitalize() for letter in SMALL_LETTERS]

    OPERATORS = [ "//", "=", "-=",
                 "/=", "%=",
                 "//=", "&=", "|=", "^=", ">>=", "<<=", "==", "!=", ">=",
                 "<=", "and", "or", "not", "is", "is not", "in", "not in", "&",
                 "|",
                 "~", "<<", ">>", "<", ">", "^", "-", "/", "%", "\+", "\*", "\*\*",  "\+=", "\*=", "\*\*="]

    SEPARATORS = [',',';','.', "(", ")", "[", "]", ":"]

    def __init__(self, filename):
        self.filename = filename


#separatori: ; , ( ) [ ]
# constante: str, int, float, double, boolene

# trateaza erorile
# a =  (identifactor = )
# """  neinchise
# ' neinchise
# daca nu se inchid parantezate corect
# 12 = eroare (constanta = )
# (keyword = )
#