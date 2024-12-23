import os
import json
import random

# 데이터 구분번호 고정 값
data_category = "S3"

# 이미지 순번 카운팅
image_sequence = 1

# 학교급 매핑
school_level_mapping = {
    "초등학교": "초등",
    "중학교": "중등",
    "고등학교": "고등"
}

# 학년 매핑
grade_mapping = {
    "1학년": "1",
    "2학년": "2",
    "3학년": "3",
    "4학년": "4",
    "5학년": "5",
    "6학년": "6"
}

# 파일명 변환 함수 (라벨링 데이터 형식으로 변환)
def convert_filename(school, grade):
    global image_sequence  # 전역 변수로 이미지 순번 사용

    # 매핑된 값 가져오기
    school_level = school_level_mapping.get(school, school)   # 학교급 매핑
    grade_number = grade_mapping.get(grade, grade)            # 학년 매핑

    # image_sequence 6자리 숫자 문자열로 변환 (예: 000001)
    sequence_str = f"{image_sequence:06d}"

    # 변환된 라벨링 데이터 파일명 생성
    labeling_file_name = f"{data_category}_{school_level}_{grade_number}_{sequence_str}"

    # 함수 호출 시마다 image_sequence 증가
    image_sequence += 1

    return labeling_file_name

# #특정 annotation 값을 처리하는 함수
# def process_annotation(values):
#     class_info_list = []
#     for value in values:
#         # Type을 box -> Bounding_Box, 나머지는 Polygon으로 처리
#         # type_value = "Bounding_Box" if value.get('type', '') == 'box' else "Polygon"
#         # 먼저 value가 딕셔너리인지 확인
#         if isinstance(value, dict):
#             # Type을 box -> Bounding_Box, 나머지는 Polygon으로 처리
#             type_value = "Bounding_Box" if value.get('type', '') == 'box' else "Polygon"       
#             class_info_list.append({
#                 "Type": type_value,  # 변환된 Type 값 추가
#                 "Type_value": value.get('location', []),
#                 "text_description": value.get('text', "")
#             })
#         # value가 문자열일 때는 "주", "관", "식"을 필터링하여 제외
#         # elif isinstance(value, str) and value not in ["주", "관", "식", "데이터", "종류"]:
#         #     class_info_list.append({
#         #         "Type": "Unknown",
#         #         "Type_value": [],
#         #         "text_description": value  # 문자열 그대로
#         #     })

#     return class_info_list

# 라벨 데이터 처리 함수
def process_label_data(label_data):
    label_dict = {}
    
    for item in label_data:
        # 라벨 데이터에서 필요한 필드 추출
        data_id = item['prev_data']['data_id']
        annotations = item['datas'][0].get('labelings', {}).get('annotations', [])

        # learning_data_list 는 가공된 데이터 저장 (class_num은 초기화)
        learning_data_list = []
        class_num = 0

        # annotation 값 추출
        for annotation in annotations:
            class_name = annotation.get('name', "")

            #특정 class_name 제외
            if class_name == "데이터 종류_noChange":
                continue    # 조건에 해당하면 다음 루프 실행

            class_num += 1
            values = annotation.get('value', []) or [] # NoneType 방지
            
            class_info_list = []
            for value in values:
                bounding_box = []
                text_description = ""

                if isinstance(value, dict):  # 값이 딕셔너리일 때
                    bounding_box = value.get('location', [])
                    text_description = value.get('text', "")
                else:
                    text_description = value  # 값이 문자열일 때

                class_info_list.append({
                    "bounding_box": bounding_box,
                    "text_description": text_description
                })

            learning_data_list.append({
                "class_num": class_num,
                "class_name": class_name,
                "class_info_list": class_info_list
            })

        # 각 라벨 항목을 딕셔너리에 저장
        label_dict[data_id] = {
            "learning_data_info": learning_data_list
        }
    
    return label_dict

