import asyncio
import os
import re
from dotenv import load_dotenv
from openai import AsyncOpenAI
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LeanServer
import tqdm

from classes import ProgramFile

load_dotenv()
client = AsyncOpenAI()
print (f"openai key: {os.environ.get('OPENAI_API_KEY')}")


# def test_code (code: str) -> bool


async def translate_repo (repo_path: str) -> list[str]:
    # lconfig = LeanREPLConfig(verbose=True)
    # lserver = AutoLeanServer(lconfig, max_ )
    files = _extract_files(repo_path)
    prompt = _make_prompt (files)
    # print(prompt)
    messages = [
        {"role": "system", "content": "You are an expert at translating python programs to lean4"},
        {"role": "user", "content": prompt}
    ]
    result = (await client.chat.completions.create(
        messages = messages,
        model="gpt-4.1"
    )).choices[0].message.content or ""
    messages.append({"role": "assistant", "content": result})
    with open("0.txt", "w") as f:
        f.write(result)
    # for i in tqdm.tqdm(range(5)):
    #     code = _extract_code(result)
    #     res = test_code (code)
    #     if any([mess.severity == 'error' for mess in res.messages]):
    #         errors = [f"Line {mess.start_pos.line}: {mess.data}" for mess in res.messages]
    #         prompt = _make_error_prompt(errors)
    #         messages.append({"role": "user", "content": prompt})
    #         result = (await client.chat.completions.create(
    #             messages = messages,
    #             model="gpt-4.1"
    #         )).choices[0].message.content or ""
    #         with open(f"{i+1}.txt", "w") as f:
    #             f.write(result)
    #     else:
    #         break

    
    return _extract_code(result)

if __name__ == "__main__":
    asyncio.run(translate_repo("input_repos/mincut"))