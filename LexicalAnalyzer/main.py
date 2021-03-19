from LexicalAnalyzer import LexicalAnalyzer
from Token import Token
import glob
import sly
import re

PYTHON_FILENAME = "../LexicalAnalyzer/my_python_program.py"
FILENAME_LEN = -1
lexical_analyzer = LexicalAnalyzer(PYTHON_FILENAME)

FINAL_LEXICAL_LIST = []

lexical_parsing_matrix = []
lexical_parsing_list = []
parsed_items_list = []


PYTHON_TOKEN_TYPES_LIST = ["identifier", "keyword", "str", "int", "float",
                        "complex", "list", "tuple", "range", "dict", "set",
                        "frozenset", "bool", "bytes", "bytearray", "memoryview",
                        "comment", "whitespace", "operator", "separator",
                         "invalid_token", "lexical_error"]

PYTHON_TOKEN_TYPES_DICT = {"identifier":0, "keyword":1, "str":2, "int":3,
                           "float":4, "complex":5, "list":6, "tuple":7,
                           "range":8, "dict":9, "set":10, "frozenset":11,
                           "bool":12, "bytes":13, "bytearray":14,
                           "memoryview":15, "comment":16, "whitespace":17,
                           "operator":18, "separator":19,
                           "invalid_token":20, "lexical_error":21}


def trim_left_side_of_string(my_string):
    if "\'" in my_string:
        return my_string[my_string.find("\'"):my_string.rfind("\'")+1]
    elif "\"" in my_string:
        return my_string[my_string.find("\""):my_string.rfind("\"")+1]
    else:
        return my_string


def return_strings_from_source_code(source_code):
    found_strings_list = []
    pattern = re.compile(r'=[\s]*\"\"\".*\"\"\"')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        for i in range(s, e+1):
            if source_code[i]=='=' or source_code[i]==' ':
                continue
            else:
                break
        found_strings_list.append(
            (i,e,source_code[i:e]))

    pattern = re.compile(r'=[\s]*\'\'\'.*\'\'\'')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        for i in range(s, e+1):
            if source_code[i]=='=' or source_code[i]==' ':
                continue
            else:
                break
        found_strings_list.append(
            (i,e,source_code[i:e]))

    pattern = re.compile(r'=[\s]*\'.*\'')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        for i in range(s, e+1):
            if source_code[i]=='=' or source_code[i]==' ':
                continue
            else:
                break
        found_strings_list.append(
            (i,e,source_code[i:e]))

    pattern = re.compile(r'=[\s]*\".*\"')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        for i in range(s, e+1):
            if source_code[i]=='=' or source_code[i]==' ':
                continue
            else:
                break
        found_strings_list.append(
            (i,e,source_code[i:e]))
    return found_strings_list


def return_multiline_comments_from_source_code(source_code):
    # TO DO: fix first character different from '='
    found_comments_list = []
    pattern = re.compile(r'\"\"\"([\s\S]*)\"\"\"')
    order = 1
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        if lexical_parsing_list[s]!=-1:
            for i_idx in range(s, e+1):
                if lexical_parsing_list[i_idx]==-1 and source_code[i_idx] == '"':
                    s = i_idx
                    break
        if lexical_parsing_list[e]!=-1:
            for i_idx in range(e, s-1, -1):
                if lexical_parsing_list[i_idx]==-1 and source_code[i_idx] == '"':
                    e = i_idx
                    break
        found_comments_list.append(
            (s, e, source_code[s:e]))

    pattern = re.compile(r'\'\'\'([\s\S]*)\'\'\'')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        if lexical_parsing_list[s]!=-1:
            for i_idx in range(s, e+1):
                if lexical_parsing_list[i_idx]==-1 and source_code[i_idx] == "'":
                    s = i_idx
                    break
        if lexical_parsing_list[e]!=-1:
            for i_idx in range(e, s-1, -1):
                if lexical_parsing_list[i_idx]==-1 and source_code[i_idx] == "'":
                    e = i_idx
                    break
        found_comments_list.append(
            (s, e, source_code[s:e]))
    return found_comments_list


