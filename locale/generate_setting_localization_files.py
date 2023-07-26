# https://github.com/ovo-Tim/qt-json-setting/blob/main/generate_localization_files.py

import argparse
import ujson as json

def findAll(target, dictData, notFound=[]) -> list:
    queue = [dictData]
    result = []
    while len(queue) > 0:
        data = queue.pop()
        for key, value in data.items():
            if key == target: result.append(value)
            elif type(value) == dict: queue.append(value)
    if not result: result = notFound
    return result

parser = argparse.ArgumentParser(description="Generate internationalization files for JSON-schema")
parser.add_argument('path', type=str, help="schema 路径")
parser.add_argument('output_path', type=str, help="输出位置")
args = parser.parse_args()

with open(args.path) as f:
    json_file = json.decode(f.read())

translate_list = []
translate_list += findAll('title', json_file)
translate_list += findAll('description', json_file)

with open(args.output_path, 'a') as f:
    for i in translate_list:
        f.write("\n")
        f.write(f'''msgid "{i}" \n''')
        f.write('''msgstr "" \n''')