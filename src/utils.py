from classes import ProgramFile


def extract_code (response: str) -> list[str]:
    codes = list(map(lambda x: x.replace('```',''), re.findall(r'(?s)```.*?```', response)))
    return codes


def extract_files (repo_path: str) -> list[ProgramFile]:
    with open("/Users/tkasriel/verified_codegen_testing/verified_codegen_testing/input_repos/mincut/mincut.py", "r") as f:
        return [ProgramFile(name="mincut.py",
                        code="\n".join(f.readlines()))]

def make_prompt (files: list[ProgramFile]) -> str:
    prompt = f"""You are an expert in Coq programming and theorem proving.
Please translate the following python program into Coq.
The program should:
- Be well-documented with comments if necessary
- Follow Coq best practices and use appropriate Coq syntax and features
```py
# mincut.py
{files[0].code}
```
"""
    return prompt

def _make_error_prompt (errors: list[str]) -> str:
    prompt = f"""I got the following errors. Please fix them:
{'\n'.join(errors)}
"""
    return prompt
