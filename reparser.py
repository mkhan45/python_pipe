import tokenize as tk
import regex as re
import ast

def tokenize(s):
    line_gen = (line for line in s.split('\n'))
    tokens = tk.generate_tokens(lambda: next(line_gen))
    return [*tokens]

def parse_expr(code):
    # TODO: gotta figure out
    exprr = "[^\\n]+"
    match re.search(exprr, code):
        case None:
            return None
        case match:
            matched_str = match[0]
            if "|>" in matched_str:
                [lhs, rhs] = matched_str.split('|>', 1)
                parsed_lhs = parse_expr(lhs)
                parsed_rhs = parse_expr(rhs)
                return ast.Call(parsed_rhs, [parsed_lhs], keywords=[])
            else:
                return ast.parse(matched_str.strip()).body[0].value

def parse_toplevel(code):
    assignr = "^.+=.+" # catches modifying assignments too
    if (match := re.search(assignr, code)) is not None:
        matched_str = match[0]
        rest = code[len(matched_str):]

        [lhs, rhs] = matched_str.split('=')
        parsed_rhs = parse_expr(rhs)
        # print(f"{rhs=}, {parsed_rhs=}")

        dummy_rhs = "None"
        dummy_ast = ast.parse(f"{lhs} = {dummy_rhs}").body[0]
        # print(f"{parsed_rhs=}")
        # print(f"before: {ast.dump(dummy_ast)}")
        dummy_ast.value = parsed_rhs
        final_ast = dummy_ast
        # print(f"after: {ast.dump(dummy_ast)}")

        return (final_ast, rest)

    returnr = "^return\s.+"
    if (match := re.search(returnr, code)) is not None:
        matched_str = match[0]
        rest = code[len(matched_str):]

        rhs = matched_str[len("return"):].strip()
        parsed_rhs = parse_expr(rhs)

        final_ast = ast.Return(parsed_rhs)

        return (final_ast, rest)

    exprr = "^.+"
    if (match := re.search(exprr, code)) is not None:
        matched_str = match[0]
        rest = code[len(matched_str):]

        return (ast.Expr(parse_expr(matched_str)), rest)

def parse(code):
    result, rest = [], code.strip()
    while rest != "":
        parse_res = parse_toplevel(rest)
        if parse_res is None:
            break

        expr, rest = parse_toplevel(rest)
        rest = rest.strip()
        result.append(expr)

    return ast.fix_missing_locations(ast.Module(body=result, type_ignores=[]))

code = \
"""\
f = lambda x: x * 2
r = 2 |> f
print(r)
"""

parsed = parse(code)
print(parsed)
print(ast.dump(parsed))
print(ast.unparse(parsed))
bytecode = compile(parsed, "", "exec")
exec(bytecode)
