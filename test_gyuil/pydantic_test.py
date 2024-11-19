import json
import os

from pydantic import BaseModel

# 파라미터로 받은 경로(폴더)가 없으면 만들어주는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 분리할 원본 json 파일 경로
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-1_output_data.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

for data in datas:

    # 파일 저장할 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-1_split_test\\'

    # 제목
    title = data.get('source_data_info').get('source_data_name')

    # 파일 형식
    file_type = '.json'

    # source_data_name ex) S1_중등_1_국어_TXT_000316
    grade = data.get('source_data_info').get('source_data_name')
    achievement_2009 = data.get('source_data_info').get('2009_achievement_standard')
    achievement_2015 = data.get('source_data_info').get('2015_achievement_standard')
    achievement_2022 = data.get('source_data_info').get('2022_achievement_standard')

    data_name = data.get('learning_data_info').get('learning_data_name')
    description = data.get('learning_data_info').get('text_description')
    qa = data.get('learning_data_info').get('text_qa')
    an = data.get('learning_data_info').get('text_an')


    id = data.get('raw_data_info').get('raw_data_name')
    publisher = data.get('raw_data_info').get('publisher')

    check = ''

    # 최소값과 최대값(1 ~ 255 or 999) 검사

    # raw_data_info
    # raw_data_name
    id_len_check = len(id) < 255 or len(id) > 1
    # publisher
    publisher_len_check = len(publisher) < 255 or len(publisher) > 1

    # learning_data_info
    # learning_data_name
    data_name_len_check = len(data_name) < 999 or len(data_name) > 1
    # text_description
    description_len_check = len(description) < 999 or len(description) > 1
    # text_qa
    qa_len_check = len(qa) < 999 or len(qa) > 1
    # text_an
    an_len_check = len(an) < 999 or len(an) > 1

    # source_data_info
    # 2009_achievement_standard
    achievement_2009_len_check = len(achievement_2009) < 999
    # 2015_achievement_standard
    achievement_2015_len_check = len(achievement_2015) < 999
    # 2022_achievement_standard
    achievement_2022_len_check = len(achievement_2022) < 999 or len(achievement_2022) > 1
    # source_data_name
    source_name_len_check = len(grade) < 255 or len(grade) > 1

    # 조건식중 하나라도 해당되지 않으면(유효성 검사 불통) 해당 인덱스는 사용하지 않음
    isNull = id_len_check or publisher_len_check or data_name_len_check or description_len_check \
                or qa_len_check or an_len_check or achievement_2009_len_check or achievement_2015_len_check \
                or achievement_2022_len_check or source_name_len_check

    # source_data_name 학년에 따라 path에 연결
    if '초등_3' in grade:
        path += '01.초등학교 3학년\\'
        
    elif '초등_4' in grade:
        path += '02.초등학교 4학년\\'
    
    elif '초등_5' in grade:
        path += '03.초등학교 5학년\\'

    elif '초등_6' in grade:
        path += '04.초등학교 6학년\\'

    elif '중등_1' in grade:
        path += '05.중학교 1학년\\'

    elif '중등_2' in grade:
        path += '06.중학교 2학년\\'

    elif '중등_3' in grade:
        path += '07.중학교 3학년\\'

    elif '고등_1' in grade:
        path += '08.고등학교 1학년\\'

    if isNull:
        # print('들어옴')
        # 폴더 없으면 만드는 함수
        makedirs(path)

        # json 파일 생성
        with open(path+title+file_type, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