def return_singleline_comment_from_source_code(source_code):
    found_comments_list = []
    pattern = re.compile(r'#.*')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        found_comments_list.append(
            (s, e, source_code[s:e]))
    return found_comments_list


def actualize_lexical_parsing_list(current_tokens_list, token_index, source_code=""):
    global lexical_parsing_list, FILENAME_LEN
    if current_tokens_list:
        for current_token in current_tokens_list:
            for i_idx in range(current_token[0], min(FILENAME_LEN-1,current_token[1]+1)):
                if lexical_parsing_list[i_idx] == -1:
                    lexical_parsing_list[i_idx] = token_index


def print_lexical_parsing_list(lexical_parsing_matrix):
    global lexical_parsing_list
    file = open(PYTHON_FILENAME)
    source_code = file.read()
    token = ""
    if lexical_parsing_list[0] != -1:
        token = ""
    for i_idx in range(1, len(lexical_parsing_list)):
        if lexical_parsing_list[i_idx] == -1 or (i_idx>=1 and
                                             lexical_parsing_list[i_idx]
                                             !=lexical_parsing_list[i_idx-1]):
            if token != "":
                previous_token_code = lexical_parsing_list[i_idx-1]
                token_type = PYTHON_TOKEN_TYPES_LIST[previous_token_code]
                l, r = -1, -1
                if token[0] == ' ' or token[-1] == ' ':
                    for j_idx in range(0, len(token)):
                        if token[j_idx] != ' ':
                            l = j_idx
                            break
                    for j_idx in range(len(token) - 1, -1, -1):
                        if token[j_idx]!=' ':
                            r = j_idx
                            break
                offset = -1
                if token_type == 'identifier' and source_code[i_idx-1] in lexical_analyzer.SMALL_LETTERS:
                    token += source_code[i_idx-1]
                    offset = i_idx - 1

                if l == -1 and r == -1:
                    if offset == -1:
                        FINAL_LEXICAL_LIST.append([token.strip(), token_type, i_idx - len(token) - 1, i_idx - 2])
                    else:
                        FINAL_LEXICAL_LIST.append([token.strip(), token_type,
                                                   offset - len(token) + 1,
                                                   offset])
                elif l != -1 and r != -1:
                    FINAL_LEXICAL_LIST.append([token.strip(), token_type, i_idx - 1 - r, i_idx - 1 - r])
                elif l != -1 and r == -1:
                    FINAL_LEXICAL_LIST.append([token.strip(), token_type, i_idx - len(token.strip()) - 1, i_idx - 2])
                elif l == -1 and r != -1:
                    FINAL_LEXICAL_LIST.append([token.strip(), token_type, i_idx - 1 - len(token) , i_idx - 2 - len(token) + len(token.strip())])
                token = ""
            continue
        else:
            token_type =  PYTHON_TOKEN_TYPES_LIST[lexical_parsing_list[i_idx - 1]]
            if token_type == 'separator' and len(token)!=0:
                token = Token(token)
                token.determine_token_type()
                FINAL_LEXICAL_LIST.append([token.token.strip(), token.token_type, i_idx-2, i_idx-2])
                token = ""
            token += source_code[i_idx-1]


def return_functions_from_source_code(source_code):
    found_comments_list = []
    pattern = re.compile(r'[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?')
    for matched_pattern in re.finditer(pattern, source_code):
        s = matched_pattern.start()
        e = matched_pattern.end()
        first_paranthesis_index = s + source_code[s:e].find("(")

        found_comments_list.append(
            (s, first_paranthesis_index-1, source_code[s:first_paranthesis_index]))
    return found_comments_list


def return_identifiers_from_source_code(source_code):
    found_identifiers_list = []
    return found_identifiers_list


