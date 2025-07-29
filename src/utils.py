import re
from classes import ProgramFile
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LeanServer
from lean_interact.server import LeanError


def extract_code (response: str) -> list[str]:
    codes = list(map(lambda x: x.replace('```lean4', '').replace('```lean', '').replace('```',''), re.findall(r'(?s)```.*?```', response)))
    return codes


def extract_files (repo_path: str) -> list[ProgramFile]:
    with open("/Users/tkasriel/verified_codegen_testing/verified_codegen_testing/input_repos/mincut/mincut.py", "r") as f:
        return [ProgramFile(name="mincut.py",
                        code="\n".join(f.readlines()))]

def test_code (code: str):
    cfg = LeanREPLConfig()
    server = LeanServer(cfg)
    res = server.run(Command(cmd=code))
    if isinstance(res, LeanError):
        raise Exception(res.model_dump_json)
    return res

def make_prompt (files: list[ProgramFile]) -> str:
    prompt = f"""
Generate me Lean 4.21.0 code that mimics the functionality of this python program. Of particular note:
- Be well-documented with comments if necessary
- Follow Lean 4 best practices and use appropriate Lean 4 syntax and features
- DO NOT use Lean 3 syntax or features
- DO NOT import Std or Init
- DO NOT use partial def. I want to verify this code later (do not generate a spec or proof), and therefore need everything unfoldable
Hint:
- Use a[i]! instead of a[i] when a is an array or a list when necessary

And MOST IMPORTANTLY
Python is an imperative language, whereas lean is functional. So you shouldn't focus on trying to mimic the code line by line, but rather mimic the same behavior the function would have. The code should look similar to other code written in a functional programming language
Make sure the signature stays the same. A function called like the following in python:
```py
def my_function (x : int, y : int, z : int):
    ...
```
becomes
```lean4
def my_function (x: Nat) (y : Nat) (z : Nat) :=
    ...
```
(Assuming that it'd be reasonable for x,y,z to be Nat's instead of Int's)
```py
# {files[0].name}
{files[0].code}
```
"""
    return prompt

def make_error_prompt (errors: list[str]) -> str:
    prompt = f"""I got the following errors. Please fix them:
{'\n'.join(errors)}
"""
    return prompt