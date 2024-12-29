import datetime
import os
from PIL import Image
from aip import AipOcr
from selenium import webdriver
import undetected_chromedriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import threading
import random


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


# 通过界面是否有确定按钮判断是否有“确认弹窗”
def exist_popup(arg_driver):
    try:
        arg_driver.find_element(By.XPATH, '//*[text()="确定"]')
        return True
    except NoSuchElementException:
        return False


# 通过判断界面是否有验证码失败提示来判断验证码是否正确
def pass_verify(arg_driver, arg_verifycode):
    try:
        arg_driver.find_element(By.XPATH, '//*[text()="验证码不正确"]')
        print(str(arg_verifycode) + ' 验证码识别失败,正在重新识别...')
        return True
    except NoSuchElementException:
        return False


def exist_by_xpath(arg_driver, xpath_expression):
    try:
        arg_driver.find_element(By.XPATH, xpath_expression)
        return True
    except NoSuchElementException:
        return False


def exist_by_id(arg_driver, element_id):
    try:
        arg_driver.find_element(By.ID, element_id)
        return True
    except NoSuchElementException:
        return False


def handle_block(arg_driver):
    # 定位滑块
    block = arg_driver.find_element(By.ID, 'nc_1_n1z')
    # 定位滑动区域
    x_offset = 500
    # 创建一个事件链对象
    chains = ActionChains(arg_driver)
    # 实现滑块拖动
    chains.drag_and_drop_by_offset(block, x_offset, 0).perform()
    chains.release()
    return arg_driver


# 进入成功后，逐个判断是否可选,输入的日期用“-”分割例如：2023-9-10
def work(n, arg_driver, arg_date, arg_sxw, arg_name_list):
    over_in = True
    while over_in:
        try:
            now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(f'进程{n}————————{now_time}————————————')
            td = arg_driver.find_element(By.XPATH, '//tbody//tr//td[@lay-ymd="' + arg_date + '"]')
            if td.get_attribute('class').find('disabled') != -1:
                print('、'.join(arg_name_list) +  '：'  + td.get_attribute('lay-ymd') + ' 无票')
            else:
                # 点击进入预约界面
                td.click()
                # 判断上午有票还是下午有票
                arg_driver.find_element(By.XPATH, '//button[text()="' + arg_sxw + '"]').click()
                # 选人
                for name in arg_name_list:
                    xpath = '//tbody//tr//td[text( )="' + name + '"]//../td/input'
                    arg_driver.find_element(By.XPATH, xpath).click()
                print('选人完成,正在进行提交...')
                # 提交
                arg_driver.find_element(By.XPATH, '//*[@id="ss"]').click()
                print('提交完成,正在在确认...')
                # 点击确认
                arg_driver.implicitly_wait(2)
                try:
                    arg_driver.find_element(By.XPATH, '//*[text()="确认预约"]').click()
                    arg_driver.find_element(By.XPATH, '//*[text()="确认预约"]').click()
                except Exception as e:
                    print(1)
                # 判断是否存在滑块
                if exist_by_id(arg_driver, 'nc_1_n1z'):
                    print('存在滑块正在处理...')
                    # 定位滑块
                    block = arg_driver.find_element(By.ID, 'nc_1_n1z')
                    # 定位滑动区域
                    x_offset = 500
                    # 创建一个事件链对象
                    chains = ActionChains(arg_driver)
                    # 实现滑块拖动
                    chains.drag_and_drop_by_offset(block, x_offset, 0).perform()
                    chains.release()
                    print('滑块处理完成....')
                else:
                    print("不存在滑块！")
                    arg_driver.save_screenshot(r"picture\temp1.png")
                if not exist_by_xpath(arg_driver, '//*[text()="你已成功预约南京博物院参观"]'):
                    print("预约失败，正在重试....")
                    picturePath = (os.path.abspath(r"picture\\" + str(arg_name_list) + '.png'))
                    print('预约失败!原因截图保存至：', picturePath)
                    arg_driver.save_screenshot(picturePath)
                else:
                    print(now_time + '预约成功')
                    picturePath = os.path.abspath(r"picture\\" + str(arg_name_list) + '.png')
                    arg_driver.save_screenshot(picturePath)
                    print('提交成功！截图保存至：', picturePath)

                    over_in = False
                    jieshu = input("程序运行完成，按任意按键退出....")
                    break
            # 点击实现刷新
            #time.sleep(random.uniform(1, 1.2))-
            arg_driver.switch_to.default_content()
            arg_driver.find_element(By.XPATH, '//span[text()="预约"]//..').click()
            arg_driver.switch_to.frame(arg_driver.find_element(By.XPATH, '//*[@id="Conframe"]'))
        except UnexpectedAlertPresentException as e:
            # 点击实现刷新
            #time.sleep(random.uniform(1, 1.2))
            arg_driver.switch_to.default_content()
            arg_driver.find_element(By.XPATH, '//span[text()="预约"]//..').click()
            arg_driver.switch_to.frame(arg_driver.find_element(By.XPATH, '//*[@id="Conframe"]'))



