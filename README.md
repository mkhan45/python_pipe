# Python Pipe

Proof of concept for extending Python with a pipe operator in a really hacky way.

I wanted to leverage Python's ast module to run a workshop on compiler/interpreter basics,
but since Python's `ast.parse` is implemented in C and the helper functions aren't exported,
it's not a good option.

The general idea was to recreate helper functions like `parse_expr()`, `parse_block()`, `parse_stmt()`
etc. by using regexes to determine where a syntax construct ends, and then use `ast.parse()` to do
most of the hard work. Then, ideally we could add snytax sugar without too much extra code.
This approach could work but it's not very representative of how writing parsers
actually goes so I'm abandoning it.

## Example

```python
code = \
"""\
f = lambda x: x * 2
r = 2 |> f
print(r)
"""

parsed = parse(code)
bytecode = compile(parsed, "", "exec")
exec(bytecode) # 4
```

The code
```
f = lambda x: x * 2
r = 2 |> f
print(r)
```

gets transformed into:

```
f = lambda x: x * 2
r = f(2)
print(r)
```
