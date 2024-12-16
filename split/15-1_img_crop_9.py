import os
from tqdm import tqdm
import shutil
import json

num = 0

grade_num_mapping = {
    '초등_3': '01.초등학교',
    '초등_4': '02.초등학교',
    '초등_5': '03.초등학교',
    '초등_6': '04.초등학교',
    '중등_1': '06.중학교',
    '중등_2': '07.중학교',
    '중등_3': '08.중학교',
    '고등_1': '09.고등학교',
    '고등_2': '10.고등학교',
    '중등_공통학년': '05.중학교(공통)',
}

subject_num_mapping = {
    '국어': '01.국어',
    '영어': '02.영어',
    '수학': '03.수학',
    '사회': '04.사회',
    '과학': '05.과학',
    '정보': '06.정보',
    '기술가정': '07.기술가정',
    '도덕': '08.도덕',
    '사회문화': '09.사회문화',
}

# 파라미터로 받은 경로(폴더)가 없으면 만들어주는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 원천 학교별, 학년별 분리하는 함수
def img_find_grade(school_num, grade):
    grade_num = grade_num_mapping.get(school_num)

    if grade == '공통학년':
        path = grade_num+'\\'
    else:
        # ex) 06.중학교 1학년\\
        path = f'{grade_num} {grade}학년\\'

    return path

# 원천데이터(이미지파일) 경로
dir_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\img_crop\\2024-nia15-1-make-8"
img_path_list = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
# for (root, directories, files) in os.walk(dir_path):
#     for d in directories:
#         d_path = os.path.join(root, d)

#     for file in files:
#         file_path = os.path.join(root, file)
#         img_path_list.append(file_path)

# with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1_output_data_1216_3.json', 'r', encoding='utf-8') as f:
#     datas = json.loads(f.read())

# for data in tqdm(datas):

#     raw_data_info = data.get('raw_data_info')
#     source_data_info = data.get('source_data_info')

#     raw_data_name = raw_data_info.get('raw_data_name')

#     source_data_name = source_data_info.get('source_data_name')

#     # 원천데이터(이미지)파일명 ex)981d05df-243f-4e75-a27e-743e5d0cceff 과 raw_data_name을 비교해서 같을경우
#     # (원천데이터 파일명이 json파일에 있는 파일인 경우)
#     for img_path in img_path_list:
#         if img_path.split('\\')[-1][0:-4] == raw_data_name:

#             path_raw_name = f'{dir_path}\\{source_data_name}.png'

#             os.rename(img_path, path_raw_name)

# os.close

img_path_list = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list.append(file_path)

# S1_중등_1_영어_TXT_048685
for img_path in img_path_list:

    # print(img_path.split('_')[6])

    if img_path.split('_')[6] == 'text':
        type_check = '텍스트'

    # 그냥 갯수세기
    num += 1
    
    # 파일이 저장될 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\make_08\\'

    # C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\img_test\\S1_중등_1_영어_TXT_048685.png 에서
    # S1_중등_1_영어_TXT_048685만 가져옴
    img_source_name = img_path.split('\\')[-1]

    # _ 기준으로 split. ex)[S1, 중등, 1, 영어, TXT, 048685]
    img_source_name_split = img_source_name.split('_')

    # print(img_source_name_split)

    # 두번째와 세번째 인덱스만 가져옴. ex)중등_1
    school_num = f'{img_source_name_split[1]}_{img_source_name_split[2]}'

    # 학년. ex) 1
    grade = img_source_name_split[2]

    # 중등_1, 1 을 전달하면 -> 06.중학교 1학년 으로 리턴
    path += img_find_grade(school_num, grade)

    # 과목. ex)영어
    subject = subject_num_mapping.get(img_source_name_split[3])

    path += f'{subject}\\'
    
    # 텍스트와 이미지 분류해서 경로에 추가
    if img_source_name_split[4] == 'TXT':
        path += '01.텍스트\\'
    else:
        path += '02.이미지\\'

    # 해당 경로 폴더가 없으면 만드는 함수
    makedirs(path)

    # 최종 경로
    path += f'{img_source_name}'

    # 파일 옮기는 함수
    shutil.move(img_path, path)

print(num)