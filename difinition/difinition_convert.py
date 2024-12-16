import json
import os
from tqdm import tqdm
import pandas as pd
import random

# make json파일 경로
with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\difinition\\2024-nia15-1-make-8.json", "r", encoding="utf-8") as f:
    makes = json.loads(f.read())

school_mapping = {
    "초등" : "초등학교",
    "중등": "중학교",
    "고등": "고등학교"
}

type_mapping = {
    "텍스트": "TXT",
    "이미지": "IMG"
}

raw_dict = {}
source_dict = {}
learning_dict = {}
list = []
failed_list = []

num_count = 8000000

for make in makes:
    datas = make.get("datas")

    # datas가 비어있는 경우가 있음
    for data in datas:

        # 인덱스 증가
        num_count += 1
        # 인덱스 여섯자리로 맞추기
        num_count_str = f"{num_count:07d}"
        
        # 국어_중학교_1학년_text_11232_70_png_00
        id = data.get("id")

        meta_datas = data.get("metaDatas")
        labelings = data.get("labelings")

        for meta in meta_datas:

            index = meta.get("index")
            value = meta.get("value")

            if index == 0:
                # 출판사
                publisher = value

            elif index == 1:
                # 출판년월
                date = value

            elif index == 2:
                # 개정년도
                revision_year = value

            elif index == 3:
                # 학교
                school = value

            elif index == 4:
                # 과목
                subject = value

            elif index == 5:
                # 학년
                grade_num = value

            elif index == 6:
                # 학기
                term = value

            elif index == 9:
                # 획득일
                date2 = value

        if publisher == '유니바':
            publisher = '2차 저작'

        # 2024.08을 2024-08-03으로 변경
        ran_date = random.randint(1, 30)
        ran_data_str = f"{ran_date:02d}"

        date = date.replace('.', '-')
        date = f'{date}-{ran_data_str}'

        # 획득일자 11/15 -> 11-15로 변경
        date2 = date2.replace('/', '-')

        grade = f'{grade_num}학년'


        if term != '공통':
            term = f'{term}학기'

        map_school = school_mapping.get(school)

        # 획득일자 형식에 년도 추가 08-27 -> 2024-08-27
        date2 = f'2024-{date2}'
    
        # label = labelings.get("annotations")[0]
        annotations = labelings.get("annotations")

        for label in annotations:

            label_index = label.get("index")
            label_value = label.get("value")

            if label_index == 0:
                if label_value:

                    text_description = label_value[0].get("text")
                    location = label_value[0].get("location")

            elif label_index == 1:
                # 성취 기준
                achievement_standard = label_value

            elif label_index == 2:
                # 질문
                qustion = label_value

            elif label_index == 3:
                # 답변
                anser = label_value

            elif label_index == 4:
                # 데이터 종류
                data_type = label_value

        annotations_len = len(annotations)

        map_type = type_mapping.get(data_type)


        # id값에 들어간 데이터 순서가 파일마다 달라서 포함된으로 사용
        if 'text' in id:
            class_name = "텍스트"
        
        elif 'table' in id:
            class_name = '이미지(표)'

        elif 'latex' in id:
            class_name = '이미지(수식)'

        elif 'chart' in id:
            class_name = '이미지(차트)'

        elif 'diagram' in id:
            class_name = '이미지(다이어그램)'

        else:
            class_name = '이미지(기타)'

        if grade_num == "2":
            grade_num = '공통'

        # S1_중등_1_영어_TXT_048685
        source_data_name = f"S1_{school}_{grade_num}_{subject}_{map_type}_{num_count_str}"

        # print(source_data_name)

        if grade == '2학년':
            grade = '공통'

        raw_dict = {
            "raw_data_name": id,
            "date": date2,
            "publisher": publisher,
            "publication_year" : date,
            "school": map_school,
            "grade": grade,
            "semester": term,
            "subject": subject,
            "revision_year": revision_year
        }

        if revision_year == "2009":
            source_dict = {
                "source_data_name": source_data_name,
                "2009_achievement_standard": [achievement_standard],
                "2015_achievement_standard": [""],
                "2022_achievement_standard": [""],
            }
        elif revision_year == "2015":
            source_dict = {
                "source_data_name": source_data_name,
                "2009_achievement_standard": [""],
                "2015_achievement_standard": [achievement_standard],
                "2022_achievement_standard": [achievement_standard],
            }
        elif revision_year == "2022":
            source_dict = {
                "source_data_name": source_data_name,
                "2009_achievement_standard": [""],
                "2015_achievement_standard": [""],
                "2022_achievement_standard": [achievement_standard],
            }

        learning_dict = {
            "learning_data_name": source_data_name,
            "class_num": annotations_len,
            "class_name": class_name,
            "bounding_box": [location],
            "text_description": text_description,
            "text_qa": qustion,
            "text_an": anser
        }
        
        # raw_data, source_data, learning_data를 하나의 딕셔너리로 합치기
        dict = {
            "raw_data_info": raw_dict,
            "source_data_info": source_dict,
            "learning_data_info": learning_dict
        }

        # 합쳐진 각각의 dict를 list에 추가
        list.append(dict)

        # for path in tqdm(img_path_list):
        #     img_path = path.split('\\')[-1]
        #     img_name = img_path.split('.')[0]
        #     # 파일명 ex)국어_고등학교_1학년_table_0_png_00.png 과 datas의 id값이 같을 경우
        #     if img_name == id:
        #         # 이름 바꾸고 다시 저장될 경로
        #         source_path = f'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\img_crop\\{make_path}\\{source_data_name}.png'

        #         os.rename(path, source_path)

        #     else :
        #         print(f'img_name: {img_name}\n id: {id}')


# json 파일 저장
with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\difinition_make\\2024-nia15-1-make-8_1216_3.json", 'w', encoding='utf-8') as f:
    json.dump(list, f, indent=4, ensure_ascii=False)

# failed_df = pd.DataFrame(failed_list)
# # id값과 파일명이 일치하지 않는 데이터 excel로 저장
# failed_df.to_excel('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1-make_failed-1.xlsx', index=False)
    