import os
import json
from tqdm import tqdm

dir_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\문단\\07.중학교 2학년\\06.정보"
img_path_list = []

for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)
        # print(d_path)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list.append(file_path)

for path in img_path_list:
    new_path = path.replace('_2_', '_공통_')

    os.rename(path, new_path)

