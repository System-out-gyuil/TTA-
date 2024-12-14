import json
import os
from tqdm import tqdm

num = 0
failed_num = 0
learning_data_null_count = 0

# 파라미터로 받은 경로(폴더)가 없으면 만들어주는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 학교별, 학년별 분리하는 함수
def find_grade(source_name, school, grade, path):
    if '초등_3' in source_name:
        path += f'01.{school}학교 {grade}학년\\'

    elif '초등_4' in source_name:
        path += f'02.{school}학교 {grade}학년\\'

    elif '초등_5' in source_name:
        path += f'03.{school}학교 {grade}학년\\'

    elif '초등_6' in source_name:
        path += f'04.{school}학교 {grade}학년\\'

    elif '중등_1' in source_name:
        path += f'06.중학교 {grade}학년\\'

    elif '중등_2' in source_name:
        path += f'07.중학교 {grade}학년\\'

    elif '중등_3' in source_name:
        path += f'08.중학교 {grade}학년\\'

    elif '고등_1' in source_name:
        path += f'09.{school}학교 {grade}학년\\'
        
    elif '고등_2' in source_name:
        path += f'10.{school}학교 {grade}학년\\'

    elif'중등_공통학년' in source_name:
        path += f'05.중학교 공통학년\\'

    # 학년 표시가 안되어있거나 안맞는 경우
    else :
        path += '98.경로 지정필요\\'

    return path

# 과목별 분리하기
def find_subject(subject, path):
    if subject == '국어':
        path += f'01.{subject}\\'

    elif subject == '영어':
        path += f'02.{subject}\\'

    elif subject == '수학':
        path += f'03.{subject}\\'

    elif subject == '사회':
        path += f'04.{subject}\\'

    elif subject == '과학':
        path += f'05.{subject}\\'

    elif subject == '정보':
        path += f'06.{subject}\\'

    elif subject == '기술가정':
        path += f'07.{subject}\\'

    elif subject == '도덕':
        path += f'08.{subject}\\'

    elif subject == '사회문화':
        path += f'09.{subject}\\'

    elif subject == '공통국어1':
        path += f'10.{subject}\\'

    elif subject == '공통국어2':
        path += f'11.{subject}\\'

    return path

# 텍스트 이미지 분리하기
def text_img_split(isTXT, path):
    if isTXT:
        path += '01.택스트\\'
    else :
        path += '02.이미지\\'

    return path

# 분리할 원본 json 파일 경로
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-2_output_data_new.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

for data in tqdm(datas):

    # 파일 저장할 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-2_split_test\\'

    # 제목
    title = data.get('source_data_info').get('source_data_name')

    # 파일 형식
    file_type = '.json'

    raw_data_info = data.get('raw_data_info')

    id = raw_data_info.get('raw_data_name')
    publisher = raw_data_info.get('publisher')
    subject = raw_data_info.get('subject')


    source_data_info = data.get('source_data_info')

    source_name = source_data_info.get('source_data_name')
    achievement_2009 = source_data_info.get('2009_achievement_standard')
    achievement_2015 = source_data_info.get('2015_achievement_standard')
    achievement_2022 = source_data_info.get('2022_achievement_standard')


    learning_data_info = data.get('learning_data_info')

    
    if not learning_data_info == []:
        
        description = learning_data_info[0].get('class_info_list')[0].get('text_description')

        # 최소값과 최대값(1 ~ 255 or 999) 검사
        # raw_data_info
        # raw_data_name (1~255)
        id_len_check = 1 <= len(id) <= 255
        # publisher (1~255)
        publisher_len_check = 1 <= len(publisher) <= 255

        # source_data_info
        # source_data_name (1~255)
        source_name_len_check = 1 <= len(source_name) <= 255
        # 2009_achievement_standard (999자 이하, null 허용이기 때문)
        achievement_2009_len_check = len(achievement_2009) <= 999
        # 2015_achievement_standard (999자 이하, null 허용이기 때문)
        achievement_2015_len_check = len(achievement_2015) <= 999
        # 2022_achievement_standard (1~999)
        achievement_2022_len_check = 1 <= len(achievement_2022) <= 999

        # learning_data_info
        # # text_description (1~9999)
        description_len_check = 1 <= len(description) <= 9999
        

        # 조건식중 하나라도 해당되지 않으면(유효성 검사 불통이면) 해당 인덱스는 사용하지 않음
        isNull = id_len_check and publisher_len_check and description_len_check \
                    and achievement_2009_len_check and achievement_2015_len_check \
                    and achievement_2022_len_check and source_name_len_check
        
        # source_name을 split을 통해 나눠줌
        splited_source_name = source_name.split("_")

        # 학교(초, 중, 고)
        school = splited_source_name[1]
        # 학년
        grade = splited_source_name[2]

        # 학교, 학년별 나누기
        path = find_grade(source_name, school, grade, path)
        # 과목 나누기
        path = find_subject(subject, path)
        
        
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
            
            path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-2_split_test\\99.비정상 데이터\\'
            makedirs(path)

            # json 파일 생성
            with open(path+title+file_type, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    # learning_data_list가 null인 데이터 개수
    else :
        learning_data_null_count += 1
        path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-2_split_test\\99.비정상 데이터\\'
        makedirs(path)

        # json 파일 생성
        with open(path+title+file_type, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

print(f'정상 데이터 개수: {num}')
print(f'비정상 데이터 개수: {failed_num + learning_data_null_count}')
print(f'총합 데이터 개수: {num + failed_num + learning_data_null_count}\n')
print(f'learning_data_null 데이터 개수: {learning_data_null_count}')
