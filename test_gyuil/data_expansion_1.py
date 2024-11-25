import json

# 파일 경로
input_file_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter\\1117_output_data\\15-1_nochange_filtered_output.json"
output_file_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter\\1117_output_data\\15-1_add_expansion.json"

# JSON 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 기존 데이터 개수 출력
original_count = len(data)

# 이미지 or 텍스트 데이터 구분
image_data = [item for item in data if "IMG" in item["source_data_info"]["source_data_name"]]
text_data = [item for item in data if "TXT" in item["source_data_info"]["source_data_name"]]

# 추가된 데이터 저장용 리스트
added_data = []

# 이미 사용된 6자리 숫자를 추출
used_numbers = set()
for item in data:
    source_data_name = item["source_data_info"]["source_data_name"]
    # 숫자 추출 (마지막 6자리)
    number = source_data_name.split("_")[-1]
    if number.isdigit():
        used_numbers.add(int(number))

# 새로운 6자리 숫자 생성 함수
def generate_unique_number(used_numbers):
    new_number = max(used_numbers) + 1  # 가장 큰 숫자에 +1
    while new_number in used_numbers:
        new_number += 1
    used_numbers.add(new_number)  # 새로운 숫자를 추가
    return f"{new_number:06d}"  # 6자리로 포맷팅

# 카운터 초기화
image_added_count = 0
text_added_count = 0

# 이미지 데이터 복사 (2배 늘리기)
duplicated_image_data = image_data.copy()
required_image_addition = len(image_data)  # 이미지 데이터 2배로 만들기
for item in duplicated_image_data[:required_image_addition]:
    new_item = item.copy()  # 각 항목을 복사

    # 고유 번호 생성
    new_number = generate_unique_number(used_numbers)

    # 고유 ID 변경
    new_item["raw_data_info"]["raw_data_name"] += f"_{new_number}"
    new_item["source_data_info"]["source_data_name"] = "_".join(
        new_item["source_data_info"]["source_data_name"].split("_")[:-1] + [new_number]
    )
    new_item["learning_data_info"]["learning_data_name"] = "_".join(
        new_item["learning_data_info"]["learning_data_name"].split("_")[:-1] + [new_number]
    )
    added_data.append(new_item)  # 추가된 데이터에 저장
    image_added_count += 1   # 이미지 데이터 추가 카운트 증가

# 텍스트 데이터 복사 (53542개 늘리기)
text_data_to_add = text_data[:53542] if len(text_data) > 53542 else text_data.copy()
for item in text_data_to_add:
    new_item = item.copy()  # 각 항목을 복사

    # 고유 번호 생성
    new_number = generate_unique_number(used_numbers)

    # 고유 ID 변경
    new_item["raw_data_info"]["raw_data_name"] += f"_{new_number}"
    new_item["source_data_info"]["source_data_name"] = "_".join(
        new_item["source_data_info"]["source_data_name"].split("_")[:-1] + [new_number]
    )
    new_item["learning_data_info"]["learning_data_name"] = "_".join(
        new_item["learning_data_info"]["learning_data_name"].split("_")[:-1] + [new_number]
    )
    added_data.append(new_item)  # 추가된 데이터에 저장
    text_added_count += 1   # 텍스트 데이터 추가 카운트 증가

# 추가된 데이터만 저장
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(added_data, f, indent=4, ensure_ascii=False)

# 결과 출력
new_count = original_count + len(added_data)
print("<15-1 데이터 증강>")
print(f"15-1 기존 총 데이터 개수: {original_count}")
print(f"15-1 기존 이미지 데이터 개수: {len(image_data)}")
print(f"15-1 기존 텍스트 데이터 개수: {len(text_data)}")
print(f"15-1 추가된 총 데이터 개수: {len(added_data)}")
print(f"15-1 추가된 이미지 데이터 개수: {image_added_count}")
print(f"15-1 추가된 텍스트 데이터 개수: {text_added_count}")
print(f"*****15-1 새파일(기존+증강) 총 데이터 개수: {new_count}*****")
