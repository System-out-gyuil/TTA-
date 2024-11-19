import os

path = 'C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\test_gyuil\\'

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

makedirs(path + 'test')

    # level_grade_mapping = {
    #     '초등_3': '01.초등학교 3학년\\',
    #     '초등_4': '02.초등학교 4학년\\',
    #     '초등_5': '03.초등학교 5학년\\',
    #     '초등_6': '04.초등학교 6학년\\',
    #     '중등_1': '05.중학교 1학년\\',
    #     '중등_2': '06.중학교 2학년\\',
    #     '중등_3': '07.중학교 3학년\\',
    #     '고등_1': '08.고등학교 1학년\\'
    # }