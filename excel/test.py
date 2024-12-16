import json
import os, sys
import pandas as pd
from tqdm import tqdm

json_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\최종_23만개_output.json'
save_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\excel\\'

raw_data_name = []
source_data_name = []
school_data_name = []
grade_data_name = []
subject_data_name = []
class_name = []

# 경로 없으면 만드는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# json 파일 불러오는 함수
def road_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        datas = json.loads(f.read())
    return datas

# # 유효성 검사 함수 
# def condition_check(data):

#     raw_data_info = data.get('raw_data_info')
#     source_data_info = data.get('source_data_info')
#     learning_data_info = data.get('learning_data_info')

#     id = raw_data_info.get('raw_data_name')
#     publisher = raw_data_info.get('publisher')

#     source_name = source_data_info.get('source_data_name')
#     achievement_2009 = source_data_info.get('2009_achievement_standard')
#     achievement_2015 = source_data_info.get('2015_achievement_standard')
#     achievement_2022 = source_data_info.get('2022_achievement_standard')

#     data_name = learning_data_info.get('learning_data_name')
#     description = learning_data_info.get('text_description')
#     qa = learning_data_info.get('text_qa')
#     an = learning_data_info.get('text_an')
#     class_name = learning_data_info.get('class_name')

#     # 최소값과 최대값(1 ~ 255 or 999) 검사
#     # raw_data_info
#     # raw_data_name (1~255)
#     id_len_check = 1 <= len(id) <= 255
#     # publisher (1~255)
#     publisher_len_check = 1 <= len(publisher) <= 255

#     # learning_data_info
#     # learning_data_name (1~999)
#     data_name_len_check = 1 <= len(data_name) <= 999
#     # text_description (1~999)
#     description_len_check = 1 <= len(description)
#     # text_qa (1~999)
#     qa_len_check = 1 <= len(qa)
#     # text_an (1~999)
#     an_len_check = 1 <= len(an)
#     # 문장_noChange 제외
#     class_name_check = not class_name == '문장_noChange'

#     # source_data_info
#     # 2009_achievement_standard (999자 이하, null 허용이기 때문)
#     achievement_2009_len_check = len(achievement_2009) <= 999
#     # 2015_achievement_standard (999자 이하, null 허용이기 때문)
#     achievement_2015_len_check = len(achievement_2015) <= 999
#     # 2022_achievement_standard (1~999)
#     achievement_2022_len_check = 1 <= len(achievement_2022) <= 999
#     # source_data_name (1~255)
#     source_name_len_check = 1 <= len(source_name) <= 255

#     # 조건식중 하나라도 해당되지 않으면(유효성 검사 불통이면) 해당 인덱스는 사용하지 않음
#     condition = id_len_check and publisher_len_check and data_name_len_check and description_len_check \
#                and qa_len_check and an_len_check and achievement_2009_len_check and achievement_2015_len_check \
#                and achievement_2022_len_check and source_name_len_check and class_name_check
    
#     return condition

# 데이터를 list에 담아줌
def data_append(data):
    raw_data_info = data.get('raw_data_info')
    source_data_info = data.get('source_data_info')
    learning_data_info = data.get('learning_data_info')

    raw_data_name.append(raw_data_info.get('raw_data_name'))
    school_data_name.append(raw_data_info.get('school'))
    grade_data_name.append(raw_data_info.get('grade'))
    subject_data_name.append(raw_data_info.get('subject'))
    source_data_name.append(source_data_info.get('source_data_name'))
    class_name.append(learning_data_info.get('class_name'))


datas = road_json(json_path)

for data in tqdm(datas):
    # condition = condition_check(data)

    # 유효성검사에 통과했을 때
    # if condition:
    data_append(data)

# print(type(raw_data_name))

appended_data = {
    'raw_data_name': raw_data_name,
    'school_data_name': school_data_name,
    'grade_data_name': grade_data_name,
    'subject_data_name': subject_data_name,
    'source_data_name': source_data_name,
    'class_name': class_name
}

df = pd.DataFrame(appended_data)
print(df.info())

df.to_excel(save_path+'15-1_test2.xlsx', index=False)