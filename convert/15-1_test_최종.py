import os
import json

# 데이터 구분번호 고정 값
data_category = "S1"

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

# 과목 매핑
subject_mapping = {
    "국어": "국어",
    "영어": "영어",
    "수학": "수학",
    "사회": "사회",
    "과학": "과학",
    "기술·가정": "기술가정",
    "도덕": "도덕",
    "정보": "정보",
    "사회문화": "사회문화"
}

# 파일명 변환 함수 (라벨링 데이터 형식으로 변환)
def convert_filename(school, grade, subject, data_type):
    global image_sequence  # 전역 변수로 이미지 순번 사용

    # 매핑된 값 가져오기 (매핑이 없을 경우 원래 값 그대로 사용)
    school_level = school_level_mapping.get(school, school)   # 학교급 매핑
    grade_number = grade_mapping.get(grade, grade)            # 학년 매핑
    subject_name = subject_mapping.get(subject, subject)      # 과목 매핑

    # image_sequence 6자리 숫자 문자열로 변환 (예: 000001)
    sequence_str = f"{image_sequence:06d}"

    # 변환된 라벨링 데이터 파일명 생성 (예: S1_중등_1_국어_TXT_000001)
    labeling_file_name = f"{data_category}_{school_level}_{grade_number}_{subject_name}_{data_type}_{sequence_str}"

    # 함수 호출 시마다 image_sequence 증가 (index)
    image_sequence += 1

    return labeling_file_name

# label데이터 처리 함수
def process_label_data(label_data):
    label_dict = {}

    for item in label_data:
        # 라벨 데이터에서 필요한 필드 추출
        data_id = item['prev_data']['data_id']
        annotations = item['datas'][0].get('labelings', {}).get('annotations', [])

        # 기본 변수들 초기화 (class_num은 annotations의 개수 사용)
        class_num = len(annotations)
        bounding_boxes = []
        text_description = ""
        text_qa = ""
        text_an = ""

        for annotation in annotations:
            if annotation.get('markType') == 'polygonAndBox':
                class_name = annotation.get('name', "")
                values = annotation.get('value', [])

                # values 리스트 순회하여 모든 text와 location 수집
                # 문단값 안들어가게 해야함
                for value in values:
                    key = list(value.keys())[0]

                    # annotations.value[] 안에서 첫번째 key값이 type일때
                    if key == 'type':
                        # location이나 text가 여러개 있을 수 있음
                        # location을 list에 담아줌
                        bounding_boxes.append(value.get('location', []))
                        # text를 이어서 담아줌
                        text_description += value.get('text', "") + " "


            # 질문과 답변 처리
            if annotation.get('name') == '질문':
                text_qa = annotation.get('value', "")
            if annotation.get('name') == '답변':
                text_an = annotation.get('value', "")

        # 질문이나 답변이 비어 있을 때 text_description으로 채움
        if not text_qa:
            text_qa = text_description

        if not text_an:
            text_an = text_description

            

        # 문자열 끝의 공백 제거
        text_description = text_description.strip()

        # 각 라벨 항목을 딕셔너리에 저장 (learning_data_name 나중에 채워질 예정)
        label_dict[data_id] = {
            "learning_data_info": {
                "learning_data_name": "",
                "class_num": class_num,
                "class_name": class_name,
                "bounding_box": bounding_boxes,
                "text_description": text_description,
                "text_qa": text_qa,
                "text_an": text_an
            }
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

            # prev_data - data_info 에서 추출
            school = prev_data.get("data_info", {}).get("school", "")
            grade = prev_data.get("data_info", {}).get("grade", "")
            semester = prev_data.get("data_info", {}).get("semester", "")
            subject = prev_data.get("data_info", {}).get("subject", "")
            date = prev_data.get("data_info", {}).get("date", "")
            publisher = prev_data.get("data_info", {}).get("publisher", "")
            publication_year = prev_data.get("data_info", {}).get("publication year", "")
            revision_year = prev_data.get("data_info", {}).get("revision year", "")

            # 데이터 종류에 따른 data_type 설정
            data_type = "TXT"   # 기본값 설정
            for meta in metaDatas:
                if meta.get("name") == "데이터 종류":
                    if meta.get("value") == "이미지":
                        data_type = "IMG"
                    elif meta.get("value") == "텍스트":
                        data_type = "TXT"

            # metaDatas 에서 성취기준 추출
            achievement_standard_2015 = ""
            achievement_standard_2009 = ""
            achievement_standard_2022 = ""
            for meta in metaDatas:
                if meta.get("name") == "성취기준":
                    achievement_standard_2015 = meta.get("value", [])
                # 2009와 2022 성취기준도 설정 가능

                # 2009의 데이터에 빈값 존재
                # 2009, 2015는 null 허용
                if meta.get("name") == "2009 성취기준":
                    achievement_standard_2009 = meta.get("value", [])
                if meta.get("name") == "2022 성취기준":
                    achievement_standard_2022 = meta.get("value", [])
                # 성취기준 매핑값을 2022_achievement_standard에 설정
                if meta.get("name") == "성취기준 매핑값":
                    achievement_standard_2022 = meta.get("value", [])

            # 파일명 변환
            converted_file_name = convert_filename(school, grade, subject, data_type)

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
                    "2022_achievement_standard": achievement_standard_2022  # 2022 성취기준 매핑값 추가
                }
            }
    return refine_dict


# 병합 함수 및 최종 JSON 생성
def merge_data(label_dict, refine_dict):
    merged_data = []
    num = 0

    # 라벨 데이터를 순회하며 리파인 데이터와 병합
    for data_id, label_info in label_dict.items():
        if data_id in refine_dict:
            # 리파인 데이터가 있을 경우 병합
            source_data_name = refine_dict[data_id]["source_data_info"]["source_data_name"]
            label_info["learning_data_info"]["learning_data_name"] = source_data_name  # learning_data_name을 source_data_name과 동일하게 설정
            
            combined_info = {
                "raw_data_info": refine_dict[data_id]["raw_data_info"],
                "source_data_info": refine_dict[data_id]["source_data_info"],
                "learning_data_info": label_info["learning_data_info"]
            }

            num += 1

        else:
            # 리파인 데이터가 없으면 라벨 데이터만 사용
            combined_info = {
                "learning_data_info": label_info["learning_data_info"]
            }

        merged_data.append(combined_info)

    # print(num)
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
    # with open('15-1_output_data_test_new_4.json', 'w', encoding='utf-8') as f_final:
    #     json.dump(final_data, f_final, indent=4, ensure_ascii=False)

    # print("JSON file")


# 호출하여 파일을 처리
label_file_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\2024-nia-label_refine_json\\2024-nia15-1-label-new.json'
refine_file_path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\2024-nia-label_refine_json\\2024-nia15-1-refine-new2.json'

generate_final_json(label_file_path, refine_file_path)