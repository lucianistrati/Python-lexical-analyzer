class Token:
    TOKEN_TYPES_LIST = ["identifier", "keyword", "str", "int", "float",
                        "complex", "list", "tuple", "range","dict","set",
                        "frozenset", "bool","bytes", "bytearray", "memoryview",
                        "comment", "whitespace", "operator", "separator",
                        "error", "invalid_token", "lexical_error"]

    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    SMALL_LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                     'o','p','q','r','s','t','u','v','w','x','y','z']

    CAPITAL_LETTERS = [letter.capitalize() for letter in SMALL_LETTERS]

    OPERATORS = ['=', '-','/','%','//','=','+=','-=','*=','/=','%=',
                 '//=','**=','&=','|=','^=','>>=','<<=','==','!=','>','<','>=',
                 '<=','and','or','not','is','is not','in','not in','&','|','^',
                 '~','<<','>>', '+', '*', '**']


    def __init__(self, token):
        self.token = token
        self.token_type = ""


    def determine_token_type(self):
        if self.is_keyword():
            self.token_type = "keyword"
        elif self.is_separator():
            self.token_type = "separator"
        elif self.is_int():
            self.token_type = "int"
        elif self.is_str():
            self.token_type = "str"
        elif self.is_list():
            self.token_type = "list"
        elif self.is_tuple():
            self.token_type = "tuple"
        elif self.is_identifier():
            self.token_type = "identifier"
        elif self.is_frozenset():
            self.token_type = "identifier"
        elif self.is_dict():
            self.token_type = "dict"
        elif self.is_float():
            self.token_type = "float"
        elif self.is_comment():
            self.token_type = "comment"
        elif self.is_bool():
            self.token_type = "bool"
        elif self.is_complex():
            self.token_type = "complex"
        elif self.is_set():
            self.token_type = "set"
        elif self.is_whitespace():
            self.token_type = "whitespace"
        elif self.is_range():
            self.token_type = "range"
        else:
            self.token_type = "invalid_token"


    def is_identifier(self):
        if self.token[0] in self.DIGITS:
            return False
        for i in range(len(self.token)):
            if self.token[i] not in self.SMALL_LETTERS and self.token[i] not in \
                    self.CAPITAL_LETTERS and self.token[i] not in self.DIGITS \
                    and self.token[i]!="_":
                return False
            if self.token[i] in ["!", "@", "#", "$", "%"] or self.token[i] in self.OPERATORS:
                return False
        if self.is_keyword():
            return False
        return True


    def is_keyword(self):
        return self.token in ["False", "await", "else", "import", "pass", "None",
                              "break", "except", "in", "raise", "True", "class",
                              "finally", "is", "return", "and", "continue", "for",
                              "lambda", "try","as","def", "from", "nonlocal",
                              "while", "assert","del", "global", "not", "with",
                              "async", "elif", "if", "or", "yield"]


    def is_str(self):
        return (self.token[0]=='"' and self.token[-1]=='"') or \
        (self.token[0]=="'" and self.token[-1]=="'") or \
        (self.token[0]=="'''" and self.token[-1]=="'''") or \
        (self.token[0]=='"""' and self.token[-1]=='"""')


    def is_int(self):
        if self.token[0] == "0":
            return False
        for i in range(len(self.token)):
            if self.token[i] not in self.DIGITS:
                return False
        return True


    def is_float(self):
        dot_counter = 0
        if self.token[0] == "0":
            return False
        if self.token[0] not in self.DIGITS or self.token[-1] not in self.DIGITS:
            return False
        for i in range(len(self.token)):
            if self.token[i] == '.':
                if dot_counter == 0:
                    dot_counter += 1
                    continue
                else:
                    return False
            if self.token[i] not in self.DIGITS:
                return False
        return True


    def is_complex(self):
        if 'j' in self.token:
            return True
        return False

    def is_collection_element(self):
        if self.token.is_set() == False and \
            self.token.is_bool() == False and \
            self.token.is_int() == False and \
            self.token.is_bytearray() == False and \
            self.token.is_complex() == False and \
            self.token.is_float() == False and \
            self.token.is_dict() == False and \
            self.token.is_frozenset() == False and \
            self.token.is_identifier() == False and \
            self.token.is_tuple() == False and \
            self.token.is_memoryview() == False and \
            self.token.is_list() == False and \
            self.token.is_range() == False and \
            self.token.is_bytes() == False and self.token.is_str() == False:
            return False 
        return True


    def is_list(self):
        if self.token[0] != '[' or self.token[-1] != ']':
            return False
        list_tokens = self.token[1:-1].split(',')
        for single_token in list_tokens:
            single_token_obj = Token(single_token)
            if single_token_obj.is_collection_element() == False:
                return False
        return True


    def is_tuple(self):
        if self.token[0] != '(' or self.token[-1] != ')':
            return False
        list_tokens = self.token[1:-1].split(',')
        for single_token in list_tokens:
            single_token_obj = Token(single_token)
            if single_token_obj.is_collection_element() == False:
                return False
        return True

    def is_range(self):
        if self.token.startswith("range(") and self.token.endswith(")"):
            return True
        return False
    #         if self.token.is_int() == True:


    def is_dict(self):
        if self.token[0]!='{' or self.token[-1]!='}':
            return False
        list_tokens = self.token[1:-1].split(',')
        for single_token in list_tokens:
            key, value = single_token.split(":")
            for pair_item in [key, value]:
                single_token_obj = Token(pair_item)
                if single_token_obj.is_collection_element() == False:
                    return False
        return True


    def is_set(self):
        if self.token[0]!='{' or self.token[-1]!='}':
            return False
        list_tokens = self.token[1:-1].split(',')
        for single_token in list_tokens:
            single_token_obj = Token(single_token)
            if single_token_obj.is_collection_element() == False:
                return False
        return True


    def is_frozenset(self):
        if self.token[0]!='(' or self.token[-1]!=')':
            return False

        if (self.token[1]!='(' and self.token[1]!='[' and self.token[1]!='{') \
            or (self.token[-2]!='(' and self.token[-2]!='[' and self.token[-2]!='{'):
            return False

        list_tokens = self.token[1:-1].split(',')
        for single_token in list_tokens:
            single_token_obj = Token(single_token)
            if single_token_obj.is_collection_element() == False:
                return False
        return True


    def is_bool(self):
        return self.token == "True" or self.token == "False"

    # def is_bytes(self):
    # def is_bytearray(self):
    # def is_memoryview(self):


    def is_comment(self):
        return self.is_single_line_comment() or self.is_multi_line_comment()

    def is_single_line_comment(self):
        return self.token[0]=='#'

    def is_multi_line_comment(self):
        return self.token.startswith('"""') and self.token.endswith("'''")

    def is_whitespace(self):
        return self.token[0] == ' '

    def is_operator(self):
        return self.token in self.OPERATORS

    def is_separator(self):
        return self.token == ',' or self.token == '[' or self.token == ']' \
            or self.token == '(' or self.token == ')' or self.token == ';' \


    # def is_error(self):
    # def is_invalid_token(self):

