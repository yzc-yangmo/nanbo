import re
import os
import requests
from aip import AipOcr
import undetected_chromedriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# 调用百度文字识别API，识别验证码
def get_test_bybaidu(image_path):
    APP_ID = '40423361'
    API_KEY = 'wZvHBl4kSDLDhDuKAkVO9ZTh'
    SECRECT_KEY = 'EDDV7R2xPGLHfVnlFW1dHEP0neAKlsQv'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    img = open(image_path, 'rb').read()
    info = client.basicAccurate(img)
    try:
        if info['words_result'][0]['words'].find(' ') != -1:
            result = ''
            for str_temp in info['words_result'][0]['words'].split(' '):
                result += str_temp
            return result
        return info['words_result'][0]['words']
    except IndexError:
        print('验证码识别失败!' + str(info))
        return -1
    
# 初始化爬虫，1为无头模式，2为有头模式
def init_spider(express_code):
    if express_code == 1:
        # 设置无头模式
        options = undetected_chromedriver.ChromeOptions()
        options.add_argument('--headless')
        driver = undetected_chromedriver.Chrome(options=options)
        rangle = (2667, 826, 2814, 888)  # 验证码固定位置
    elif express_code == 2:
        driver = undetected_chromedriver.Chrome()
        rangle = (1060, 820, 1210, 890)  # 验证码固定位置
    else:
        driver, rangle = None, None
        print('参数输入错误')
    return driver, rangle


# 通过判断界面是否有验证码失败提示来判断验证码是否正确
def pass_verify(arg_driver, arg_verifycode):
    try:
        arg_driver.find_element(By.XPATH, '//*[text()="验证码不正确"]')
        print(str(verifycode) + ' 验证码识别失败,正在重新识别...')
        return True
    except NoSuchElementException:
        return False

def extract_info(text):
    # 姓名的正则表达式
    name_regex = r'[\u4e00-\u9fa5]+'
    # 身份证号的正则表达式
    id_regex = r'\d{17}[\dX]'

    # 使用正则表达式匹配姓名和身份证号
    name_match = re.search(name_regex, text)
    id_match = re.search(id_regex, text)

    # 如果都匹配成功，则返回匹配结果，否则返回None
    if name_match and id_match:
        return name_match.group(), id_match.group()
    else:
        return None


def cookies_str_to_dict(cookie_str):
    cookie_dict = {}
    for cookie in cookie_str.split(';'):
        name, value = cookie.strip().split('=', 1)
        cookie_dict[name] = value
    return cookie_dict


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ticket.wisdommuseum.cn',
    'Referer': 'https://ticket.wisdommuseum.cn/reservation/ticketOut/out/toOrderPC.do',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



if __name__ == "__main__":
    mode_code1 = 2 # 显示浏览器

    # 初始化爬虫
    driver, r1 = init_spider(mode_code1)
    # 登录
    print('正在进行登录...')
    driver.get(r'https://ticket.wisdommuseum.cn/reservation/userOut/outSingle/toLoginSingle.do')
    
    pn = input('请输入手机号：').strip()
    pwd = input('请输入密码：').strip()
    driver.find_element(By.XPATH, '//*[@id="telephone"]').send_keys(pn)  # 定位并输入账号
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pwd)  # 定位并输入密码
    while True:
        verifycode = input('请输入验证码:') # 验证码
        driver.find_element(By.XPATH, '//*[@id="code"]').send_keys(verifycode)  # 定位并输入验证码
        # 点击登录
        driver.find_element(By.XPATH, '//*[@id="form"]/div[1]/div[6]/input').click() 

        # 判断验证码是否正确
        if not pass_verify(driver, verifycode):  # 有验证码错误字样
            break
    
    # ---------------------登录成功---------------------------
    # 获取cookies
    cookies = driver.get_cookies()

    # txt文件内容
    txt_file_content = {'pn':pn, 
                        'pwd':pwd, 
                        'names':'', 
                        'time':input("时间（使用'-'分割，例如：2024-1-11）：").strip(),
                        'sxw':input('上午/下午：'),
                        'display_mode':'2',
                        'varify_code_mode':'1'}
    # 存放人名用于生成txt
    nams_list = []
    # 循环添加
    while True:
        input_content = input('请输入还有姓名与身份证号的字符（结束输入no）：').strip()
        
        # 添加结束
        if input_content == 'no' or input_content == 'NO':
            break
        
        # 提取姓名与身份证号
        name, cardNo = extract_info(input_content)
        print(name)
        print(f'|{cardNo}| len:{len(cardNo)}')

    data = {
        'type': '0',
        'id': '',
        'name': name,
        'cardNo': cardNo,
    }
    # 发出请求
    response = requests.post(
        'https://ticket.wisdommuseum.cn/reservation/ticketOut/out/saveLinkmanPCAll.do',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    # 打印返回值
    print(f'return_code:', response.text)
    nams_list.append(name)

    # 生成txt文档
    txt_file_content['names'] = ' '.join(nams_list)
    file_path = txt_file_content['pn'] + '.txt'
    with open(file_path, 'w') as file:
        for key, val in txt_file_content.items():
            file.write(str(val)+'\n')
    print(f'文件保存成功！路径如下：{os.path.abspath(file_path)}')
