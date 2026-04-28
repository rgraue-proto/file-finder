import os
import datetime
from multiprocessing import Pool
from llm import query, tokenize
from pine import upsert_embeding

def iter_files(rel_path: str):
    for root, _, files in os.walk(rel_path):
        for name in files:
            yield os.path.abspath(os.path.join(root, name))

def load_file(abs_path: str):
    start = datetime.datetime.now()
    file_name = abs_path.split('/').pop(-1)
    try:
        prompt = f'Describe this file named {file_name} and its contents in one sentence:\n'

        with open(abs_path, 'r', encoding='utf-8') as file:
            for line in file:
                if not line.isascii():
                    raise Exception(f'non ascii file: {abs_path}')
                prompt += line

        summary = query(prompt)
        embedings = tokenize(summary)

        meta = {
            'abs_path': abs_path,
            'summary': summary,
        }

        # load into pinecone
        upsert_embeding(
            abs_path,
            embedings,
            meta
        )

        print(f'{datetime.datetime.now() - start} | finished indexing {abs_path}')
        return {
            'abs_path': abs_path,
            'summary': summary,
        }
    
    except Exception as e:
        print(f'{abs_path} - {str(e)}')
    
    


def load_folder(rel_path: str, verbose: bool):
    files = []
    for file_path in iter_files(rel_path):
        files.append(file_path)

    if (len(files) == 0):
        print('no files found')
        return

    print(f'loading {len(files)} files.')
    with Pool(min(len(files), 2)) as p:
        p.map(load_file, files)

    