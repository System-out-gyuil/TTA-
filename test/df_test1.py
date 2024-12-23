import pandas as pd
import json
 
with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data\\15-1_output_data_test.json', 'r', encoding='utf-8') as f:
    js = json.loads(f.read()) ## json 라이브러리 이용
df = pd.json_normalize(js)

print(df.info())

# num = 0
# for data in df['learning_data_info.text_qa']:
#     if data[0] == '':
#         num += 1

# print(num)

# print(df['learning_data_info.text_description'])

# num = 0
# for data in df['learning_data_info.text_description']:
#     if data == "":
#         num += 1
#         print(f'빈 데이터: {data}')

# print(num)
# df_to_json = df.to_json(orient='records')

# print(df_to_json)


for datas in df:

    # print(datas)

    for data in df[datas]:

        # print(data)

        # 2009, 2015_achievement_standard는 null값을 허용하기때문에 제외
        isNotDescendant = not datas == 'source_data_info.2009_achievement_standard' and not datas == 'source_data_info.2015_achievement_standard'
        
        # if datas == 'raw_data_info.raw_data_name':
        #     pass
        #     # print(data)
        #     # data가 비어있고 2009, 2015가 아닐때
        # if data == '' and isNotDescendant:
        #     print(data)

        # print(type(data))

        # if datas == 'learning_data_info.text_qa':
        #     print(data)

        isCheck = datas == 'learning_data_info.text_description' and datas == 'learning_data_info.text_qa', datas == 'learning_data_info.text_an'

        if isCheck and len(data) > 999 and len(data) < 1:
            print(f'{datas}: {data}')