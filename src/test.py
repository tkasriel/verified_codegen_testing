import tqdm
from models import *
from main import LeanTranslator
import asyncio
import os

async def run_on_folder (folder_path: str) -> None:
    model = GPT4o()
    lt = LeanTranslator(model=model)
    input_files = os.listdir(INPUT_FOLDER)
    await asyncio.gather(*[handle_file(os.path.join(INPUT_FOLDER, input_file), tqdm.tqdm(total=11, position=i), lt) for i, input_file in enumerate(input_files)])

async def handle_file (filepath: str, progress_bar: tqdm.tqdm, lt: LeanTranslator):
    code = await lt.translate_file(filepath, progress_bar)
    filename = os.path.basename(filepath)
    output_folder = "outputs_2"
    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, f"{filename[:-3]}.lean"), "w") as f:
        f.write(code)


if __name__ == "__main__": 
    
    INPUT_FOLDER = "input_repos/single_files"
    model = GPT4o()
    lt = LeanTranslator(model=model)
    loop = asyncio.get_event_loop()

    input_files = os.listdir(INPUT_FOLDER)
    results = loop.run_until_complete(asyncio.gather(*[handle_file(os.path.join(INPUT_FOLDER, input_file), tqdm.tqdm(total=11, position=i), lt) for i, input_file in enumerate(input_files)]))

    # asyncio.run(lt.translate_file("input_repos/mincut/mincut.py"))
