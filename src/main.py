
import os
from classes import ProgramFile
from models.base_model import Model
from utils import extract_code, make_prompt


class LeanTranslator:
    def __init__(self, model: type[Model]):
        self.model = model
        self.log_folder = "logs/"
        os.makedirs(self.log_folder, exist_ok=True)
    async def translate_file (self, filepath: str) -> str:
        with open (filepath, "r") as f:
            file = ProgramFile(name=os.path.basename(filepath),
                               code="\n".join(f.readlines()))
        prompt = make_prompt ([file])
        result = await self.model.send (prompt)
        with open (os.path.join(self.log_folder, "result.txt"), "w") as f:
            f.write(result)
        code = extract_code(result)[-1]
        with open(os.path.join(self.log_folder, "result.v"), 'w') as f:
            f.write(code)
        return code


    # async def translate_repo (repo_path: str) -> list[str]:
    # # lconfig = LeanREPLConfig(verbose=True)
    # # lserver = AutoLeanServer(lconfig, max_ )
    # files = _extract_files(repo_path)
    # prompt = _make_prompt (files)
    # # print(prompt)
    # messages = [
    #     {"role": "system", "content": "You are an expert at translating python programs to lean4"},
    #     {"role": "user", "content": prompt}
    # ]
    # result = (await client.chat.completions.create(
    #     messages = messages,
    #     model="gpt-4.1"
    # )).choices[0].message.content or ""
    # messages.append({"role": "assistant", "content": result})
    # with open("0.txt", "w") as f:
    #     f.write(result)
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

    
    # return _extract_code(result)

if __name__ == "__main__": 
    from models.qwen import Qwen
    import asyncio
    qwen = Qwen()
    lt = LeanTranslator(model=Qwen)
    asyncio.run(lt.translate_file("input_repos/mincut/mincut.py"))
