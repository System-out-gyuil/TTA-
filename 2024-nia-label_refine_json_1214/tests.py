import json


def check(f):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"파일로드됨 {f}, 데이터 개수: {len(data)}")
    except json.JSONDecodeError as e:
        print(f"{f}, 오류: {e}")
    except Exception as e:
        print(f"{f}, 오류: {e}")


f = r"C:\Users\admin\Desktop\syntax_check_converter - 복사본\2024-nia-label_refine_json_1214\2024-nia15-1-label-new1.json"  

check(f)