import json
import os
from tqdm import tqdm

num = 0
failed_num = 0
text_num = 0
img_num = 0

list = []

grade_num_mapping = {
    '초등_3': '01.',
    '초등_4': '02.',
    '초등_5': '03.',
    '초등_6': '04.',
    '중등_1': '06.',
    '중등_2': '05.',
    '중등_3': '08.',
    '고등_1': '09.',
    '고등_2': '10.',
    '중등_공통학년': '05.',
}

subject_num_mapping = {
    '국어': '01.',
    '영어': '02.',
    '수학': '03.',
    '사회': '04.',
    '과학': '05.',
    '정보': '06.',
    '기술가정': '07.',
    '도덕': '08.',
    '사회문화': '09.',
}

# 파라미터로 받은 경로(폴더)가 없으면 만들어주는 함수
def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 유효성 검사 함수 
def condition_check(data):

    raw_data_info = data.get('raw_data_info')

    id = raw_data_info.get('raw_data_name')
    publisher = raw_data_info.get('publisher')


    source_data_info = data.get('source_data_info')

    source_name = source_data_info.get('source_data_name')
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
    description_len_check = 1 <= len(description)
    # text_qa (1~999)
    qa_len_check = 1 <= len(qa)
    # text_an (1~999)
    an_len_check = 1 <= len(an)
    # 문장_noChange 제외
    class_name_check = not class_name == '문장_noChange'

    # source_data_info
    # 2009_achievement_standard (999자 이하, null 허용이기 때문)
    achievement_2009_len_check = len(achievement_2009) <= 999
    # 2015_achievement_standard (999자 이하, null 허용이기 때문)
    achievement_2015_len_check = len(achievement_2015) <= 999
    # 2022_achievement_standard (1~999)
    achievement_2022_len_check = 1 <= len(achievement_2022) <= 999
    # source_data_name (1~255)
    source_name_len_check = 1 <= len(source_name) <= 255

    # 조건식중 하나라도 해당되지 않으면(유효성 검사 불통이면) 해당 인덱스는 사용하지 않음
    condition = id_len_check and publisher_len_check and data_name_len_check and description_len_check \
               and qa_len_check and an_len_check and achievement_2009_len_check and achievement_2015_len_check \
               and achievement_2022_len_check and source_name_len_check and class_name_check
    
    return condition

# 학교별, 학년별 분리하는 함수
def find_grade(school_num, school, grade):
    grade_num = grade_num_mapping.get(school_num)

    path = f'{grade_num}{school} {grade}\\'

    return path

# 과목별 분리하기
def find_subject(subject):
    subject_num = subject_num_mapping.get(subject)

    path = f'{subject_num}{subject}\\'

    return path

# 텍스트 이미지 분리하기
def text_img_split(isTXT, path, text_num, img_num):
    if isTXT:
        text_num += 1
        path += '01.택스트\\'
    else :
        img_num += 1
        path += '02.이미지\\'

    return path, text_num, img_num

# 분리할 output json 파일 경로로 불러오기
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data_new\\15-1_output_data_new.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

for data in tqdm(datas):

    # 파일 저장할 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\split\\15-1_split\\'

    # 파일 형식
    file_type = '.json'

    # 제목
    title = data.get('source_data_info').get('source_data_name')

    source_name = data.get('source_data_info').get('source_data_name')

    raw_data_info = data.get('raw_data_info')


    # 각종 데이터 유효성 검사
    # condition = condition_check(data)
    condition = True
    
    school = raw_data_info.get('school')
    grade = raw_data_info.get('grade')

    # source_name을 split을 통해 나눠줌
    splited_source_name = source_name.split("_")

    # 학교(초등, 중등, 고등)
    school_check = splited_source_name[1]
    # 학년
    grade_check = splited_source_name[2]
    # 학교, 학년 번호 매핑용
    school_num = f'{school_check}_{grade_check}'

    # 과목
    subject = splited_source_name[3]
    # TXT인지
    isTXT = splited_source_name[4] == 'TXT'

    
    # 유효성 검사 통과
    if condition:
        num += 1

        # 학교, 학년별 나누기
        path += find_grade(school_num, school, grade)

        # 과목 나누기
        path += find_subject(subject)

        # 이미지, 텍스트 나누기
        test = text_img_split(isTXT, path, text_num, img_num)
        
        path = test[0]
        text_num = test[1]
        img_num = test[2]

        # 폴더 없으면 만드는 함수
        makedirs(path)
        # list.append(data)
        # json 파일 생성
        # with open(path+title+file_type, 'w', encoding='utf-8') as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)
        
    
    # 유효성 검사 통과 못한 데이터들
    else :
        failed_num += 1

        # 검사 통과 못한 데이터가 들어갈 경로
        path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\split\\15-1_split\\99.비정상 데이터\\'
        makedirs(path)

        # json 파일 생성
        # with open(path+title+file_type, 'w', encoding='utf-8') as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

print(f'정상 데이터 개수: {num}')
print(f'비정상 데이터 개수: {failed_num}')
print(f'총합 데이터 개수: {num + failed_num}\n')
print(f'text 개수: {text_num}')
print(f'img 개수: {img_num}')
