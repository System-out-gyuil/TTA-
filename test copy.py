import os
import random
import shutil
import json

img_path_list = []
json_list = []

# # 원천데이터(이미지파일) 경로
# dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천"

# # 경로에 아래에 있는 있는 모든 파일 가져오기
# for (root, directories, files) in os.walk(dir_path):
#     for d in directories:
#         d_path = os.path.join(root, d)

#     for file in files:
#         if 'IMG' in file:
#             file_path = os.path.join(root, file)
#             img_path_list.append(file_path)

# # 원천데이터(이미지파일) 경로
# dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천-1"

# # 경로에 아래에 있는 있는 모든 파일 가져오기
# for (root, directories, files) in os.walk(dir_path):
#     for d in directories:
#         d_path = os.path.join(root, d)

#     for file in files:
#         if 'IMG' in file:
#             file_path = os.path.join(root, file)
#             img_path_list.append(file_path)

# 원천데이터(이미지파일) 경로
dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천-2"

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        if 'png' in file and 'IMG' in file:
            file_path = os.path.join(root, file)
            img_path_list.append(file_path)

# # 원천데이터(이미지파일) 경로
# dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\split"

# # 경로에 아래에 있는 있는 모든 파일 가져오기
# for (root, directories, files) in os.walk(dir_path):
#     for d in directories:
#         d_path = os.path.join(root, d)

#     for file in files:
#         if 'IMG' in file:
#             file_path = os.path.join(root, file)
#             img_path_list.append(file_path)

with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1_output_data_1216_4.json", "r", encoding="utf-8") as f:
    datas = json.loads(f.read())

# IMG데이터만 모아진 list에서 랜덤으로 하나를 선택해서 리턴
from_file_path = random.choice(img_path_list)
to_file_path = 123

# shutil.copyfile(from_file_path, to_file_path) 

ran_list = []
for i in range(10):
    ran_list.append(random.choice(img_path_list))

# S1_중등_3_수학_IMG_149391
# splited_path = from_file_path.split('\\')[-1].split('.')[0]
# print(splited_path)

for data in datas:
    source_data_name = data.get('source_data_info').get('source_data_name')

    for ran_path in ran_list:
        splited_path = ran_path.split('\\')[-1].split('.')[0]

        if splited_path == source_data_name:
            json_list.append(data)

ran_ments1 = [
    '이 이미지는',
    '해당 이미지는'
]

for file in json_list:
    class_name = data.get('learning_data_info').get('class_name')
     
    if class_name == "이미지(기타)":

        text_description = f'{random.choice(ran_ments1)} {file.get('learning_data_info').get('text_description')}'

    elif class_name == "이미지(수식)":
        text_description = f'{random.choice(ran_ments)} {file.get('learning_data_info').get('text_description')}'
    
    print(text_description)