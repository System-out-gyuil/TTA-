import os
import json
from tqdm import tqdm

dir_path = "C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-2"
img_path_list = []

for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)
        # print(d_path)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list.append(file_path)

        # print(file_path.split('\\')[-1][0:-4])

os.close

print(len(img_path_list))

with open('C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\conversion_data_new\\15-2_output_data_new.json', 'r', encoding='utf-8') as f:
    datas = json.loads(f.read())

for data in tqdm(datas):

    raw_data_info = data.get('raw_data_info')
    source_data_info = data.get('source_data_info')

    raw_data_name = raw_data_info.get('raw_data_name')

    source_data_name = source_data_info.get('source_data_name')


    for img_path in img_path_list:
        if img_path.split('\\')[-1][0:-4] == raw_data_name:

            path_raw_name = dir_path+'\\'+source_data_name+'.png'

            os.rename(img_path, path_raw_name)
        
os.close