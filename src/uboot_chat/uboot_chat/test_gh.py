import re

pattern = re.compile(
    r'(?:去|到|带我去|送我去)?\s*([零〇一二三四五六七八九十]{1,3}|\d{1,4})号房'
)

user_msg = "一天"
m = pattern.search(user_msg)
if m:
    print("匹配成功:", m.group(1))
