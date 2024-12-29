import requests
import os
from tqdm import tqdm


cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218948021d1765-04a7b784f39198-7e565470-1821369-18948021d181261%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2218948021d1765-04a7b784f39198-7e565470-1821369-18948021d181261%22%7D',
    'Ecp_ClientId': '3231027192900515924',
    '__root_domain_v': '.nepu.edu.cn',
    '_qddaz': 'QD.535104622067066',
    '_webvpn_key': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjEwNzAzMTQwMjE0IiwiZ3JvdXBzIjpbMTM3LDFdLCJpYXQiOjE3MDQ2MzU2NjAsImV4cCI6MTcwNDcyMjA2MH0.83CIgVt4DxEsMkq51YHqYQj9UV9jJ1msk8veZCDdQ-4',
    'webvpn_username': '210703140214%7C1704635660%7Cb5cb4435e9b29f4269856affdcbed15cdb641cd1',
    'JSESSIONID': 'E5C8C4FF35563737906161B8B2B6F630',
}

headers = {
    'authority': 'jwgl.webvpn.nepu.edu.cn',
    'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218948021d1765-04a7b784f39198-7e565470-1821369-18948021d181261%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2218948021d1765-04a7b784f39198-7e565470-1821369-18948021d181261%22%7D; Ecp_ClientId=3231027192900515924; __root_domain_v=.nepu.edu.cn; _qddaz=QD.535104622067066; _webvpn_key=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjEwNzAzMTQwMjE0IiwiZ3JvdXBzIjpbMTM3LDFdLCJpYXQiOjE3MDQ2MzU2NjAsImV4cCI6MTcwNDcyMjA2MH0.83CIgVt4DxEsMkq51YHqYQj9UV9jJ1msk8veZCDdQ-4; webvpn_username=210703140214%7C1704635660%7Cb5cb4435e9b29f4269856affdcbed15cdb641cd1; JSESSIONID=E5C8C4FF35563737906161B8B2B6F630',
    'dnt': '1',
    'referer': 'https://jwgl.webvpn.nepu.edu.cn/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}

params = {
    'd': '1704635686205',
}


if __name__=='__main__':
    for d in tqdm(range(100)):
        params = {
            'd': str(d),
        }
        response = requests.get('https://jwgl.webvpn.nepu.edu.cn/yzm', params=params, cookies=cookies, headers=headers)
        response.raise_for_status()
        
        path = os.path.join(r'D:\Desktop\picture', str(d) + '.png')
        with open(path, 'wb') as f:
            f.write(response.content)

