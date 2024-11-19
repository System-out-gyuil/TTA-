import json
 
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-1_output_data - 복사본.json', 'r', encoding='utf-8') as f:
    js = json.loads(f.read()) # json 라이브러리 이용


for i in js:
    # 경로
    path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\15-1_split_test\\'

    # 제목
    title = i.get('source_data_info').get('source_data_name')

    # 파일 형식
    file = '.json'

    with open(path+title+file, 'w', encoding='utf-8') as f:
        json.dump(i, f, indent=4, ensure_ascii=False)

        