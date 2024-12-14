import os
import json
from tqdm import tqdm
import shutil

dir_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\img_test"

with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data_new\\15-1_output_data_new.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

img_path_list = []

num = 0

for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list.append(file_path)
        # print(file_path)

        num += 1

        shutil.move(file_path, 'C:\\Users\\admin\\Desktop\\test\\')

        # os.rename(file_path, (f'{dir_path}\\test{num}.png'))