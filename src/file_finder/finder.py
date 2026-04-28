from llm import tokenize
from pine import query_index
import datetime

def find_files(prompt: str, verbose: bool, confidence: float):
    start = datetime.datetime.now()
    vectors = tokenize(prompt)
    matches = query_index(vectors).matches

    confidence = .38 if confidence is None else confidence
    matches = list(filter(lambda m: m['score'] >= confidence or prompt in m['metadata']['abs_path'], matches))
    
    print(f'\n{datetime.datetime.now() - start} | Found {len(matches)} files matching criteria:')
    for match in matches:
        print(f'   {match['metadata']['abs_path']}')
        if verbose is True:
            print(f'      |{round(match['score'], 2)} summary: ${match['metadata']['summary']}')