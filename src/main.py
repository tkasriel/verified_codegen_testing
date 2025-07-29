
import os

import tqdm
from classes import ProgramFile
from models.base_model import Model
from utils import extract_code, make_error_prompt, make_prompt, test_code
from dotenv import load_dotenv
load_dotenv()


class LeanTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.log_folder = "logs/"
        os.makedirs(self.log_folder, exist_ok=True)
    async def translate_file (self, filepath: str, progress_bar: tqdm.tqdm) -> str:
        with open (filepath, "r") as f:
            file = ProgramFile(name=os.path.basename(filepath),
                               code="\n".join(f.readlines()))
        local_log_folder= os.path.join(self.log_folder, file.name[:-3])
        os.makedirs(local_log_folder, exist_ok=True)
        
        prompt = make_prompt ([file])
        result = await self.model.send (prompt)
        with open (os.path.join(local_log_folder, "result.txt"), "w") as f:
            f.write(result)
        code = extract_code(result)[-1]
        with open(os.path.join(local_log_folder, "result.lean"), 'w') as f:
            f.write(code)
        progress_bar.update()
        for i in range(10):
            code = extract_code(result)[-1]
            res = test_code (code)
            if any([mess.severity == 'error' for mess in res.messages]):
                errors = [f"Line {mess.start_pos.line}: {mess.data}" for mess in res.messages if mess.severity == "error"]
                prompt = make_error_prompt(errors)
                result = await self.model.send(prompt)
                with open(os.path.join(local_log_folder, f"{i+1}.txt"), "w") as f:
                    f.write(result)
                with open(os.path.join(local_log_folder, f"{i+1}.lean"), "w") as f:
                    f.write(extract_code(result)[-1])
            else:
                progress_bar.close()
                return code
            progress_bar.update()
        progress_bar.close()
        return "no code generated"


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