def interval_intersect(la, ra, lb, rb):
    if la <= ra and lb <= rb:
        if (la <= lb <= ra <= rb) or (lb <= la <= rb <= ra) or (la <= lb <= rb <= ra) or (lb <= la <= ra <= rb):
            return True
        else:
            return False
    else:
        return None

def return_keywords_from_source_code(source_code):
    global lexical_parsing_list
    found_keywords_list = []
    for token in lexical_analyzer.PYTHON_KEYWORDS_LIST:
        pattern = re.compile(token)
        for matched_pattern in re.finditer(pattern, source_code):
            s = matched_pattern.start()
            e = matched_pattern.end()
            if lexical_parsing_list[s] == -1 and lexical_parsing_list[e] == -1:
                has_intercalation = False
                for i_idx in range(len(found_keywords_list)):
                    left_idx, right_idx, _ = found_keywords_list[i_idx]
                    is_intersection = interval_intersect(left_idx, right_idx, s, e)
                    if is_intersection == True:
                        has_intercalation = True
                        break
                if len(found_keywords_list) == 0:
                    found_keywords_list.append((s, e , source_code[s:e]))
                elif has_intercalation == False:
                    found_keywords_list.append((s, e , source_code[s:e]))
    return found_keywords_list


def return_operators_from_source_code(source_code):
    global lexical_parsing_list
    found_operators_list = []
    for token in lexical_analyzer.OPERATORS:
        pattern = re.compile(token)
        for matched_pattern in re.finditer(pattern, source_code):
            s = matched_pattern.start()
            e = matched_pattern.end()

            # if 1 <= s <= e <= len(source_code) - 2:
            #     prev = source_code[s-1]
            #     end = source_code[e+1]
            #     first = source_code[s]
            #     last = source_code[e]
            #     if prev in lexical_analyzer.SMALL_LETTERS and end in lexical_analyzer.SMALL_LETTERS \
            #         and prev in lexical_analyzer.DIGITS and end in lexical_analyzer.DIGITS and \
            #         prev in lexical_analyzer.CAPITAL_LETTERS and end in lexical_analyzer.CAPITAL_LETTERS \
            #         and first in lexical_analyzer.SMALL_LETTERS and first in lexical_analyzer.SMALL_LETTERS \
            #         and last in lexical_analyzer.DIGITS and first in lexical_analyzer.DIGITS and \
            #         first in lexical_analyzer.CAPITAL_LETTERS and last in lexical_analyzer.CAPITAL_LETTERS:
            #         break
            if e >= len(source_code):
                break
            if s + 1 == e or s == e:
                if len(source_code[s:e]) == 0:
                    break
            if lexical_parsing_list[s] == -1 and lexical_parsing_list[e] == -1:
                has_intercalation = False
                for i_idx in range(len(found_operators_list)):
                    left_idx, right_idx, _ = found_operators_list[i_idx]
                    is_intersection = interval_intersect(left_idx, right_idx, s, e)
                    if is_intersection == True:
                        has_intercalation = True
                        break
                if len(found_operators_list) == 0:
                    found_operators_list.append((s, e , source_code[s:e]))
                elif has_intercalation == False:
                    found_operators_list.append((s, e , source_code[s:e]))
    return found_operators_list


def return_separators_from_source_code(source_code):
    global lexical_parsing_list
    found_separators_list = []
    for token in lexical_analyzer.SEPARATORS:
        if token == '(':
            pattern = re.compile(r'\(')
        elif token == ')':
            pattern = re.compile(r'\)')
        elif token == '[':
            pattern = re.compile(r'\[')
        elif token == ']':
            pattern = re.compile(r'\]')
        else:
            pattern = re.compile(token)
        for matched_pattern in re.finditer(pattern, source_code):
            s = matched_pattern.start()
            e = matched_pattern.end()
            if e >= len(source_code):
                break
            if lexical_parsing_list[s] == -1 and lexical_parsing_list[e] == -1:
                if source_code[s:e] in lexical_analyzer.SEPARATORS:
                    if source_code[s:e] == '.' and (source_code[s-1] in lexical_analyzer.DIGITS or source_code[e+1] in lexical_analyzer.DIGITS):
                        break
                    if source_code[s:e] in lexical_analyzer.SEPARATORS:
                        found_separators_list.append((s, e , source_code[s:e]))
    return found_separators_list


