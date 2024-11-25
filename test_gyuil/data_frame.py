import json
import os, sys
import pandas as pd
from tqdm import tqdm

json_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data_new\\15-1_output_data_new.json'
save_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\excel\\'

raw_data_name = []
date = []
publisher = []
publication_year = []
school = []
grade = []
semester = []
revision_year = []

source_data_name = []
achievement_standard_2009 = []
achievement_standard_2015 = []
achievement_standard_2022 = []

learning_data_name = []
class_num = []
class_name = []
bounding_box = []
text_description = []
text_qa = []
text_an = []

# 경로 없으면 만드는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# json 파일 불러오는 함수
def road_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        datas = json.loads(f.read())
    return datas


# 데이터를 list에 담아줌
def data_append(data):
    raw_data_info = data.get('raw_data_info')
    source_data_info = data.get('source_data_info')
    learning_data_info = data.get('learning_data_info')

    raw_data_name.append(raw_data_info.get('raw_data_name'))
    date.append(raw_data_info.get('date'))
    publisher.append(raw_data_info.get('publisher'))
    publication_year.append(raw_data_info.get('publication_year'))
    school.append(raw_data_info.get('school'))
    grade.append(raw_data_info.get('grade'))
    semester.append(raw_data_info.get('semester'))
    revision_year.append(raw_data_info.get('revision_year'))

    source_data_name.append(source_data_info.get('source_data_name'))
    achievement_standard_2009.append(source_data_info.get('2009_achievement_standard'))
    achievement_standard_2015.append(source_data_info.get('2015_achievement_standard'))
    achievement_standard_2022.append(source_data_info.get('2022_achievement_standard'))

    learning_data_name.append(learning_data_info.get('learning_data_name'))
    class_num.append(learning_data_info.get('class_num'))
    class_name.append(learning_data_info.get('class_name'))
    bounding_box.append(learning_data_info.get('bounding_box'))
    text_description.append(learning_data_info.get('text_description'))
    text_qa.append(learning_data_info.get('text_qa'))
    text_an.append(learning_data_info.get('text_an'))


datas = road_json(json_path)

for data in tqdm(datas):
    data_append(data)


appended_data = {
    'raw_data_name': raw_data_name,
    'date': date,
    'publisher': publisher,
    'publication_year': publication_year,
    'school': school,
    'grade': grade,
    'semester': semester,
    'revision_year': revision_year,

    'source_data_name': source_data_name,
    '2009_achievement_standard': achievement_standard_2009,
    '2015_achievement_standard': achievement_standard_2015,
    '2022_achievement_standard': achievement_standard_2022,

    'learning_data_name': learning_data_name,
    'class_num': class_num,
    'class_name': class_name,
    'bounding_box': bounding_box,
    'text_description': text_description,
    'text_qa': text_qa,
    'text_an': text_an
}

df = pd.DataFrame(appended_data)
print(df.info())

print(df.isna().sum())
