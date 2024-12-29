import re

def extract_and_connect_names(text):
    # 定义一个正则表达式来匹配中文人名
    name_pattern = re.compile(r'([\u4e00-\u9fa5]+)') # 匹配中文字符
    
    # 使用正则表达式查找所有匹配的人名
    names = name_pattern.findall(text)
    
    # 将人名列表用空格连接成一个字符串
    connected_names = ' '.join(names)
    
    return connected_names

while True:
    # 给定的字符串
    input_text = input('Please:')

    # 调用函数并打印结果
    result = extract_and_connect_names(input_text)
    print(result)