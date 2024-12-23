import os
import json
from tqdm import tqdm

dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\2차 저작_라벨링"
img_path_list = []
json_list = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        if 'json' in file_path:
            img_path_list.append(file_path)

        
for json_path in tqdm(img_path_list):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    json_list.append(data)

with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\추가 생성분.json", 'w', encoding='utf-8') as f:
    json.dump(json_list, f, indent=4, ensure_ascii=False)

print(len(json_list))