def return_errors_from_source_code(source_code, option):
    found_errors_list = []
    if option == "post_scan":
        # identifier = orice ce nu e keyword, comment, operator, separator
        if source_code.trim()[0] == '=':
            found_errors_list.append((0,0,source_code[0]))
        if source_code.trim()[-1] == '=':
            found_errors_list.append((len(source_code)-1, len(source_code)-1, source_code[len(source_code)-1]))

        for i_idx in range(1, len(source_code)-1):
            left_idx, right_idx = None, None
            if source_code[i_idx] == '=':
                for j_idx in range(i_idx - 1, -1, -1):
                    if lexical_parsing_list[j_idx] != -1:
                        if PYTHON_TOKEN_TYPES_DICT[lexical_parsing_list[j_idx]] != 'identifier':
                            left_idx = j_idx
                        break
                for j_idx in range(i_idx + 1, len(source_code)):
                    if lexical_parsing_list[j_idx] != -1:
                        if PYTHON_TOKEN_TYPES_DICT[lexical_parsing_list[j_idx]] in ['keyword', 'comment', 'operator', 'separator']:
                            right_idx = j_idx
                        break

            if left_idx and right_idx:
                found_errors_list.append((left_idx, right_idx, source_code[left_idx: right_idx + 1]))
            elif left_idx:
                found_errors_list.append((left_idx, i_idx, source_code[left_idx: i_idx + 1 ]))
            elif right_idx:
                found_errors_list.append((i_idx, right_idx, source_code[i_idx:right_idx + 1]))

    if option == "pre_scan":
        pattern = re.compile(r'\"\"\"')
        cnt = 0
        for matched_pattern in re.finditer(pattern, source_code):
            cnt += 1
            s = matched_pattern.start()
            e = matched_pattern.end()

        if cnt % 2 == 1:
            for matched_pattern in re.finditer(pattern, source_code):
                cnt -= 1
                s = matched_pattern.start()
                e = matched_pattern.end()
                if cnt == 0:
                    found_errors_list.append(
                        (s, e, source_code[s:e]))

        pattern = re.compile(r"\'\'\'")
        cnt = 0
        for matched_pattern in re.finditer(pattern, source_code):
            cnt += 1
            s = matched_pattern.start()
            e = matched_pattern.end()

        if cnt % 2 == 1:
            for matched_pattern in re.finditer(pattern, source_code):
                cnt -= 1
                s = matched_pattern.start()
                e = matched_pattern.end()
                if cnt == 0:
                    found_errors_list.append(
                        (s, e, source_code[s:e]))

        cnt = 0
        last_idx = 0
        idxs_list = []
        cntset = set()
        for i_idx in range(len(source_code)):
            cntset.add(cnt)
            if source_code[i_idx] == '(':
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == ')':
                cnt -= 1
                if cnt >= 0:
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append((last_idx, i_idx, source_code[last_idx:i_idx+1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)

        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
        cnt = 0
        idxs_list = []
        for i_idx in range(len(source_code)):
            if source_code[i_idx] == '[' and cnt >= 0:
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == ']':
                cnt -= 1
                if cnt >= 0:
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append(
                        (last_idx, i_idx, source_code[last_idx:i_idx + 1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)
        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
        cnt = 0
        idxs_list = []
        for i_idx in range(len(source_code)):
            if source_code[i_idx] == '"""' and cnt >= 0:
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == '"""':
                cnt -= 1
                if cnt >= 0:
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append(
                        (last_idx, i_idx, source_code[last_idx:i_idx + 1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)
        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
        cnt = 0
        idxs_list = []
        for i_idx in range(len(source_code)):
            if source_code[i_idx] == "'''" and cnt >= 0:
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == "'''":
                if cnt >= 0:
                    cnt -= 1
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append(
                        (last_idx, i_idx, source_code[last_idx:i_idx + 1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)
        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
        cnt = 0
        idxs_list = []
        for i_idx in range(len(source_code)):
            if source_code[i_idx] == '"' and cnt >= 0:
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == '"':
                cnt -= 1
                if cnt >= 0:
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append(
                        (last_idx, i_idx, source_code[last_idx:i_idx + 1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)
        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
        cnt = 0
        idxs_list = []
        for i_idx in range(len(source_code)):
            if source_code[i_idx] == "'" and cnt >= 0:
                cnt += 1
                last_idx = i_idx
                idxs_list.append(last_idx)
            if source_code[i_idx] == "'":
                cnt -= 1
                if cnt >= 0:
                    last_idx = i_idx
                    idxs_list.append(last_idx)
                else:
                    found_errors_list.append((i_idx, i_idx, source_code[last_idx: i_idx+1]))
                    last_idx = i_idx
                    idxs_list.append(last_idx)
        if cnt!=0 and len(idxs_list)>=2:
            found_errors_list.append(
                (idxs_list[-2], idxs_list[-1], source_code[idxs_list[-2]:idxs_list[-1]]))
    return found_errors_list


def add_bottom_border(PYTHON_FILENAME):
    file = open(PYTHON_FILENAME, 'a')
    file.write("\n\n")
    file.close()


def main():
    global lexical_parsing_list, lexical_parsing_matrix, lexical_analyzer
    row, col = 0, 0
    add_bottom_border(PYTHON_FILENAME)

    lines = open(PYTHON_FILENAME,"r")

    lexical_parsing_matrix = [[-1 for i in range(len(line))] for line in lines]

    file = open(PYTHON_FILENAME)
    source_code = file.read()
    global FILENAME_LEN
    FILENAME_LEN = len(source_code)
    lexical_parsing_list = [-1 for i in range(len(source_code))]

    found_errors_list = return_errors_from_source_code(source_code, option="pre_scan")

    actualize_lexical_parsing_list(found_errors_list,
                                   PYTHON_TOKEN_TYPES_DICT['lexical_error'])

    #  extract strings and comments
    found_strings_list = return_strings_from_source_code(source_code)
    actualize_lexical_parsing_list(found_strings_list,
                                   PYTHON_TOKEN_TYPES_DICT['str'])

    found_multiline_comments_list = return_multiline_comments_from_source_code(source_code)
    actualize_lexical_parsing_list(found_multiline_comments_list,
                                   PYTHON_TOKEN_TYPES_DICT['comment'])

    found_singleline_comments_list = return_singleline_comment_from_source_code(
        source_code)
    actualize_lexical_parsing_list(found_singleline_comments_list,
                                   PYTHON_TOKEN_TYPES_DICT['comment'])

    found_functions_list = return_functions_from_source_code(source_code)
    actualize_lexical_parsing_list(found_functions_list,
                                  PYTHON_TOKEN_TYPES_DICT['identifier'])

    found_separators_list = return_separators_from_source_code(source_code)
    actualize_lexical_parsing_list(found_separators_list,
                                   PYTHON_TOKEN_TYPES_DICT['separator'],
                                   source_code)

    found_keywords_list = return_keywords_from_source_code(source_code)
    actualize_lexical_parsing_list(found_keywords_list,
                                   PYTHON_TOKEN_TYPES_DICT['keyword'])

    found_operators_list = return_operators_from_source_code(source_code)

    actualize_lexical_parsing_list(found_operators_list, PYTHON_TOKEN_TYPES_DICT['operator'])

    found_identifiers_list = []
    lines = open(PYTHON_FILENAME, "r")

    row, col = 0, 0
    total_counter = 0
    first = -1
    for line in lines:
        alfanumeric_token = ""
        col = 0
        for ch in line:
            if lexical_parsing_list[total_counter] != -1:
                total_counter += 1
                first = total_counter
                alfanumeric_token = ""
                continue
            if ch in lexical_analyzer.SMALL_LETTERS or ch in \
                lexical_analyzer.CAPITAL_LETTERS or ch in \
                lexical_analyzer.DIGITS or ch == "_":
                if first == -1:
                    first = total_counter
                    alfanumeric_token = ""
                alfanumeric_token += ch
            else:
                if len(alfanumeric_token) != 0:
                    token = Token(alfanumeric_token)
                    token.determine_token_type()
                    actualize_lexical_parsing_list([(first, total_counter, alfanumeric_token)],
                                                   PYTHON_TOKEN_TYPES_DICT[
                                                       token.token_type])
                    found_identifiers_list.append((first, total_counter, alfanumeric_token))
                    first = -1
                alfanumeric_token = ""
            total_counter += 1
            col += 1
        row += 1
    found_identifiers_list = []
    lines = open(PYTHON_FILENAME, "r")
    row, col = 0, 0
    total_counter = 0
    first = -1
    for line in lines:
        alfanumeric_token = ""
        col = 0
        for ch in line:
            if lexical_parsing_list[total_counter] != -1:
                total_counter += 1
                continue
            if ch in lexical_analyzer.OPERATORS:
                if first == -1:
                    first = total_counter
                    alfanumeric_token = ""
                alfanumeric_token += ch
            else:
                if len(alfanumeric_token) != 0:
                    token = Token(alfanumeric_token.strip())
                    token.determine_token_type()
                    found_identifiers_list.append(
                        (first, total_counter, alfanumeric_token))
                    first = -1
                alfanumeric_token = ""
            total_counter += 1
            col += 1
        row += 1

    found_errors_list = return_errors_from_source_code(source_code,
                                                       option="pre_scan")

    actualize_lexical_parsing_list(found_errors_list,
                                   PYTHON_TOKEN_TYPES_DICT['lexical_error'])

    print_lexical_parsing_list(lexical_parsing_matrix)
    global FINAL_LEXICAL_LIST

    write_final_lexical_list()


def write_final_lexical_list():
    global FINAL_LEXICAL_LIST

    lines = open(PYTHON_FILENAME, "r")
    row, col = 0, 0
    total_chr_counter = 0

    for line in lines:
        col = 0
        for ch in line:
            for i_idx in range(len(FINAL_LEXICAL_LIST)):
                if FINAL_LEXICAL_LIST[i_idx][2] == total_chr_counter:
                    FINAL_LEXICAL_LIST[i_idx][2] = (row, col)
                if FINAL_LEXICAL_LIST[i_idx][3] == total_chr_counter:
                    FINAL_LEXICAL_LIST[i_idx][3] = (row, col)
            total_chr_counter += 1
            col += 1
        row += 1

    output_writer = open("lexical_analyzer_output.txt", "w")

    for i in range(len(FINAL_LEXICAL_LIST)):
        output_writer.write("Token: {" + FINAL_LEXICAL_LIST[i][0] + "}, ")
        output_writer.write("type: " + FINAL_LEXICAL_LIST[i][1] + ", ")
        output_writer.write("starting (col, row): " + str(FINAL_LEXICAL_LIST[i][2]) + "; ")
        output_writer.write("ending (col, row): " + str(FINAL_LEXICAL_LIST[i][3]) + "; ")
        output_writer.write("length of token: " + str(len(FINAL_LEXICAL_LIST[i][0])) + "\n")

if __name__ == "__main__":
    main()