def main(n, username, password, name_list, date, sxw, mode_code1, mode_code2):
    over = True
    # 初始化爬虫
    driver, r1 = init_spider(mode_code1)
    # 开始
    while over:
        try:
            # 登录
            print('正在进行登录...')
            driver.get(r'https://ticket.wisdommuseum.cn/reservation/userOut/outSingle/toLoginSingle.do')
            # 获取并输入验证码
            driver.implicitly_wait(2)
            # driver.maximize_window()  # 窗口最大化处理
            try:
                driver.find_element(By.XPATH, '//*[@id="telephone"]').send_keys(username)  # 定位并输入账号
                driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)  # 定位并输入密码
                print('账号密码输入完成！')
            except Exception as e:
                print("账号密码输入错误！正在刷新...")
                driver.refresh()
                continue
            # mode_code2 = int(input('输入验证码处理方式(1、手动输入 2、自动识别)：'))


            while next:
                if mode_code1 == 1 and mode_code2 == 1:
                    # 截取二维码图片并保存为.png
                    captcha_element = driver.find_element(By.ID, 'checkNumImage')
                    driver.execute_script("arguments[0].scrollIntoView();", captcha_element)
                    captcha_element.screenshot('captcha.png')
                    # 打开图片
                    image = Image.open('captcha.png')
                    image.show()
                    # 输入验证码
                    verifycode = input('请输入验证码:')
                    # 识别后删除图片
                    image.close()
                    os.remove('captcha.png')

                elif mode_code1 == 2 and mode_code2 == 1:
                    # 输入验证码
                    verifycode = input('请输入验证码:')
                
                elif mode_code2 == 2:
                    # 截取二维码图片并保存为.png
                    captcha_element = driver.find_element(By.ID, 'checkNumImage')
                    driver.execute_script("arguments[0].scrollIntoView();", captcha_element)
                    png_name = 'captcha.png'
                    captcha_element.screenshot(png_name)
                    # 调用百度文字识别API，识别验证码
                    verifycode = get_test_bybaidu(png_name)
                    os.remove(png_name)

                else:
                    verifycode = None
                    print('参数输入错误！')
                driver.find_element(By.XPATH, '//*[@id="code"]').send_keys(verifycode)  # 定位并输入验证码
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="form"]/div[1]/div[6]/input').click()  # 点击登录
                time.sleep(1)
                # 判断验证码是否正确
                if pass_verify(driver, verifycode):  # 有验证码错误字样
                    continue
                else:
                    # 没有验证码错误字样，分情况处理
                    if exist_by_xpath(driver, '//*[@id="Conframe"]'):  # 成功进入
                        print('验证码识别成功!')
                        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="Conframe"]'))
                        if exist_by_xpath(driver, '/html/body/div[1]/div[2]/h3[text()="请选择您需要预约的日期"]'):
                            work(n, driver, arg_date=date, arg_sxw=sxw, arg_name_list=name_list)
                            over = False
                            break
                        print('进入失败！')
                    else:  # 存在滑块
                        driver = handle_block(driver)
                        time.sleep(3)
                        work(n, driver, arg_date=date, arg_sxw=sxw, arg_name_list=name_list)
                        over = False
                        break
            break
        except Exception as e:
            print(e)
            print('错误！ 正在重试...')
            # 刷新网页
            driver.refresh()




if __name__ == '__main__':
    addres = input("请输入配置文件地址：")
    # addres = '/home/yangmo/PythonProjects/nanbo/1518.txt'
    if '"' in addres:
        addres = addres[1:-1]
    with open(addres, 'r', encoding='utf-8') as file:
        content = file.read()
        contentList = content.split('\n')
        print(contentList)


    # 初始化基本信息
    username, password, name_list = contentList[0], contentList[1], []
    print("")
    temp_str = contentList[2]
    # 正常使用
    if temp_str.find(' ') != -1:
        name_list = temp_str.split(' ')
    else:
        name_list.append(temp_str)

    # 游玩时间
    date = contentList[3]
    
    # 上下午
    sxw = contentList[4]
    # 显示模式 1为不显示浏览器，2为显示浏览器
    mode_code1, mode_code2 = int(contentList[5]), int(contentList[6])

    # 多线程处理
    thread_nums = 4

    for i in range(thread_nums):
        thread_id = i+1
        print('启动第'+str(thread_id)+'个线程！')
        temp = threading.Thread(target=main, args=(thread_id, username, password, name_list, date, sxw, mode_code1, mode_code2))
        temp.start()
        time.sleep(random.uniform(20, 30))
    
    print(1)


