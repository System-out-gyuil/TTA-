import json
import os
from tqdm import tqdm

# json파일 경로
with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\difinition_make\\2024-nia15-1-make-5_1216.json", "r", encoding="utf-8") as f:
    makes = json.loads(f.read())

# 원천데이터(이미지파일) 경로
dir_path = f"D:\\제출용\\문단\\2024-nia15-1-make-5"
img_path_list = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        # C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\img_crop\\2024-nia15-1-make-1\\국어_고등학교_1학년_text_13145_32_png_00.png
        file_path = os.path.join(root, file)
        img_path_list.append(file_path)

for path in tqdm(img_path_list):
    img_path = path.split('\\')[-1]
    img_name = img_path.split('.')[0]

    for make in makes:
        if make.get('raw_data_info').get('raw_data_name') == img_name:
            os.rename(path, f'{dir_path}\\{make.get('source_data_info').get('source_data_name')}.png')

            