from dotenv import load_dotenv
from openai import AsyncOpenAI

from classes import ProgramFile
load_dotenv()
client = AsyncOpenAI()

def _extract_files (repo_path: str) -> list[ProgramFile]:
    with open("/Users/tkasriel/verified_codegen_testing/verified_codegen_testing/input_repos/mincut/mincut.py", "r") as f:
        return [ProgramFile(name="mincut.py",
                        code="\n".join(f.readlines()))]

def _make_prompt (files: list[ProgramFile]) -> str:
    prompt = f"""Below is a Python repository, with several files together building necessary features related to the stack data structure. Translate the entire codebase into Lean4, sticking to best coding practices. Output your answer code directly organized by files
    ```py
    # mincut.py
    {files[0].code}
    ```
"""
    return prompt

async def translate_repo (repo_path: str) -> list[ProgramFile]:
    files = _extract_files(repo_path)
    prompt = _make_prompt (files)
    messages = [
        {"role": "system", "content": "You are an expert at translating python programs to lean4"},
        {"role": "user", "content": prompt}
    ]
    result = await client.chat.completions.create(
        messages = messages,
        model="gpt-4.1"
    )
    with open("out.txt", "w") as f:
        f.write(result.choices[0].message.content or "")
    return []