# 리파인 데이터 처리 함수
def process_refine_data(refine_data):
    refine_dict = {}

    for item in refine_data:
        for data in item['datas']:
            data_id = data['id']

            prev_data = item.get('prev_data', {})  # prev_data가 없으면 기본값 {} 사용
            metaDatas = data.get('metaDatas', [])

            # prev_data 에서 추출
            school = prev_data.get("data_info", {}).get("school", "")
            grade = prev_data.get("data_info", {}).get("grade", "")
            semester = prev_data.get("data_info", {}).get("semester", "")
            subject = prev_data.get("data_info", {}).get("subject", "")
            date = prev_data.get("data_info", {}).get("date", "")
            publisher = prev_data.get("data_info", {}).get("publisher", "")
            publication_year = prev_data.get("data_info", {}).get("publication year", "")
            revision_year = prev_data.get("data_info", {}).get("revision year", "")

            # metaDatas 에서 성취기준 추출
            achievement_standard_2015 = ""
            achievement_standard_2009 = ""
            achievement_standard_2022 = ""
            types_of_problems = ""  # 문제 유형 (주관식/객관식)

            # metaDatas 리스트에서 값을 순회하여 추출
            for meta in metaDatas:
                if meta.get("name") == "성취기준":
                    achievement_standard_2015 = meta.get("value", [])
                if meta.get("name") == "2009 성취기준":
                    achievement_standard_2009 = meta.get("value", [])
                if meta.get("name") == "2022 성취기준":
                    achievement_standard_2022 = meta.get("value", [])
                # 성취기준 매핑값을 2022_achievement_standard에 설정
                if meta.get("name") == "성취기준 매핑값":
                    achievement_standard_2022 = meta.get("value", [])
                # 데이터 종류 (주관식/객관식) 추출
                if meta.get("name") == "데이터 종류":
                    types_of_problems = meta.get("value", "")

            # 난이도를 랜덤 설정 (상, 중, 하)
            level_of_difficulty = random.choice(["상", "중", "하"])

            # 파일명 변환
            converted_file_name = convert_filename(school, grade)
            
            # 필요 데이터 딕셔너리에 저장
            refine_dict[data_id] = {
                "raw_data_info": {
                    "raw_data_name": data_id,
                    "date": date,
                    "publisher": publisher,
                    "publication_year": publication_year,
                    "school": school,
                    "grade": grade,
                    "semester": semester,
                    "subject": subject,
                    "revision_year": revision_year  # revision_year 추가
                },
                "source_data_info": {
                    "source_data_name": converted_file_name,
                    "2009_achievement_standard": achievement_standard_2009,
                    "2015_achievement_standard": achievement_standard_2015,
                    "2022_achievement_standard": achievement_standard_2022,  # 2022 성취기준 매핑값 추가
                    "level_of_difficulty": level_of_difficulty,  # 난이도 추가
                    "types_of_problems": types_of_problems  # 문제 유형 추가
                }
            }
    return refine_dict

# 병합 함수 및 최종 JSON 생성
def merge_data(label_dict, refine_dict):
    merged_data = []

    # 라벨 데이터를 순회하며 리파인 데이터와 병합
    for data_id, label_info in label_dict.items():
        if data_id in refine_dict:
            # 리파인 데이터가 있을 경우 병합
            source_data_name = refine_dict[data_id]["source_data_info"]["source_data_name"]

            updated_learning_data_info = []
            for learning_data in label_info["learning_data_info"]:
                updated_learning_data = {
                    "class_num": learning_data["class_num"],  # 기존 정보 유지
                    "class_name": learning_data["class_name"],
                    "class_info_list": learning_data["class_info_list"]  # class_info_list를 유지
                }
                updated_learning_data_info.append(updated_learning_data)

            label_info["learning_data_info"] = updated_learning_data_info

            combined_info = {
                "raw_data_info": refine_dict[data_id]["raw_data_info"],
                "source_data_info": refine_dict[data_id]["source_data_info"],
                "learning_data_info": label_info["learning_data_info"]
            }
        else:
            # 리파인 데이터가 없으면 라벨 데이터만 사용
            combined_info = {
                "learning_data_info": label_info["learning_data_info"]
            }

        merged_data.append(combined_info)

    return merged_data

# 라벨 데이터 및 리파인 데이터 각각 처리
def generate_final_json(label_file, refine_file):
    # 라벨 데이터 처리
    with open(label_file, 'r', encoding='utf-8') as f1:
        label_data = json.load(f1)
    label_dict = process_label_data(label_data)

    # 리파인 데이터 처리
    with open(refine_file, 'r', encoding='utf-8') as f2:
        refine_data = json.load(f2)
    refine_dict = process_refine_data(refine_data)

    # 라벨 데이터와 리파인 데이터를 병합
    final_data = merge_data(label_dict, refine_dict)

    # 최종 데이터를 JSON 파일로 저장
    with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-3_output_data_new.json', 'w', encoding='utf-8') as f_final:
        json.dump(final_data, f_final, indent=4, ensure_ascii=False)

    print("JSON file")

# 호출하여 파일을 처리
label_file_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\2024-nia15-3-label-new.json'
refine_file_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\2024-nia15-3-refine-new2.json'

generate_final_json(label_file_path, refine_file_path)
