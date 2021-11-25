from pymongo import MongoClient
import gzip
from tqdm import tqdm
import json

from _utils import Example


def connect_db():
    client = MongoClient('172.29.7.226', 27017, username='admin', password='123456')
    db = client.code_search_net
    return db


def insert_doc_from_txt(collection, file_path):
    with gzip.open(file_path, 'rt') as f:
        for index, line in tqdm(enumerate(f.readlines()), 'insert to db.'):
            code_json = json.loads(line)

            code_data = {
                'code_index': index,
                'repo': code_json['repo'],
                'path': code_json['path'],
                'func_name': code_json['func_name'],
                'original_string': code_json['original_string'],
                'code_tokens': code_json['code_tokens'],
                'docstring': code_json['docstring'],
                'docstring_tokens': code_json['docstring_tokens'],
                'url': code_json['url'],
                'sha': code_json['sha'],
                'partition': code_json['partition'],
                'lang': 'go'
            }

            collection.insert_one(code_data)


# read data from db
def find_all_by_tag(collection, tag):
    return collection.find({'partition': tag})


def read_summarize_examples_from_db(collection, split_tag, lang, data_num):
    """Read examples from mongodb with conditions."""
    print('load data from db.')
    return_items = {'code_index': 1, 'code_tokens': 1, 'docstring_tokens': 1, '_id': 0}
    conditions = {'partition': split_tag, 'lang': lang}

    examples = []
    results = collection.find(conditions, return_items)
    for result in tqdm(results):
        idx = result['code_index']
        code = ' '.join(result['code_tokens']).replace('\n', ' ')
        code = ' '.join(code.strip().split())
        nl = ' '.join(result['docstring_tokens']).replace('\n', '')
        nl = ' '.join(nl.strip().split())
        examples.append(
            Example(
                idx=idx,
                source=code,
                target=nl,
            )
        )
        if idx + 1 == data_num:
            break
    return examples


# if __name__ == '__main__':
#     codes = connect_db().codes
#     # insert_doc_from_txt(codes, '/home/tangze/test_dfg.jsonl.gz')
#     results = find_all_by_tag(codes, 'train')
#     code_tokens = []
#     nl_tokens = []
#
#     for r in tqdm(results):
#         code_tokens.append(' '.join(r['code_tokens']))
#         nl_tokens.append(' '.join(r['docstring_tokens']))
#
#     with open('./train_code.txt', 'w') as f:
#         for code_token in code_tokens:
#             f.write(code_token+'\n')
#
#     with open('./train_doc.txt', 'w') as f:
#         for nl in nl_tokens:
#             f.write(nl + '\n')




