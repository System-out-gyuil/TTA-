import os

txt_num1 = 0
txt_num2 = 0
txt_num3 = 0
txt_num4 = 0

img_num1 = 0
img_num2 = 0
img_num3 = 0
img_num4 = 0

# 원천데이터(이미지파일) 경로
dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천"
img_path_list1 = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list1.append(file_path)

# 원천데이터(이미지파일) 경로
dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천-1"
img_path_list2 = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list2.append(file_path)

# 원천데이터(이미지파일) 경로
dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\15-1 원천-2"
img_path_list4 = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        if 'png' in file:
            file_path = os.path.join(root, file)
            img_path_list4.append(file_path)

# 원천데이터(이미지파일) 경로
dir_path = f"C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\split"
img_path_list3 = []

# 경로에 아래에 있는 있는 모든 파일 가져오기
for (root, directories, files) in os.walk(dir_path):
    for d in directories:
        d_path = os.path.join(root, d)

    for file in files:
        file_path = os.path.join(root, file)
        img_path_list3.append(file_path)

for path1 in img_path_list1:
    if 'TXT' in path1:
        txt_num1 += 1
    elif 'IMG' in path1:
        img_num1 += 1

for path2 in img_path_list2:
    if 'TXT' in path2:
        txt_num2 += 1
    elif 'IMG' in path2:
        img_num2 += 1

for path3 in img_path_list3:
    if 'TXT' in path3:
        txt_num3 += 1
    elif 'IMG' in path3:
        img_num3 += 1

for path4 in img_path_list4:
    if 'TXT' in path4:
        txt_num4 += 1
    elif 'IMG' in path4:
        img_num4 += 1

img_num = img_num1 + img_num2 + img_num3 + img_num4
txt_num = txt_num1 + txt_num2 + txt_num3 + txt_num4

print(f'img 갯수: {img_num}')
print(f'txt 갯수: {txt_num}')

