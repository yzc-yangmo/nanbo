# coding=utf-8
import re
import requests
import os



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


cookies=cookies_str_to_dict(input('str_cookie:'))
print('------------------------------------------------------------------------------------------------------')
if len(cookies) != 6:
    print('Cookies解析失败！')
else:
    print('Cookies解析成功！')

# cookies = {
#     'JSESSIONID': 'AA96563633E568A195936BA565AC53BC;',
#     'UM_distinctid': '18b7a3285177ff-0d931be07d2d72-26031151-1bcab9-18b7a328518125d',
#     'CNZZDATA1281245212': '60630283-1698562213-https%253A%252F%252Fwww.njmuseum.com%252F%7C1698566518',
#     'tfstk': 'fsxn3r0KVe7B-AlHucjIXP6l2juOAWsW4QERwgCr715_2phB9uXPsK9Lvbspq3vvFeUppL5kr1JJJkHCyzSkhBfdyM5-q_AeiuCCp_dMZKpVTk3CeuA6EIRlPv1Ra_AJUeHtDmpBdgszqjnxDho16LO34aSrU1WlFDSHtwpBdgw1wYYw0pZu-SKuqgRPbGWAUgWP4QSNb165UWWzYAvZtgF4xOrMm4QVi-28yAnnJt52L6JpphlAzy9hsFL6j9vdgpu44u-GKw-onH0-lwLyhZtpB0q1vKYNbtpIxlj2LtAd6Io4jGJ9QQQX5bZA5CxlzH7QUA5wxCxCYB3zmIjHZZ-FS8rJnd5hjO-qer19j6dyxNkYmaIwDZSeWVGdyMXDaHO3EuRV4vaaurgTVOkJjza58O6GMQg61JXXZwr-IA4jbwW1dcDiIza58O6GMADguP7FC9iG',
#     'acw_tc': '76b20fe717120317704996911e727d20feb26cc56dbf9d3dea7bd97be94918',
#     'acw_sc__v2': '660b881b48ac85175132f755edef4f2e0e7ab21d',
# }

txt_file_content = {'pn':input('手机号:').strip(), 
                    'pwd':input('密码：').strip(), 
                    'names':'', 
                    'time':input("时间（使用'-'分割，例如：2024-1-11）：").strip(),
                    'sxw':input('上午/下午：'),
                    'display_mode':'2',
                    'varify_code_mode':'2'}
nams_list = []
while True:
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
    input_content = input('请输入还有姓名与身份证号的字符（结束输入no）：').strip()
    
    # 添加结束
    if input_content == 'no' or input_content == 'NO':
        break
    # 提取姓名与身份证号
    name, cardNo = extract_info(input_content)
    print(name)
    print(f'|{cardNo}| len:{len(cardNo)}')
    # 构造请求头参数
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

    # # 判断是否添加成功
    # if int(response.text) > 0:
    #     print(' 添加成功！')
    #     # 写入字典信息
    #     nams_list.append(name)

    # else:
    #     print(f'  添加失败！错误代码 {response.text}')  
    #     if response.text == '-1':
    #         print(f'{name} 添加失败！')
    #     elif response.text == '-4':
    #         print('添加失败！账号人员已满...')

gene_txt = input('是否需要生成txt文档（y/n)：')
if gene_txt == 'y' or gene_txt == 'Y':
    # 生成txt文档
    txt_file_content['names'] = ' '.join(nams_list)
    file_path = txt_file_content['pn'] + '.txt'
    with open(file_path, 'w') as file:
        for key, val in txt_file_content.items():
            file.write(str(val)+'\n')
    print(f'文件保存成功！路径如下：{os.path.abspath(file_path)}')