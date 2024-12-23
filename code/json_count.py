import json

with open("C:\\Users\\admin\\Desktop\\syntax_check_converter - 복사본\\추가 생성분.json", "r", encoding="utf-8") as f:
    makes = json.loads(f.read())

print(len(makes))
