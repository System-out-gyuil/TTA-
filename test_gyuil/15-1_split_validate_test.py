import json
import os
from tqdm import tqdm

num = 0
failed_num = 0
nochange_num = 0

# 파라미터로 받은 경로(폴더)가 없으면 만들어주는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 분리할 원본 json 파일 경로
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-1_output_data_test_new_4.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

for data in tqdm(datas):

    # 파일 저장할 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-1_split_test\\'

    # 제목
    title = data.get('source_data_info').get('source_data_name')

    # 파일 형식
    file_type = '.json'

    raw_data_info = data.get('raw_data_info')

    id = raw_data_info.get('raw_data_name')
    publisher = raw_data_info.get('publisher')


    source_data_info = data.get('source_data_info')

    grade = source_data_info.get('source_data_name')
    achievement_2009 = source_data_info.get('2009_achievement_standard')
    achievement_2015 = source_data_info.get('2015_achievement_standard')
    achievement_2022 = source_data_info.get('2022_achievement_standard')


    learning_data_info = data.get('learning_data_info')

    data_name = learning_data_info.get('learning_data_name')
    description = learning_data_info.get('text_description')
    qa = learning_data_info.get('text_qa')
    an = learning_data_info.get('text_an')
    class_name = learning_data_info.get('class_name')


    # 최소값과 최대값(1 ~ 255 or 999) 검사
    # raw_data_info
    # raw_data_name (1~255)
    id_len_check = 1 <= len(id) <= 255
    # publisher (1~255)
    publisher_len_check = 1 <= len(publisher) <= 255

    # learning_data_info
    # learning_data_name (1~999)
    data_name_len_check = 1 <= len(data_name) <= 999
    # text_description (1~999)
    description_len_check = 1 <= len(description) <= 999
    # text_qa (1~999)
    qa_len_check = 1 <= len(qa) <= 999
    # text_an (1~999)
    an_len_check = 1 <= len(an) <= 999
    # 문장_noChange 제거
    class_name_check = not class_name == '문장_noChange'

    # source_data_info
    # 2009_achievement_standard (999자 이하, null 허용이기 때문)
    achievement_2009_len_check = len(achievement_2009) <= 999
    # 2015_achievement_standard (999자 이하, null 허용이기 때문)
    achievement_2015_len_check = len(achievement_2015) <= 999
    # 2022_achievement_standard (1~999)
    achievement_2022_len_check = 1 <= len(achievement_2022) <= 999
    # source_data_name (1~255)
    source_name_len_check = 1 <= len(grade) <= 255

    # 조건식중 하나라도 해당되지 않으면(유효성 검사 불통이면) 해당 인덱스는 사용하지 않음
    isNull = id_len_check and publisher_len_check and data_name_len_check and description_len_check \
                and qa_len_check and an_len_check and achievement_2009_len_check and achievement_2015_len_check \
                and achievement_2022_len_check and source_name_len_check and class_name_check
    

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

    elif '중등_공통학년' in grade:
        path += '09.중등 공통학년\\'

    # noChange 개수 확인용
    if not class_name_check:
        nochange_num += 1

    # 유효성 검사 통과
    if isNull:
        num += 1
        # 폴더 없으면 만드는 함수
        makedirs(path)

        # json 파일 생성
        with open(path+title+file_type, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
    
    # 유효성 검사 통과 못한 데이터들
    else :
        failed_num += 1
        
        path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-1_split_test\\99.비정상 데이터\\'
        makedirs(path)

        # json 파일 생성
        with open(path+title+file_type, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

print(f'정상 데이터 개수: {num}')
print(f'비정상 데이터 개수: {failed_num}')
print(f'총합 데이터 개수: {num + failed_num}\n')
print(f'noChange 데이터 개수: {nochange_num}')
