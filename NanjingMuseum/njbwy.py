import datetime
import os
import yagmail
from PIL import Image
from aip import AipOcr
import undetected_chromedriver
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import random


# 调用百度文字识别API，识别验证码
def get_test_bybaidu(image_path):
    APP_ID = '36775789'
    API_KEY = 'wsnqnVSUZcU3xuFR4Rwntk7n'
    SECRECT_KEY = 'HiMiWkU1jQablzQgOOjBKpE6haysbg0s'
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


# 初始化
def init_spider(express_code):
    if express_code == 1:
        options = undetected_chromedriver.ChromeOptions()
        options.headless = True
        driver = undetected_chromedriver.Chrome(options=options)
        rangle = (1210, 810, 1365, 890)  # 验证码固定位置
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
        print(str(verifycode) + ' 验证码识别失败,正在重新识别...')
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
    block = driver.find_element(By.ID, 'nc_1_n1z')
    # 定位滑动区域
    # slot = arg_driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
    x_offset = 500
    # 创建一个事件链对象
    chains = ActionChains(arg_driver)
    # 实现滑块拖动
    chains.drag_and_drop_by_offset(block, x_offset, 0).perform()
    chains.release()
    return arg_driver


# 进入成功后，逐个判断是否可选,输入的日期用“-”分割例如：2023-9-10
def work(arg_driver, arg_date, arg_sxw, arg_name_list):
    over_in = True
    while over_in:
        now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print('----------' + now_time + '----------')
        if arg_date == "0":
            # 逐个判断是否可选
            for td in arg_driver.find_elements(By.XPATH, '//tbody//tr//td'):
                if td.get_attribute('class').find('disabled') != -1:
                    print(td.get_attribute('lay-ymd') + ' 无票')
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
                    # 点击确认
                    arg_driver.find_element(By.XPATH, '//*[text()="确认预约"]').click()
                    # 判断是否存在滑块
                    if exist_by_id(arg_driver, 'nc_1_n1z'):
                        print('存在滑块正在处理...')
                        # 处理滑块，并返回处理后的driver
                        arg_driver = handle_block(arg_driver)
                    else:
                        print("不存在滑块！")
                    print('提交成功！！')
                    print(now_time + '抢票成功')
                    mail.send(to="2403577910@qq.com", subject="南京博物馆抢票成功",
                              contents="南京博物馆抢票成功 " + str(arg_name_list) + " " + str(arg_date) + " " + str(arg_sxw))
                    over_in = False
                    jieshu = input("程序运行完成，按任意按键退出....")
                    break

        else:
            td = arg_driver.find_element(By.XPATH, '//tbody//tr//td[@lay-ymd="' + arg_date + '"]')
            if td.get_attribute('class').find('disabled') != -1:
                print(td.get_attribute('lay-ymd') + ' 无票')
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
                # 点击确认
                arg_driver.find_element(By.XPATH, '//*[text()="确认预约"]').click()
                # 判断是否存在滑块
                if exist_by_id(arg_driver, 'nc_1_n1z'):
                    print('存在滑块正在处理...')
                    # 处理滑块，并返回处理后的driver
                    arg_driver = handle_block(arg_driver)
                else:
                    print("不存在滑块！")
                print('提交成功！！')
                print(now_time + '抢票成功')
                mail.send(to="2403577910@qq.com", subject="南京博物馆抢票成功",
                          contents="南京博物馆抢票成功 " + str(arg_name_list) + " " + str(arg_date) + " " + str(arg_sxw))
                jieshu = input("程序运行完成，按任意按键退出....")
                over_in = False
        # 点击实现刷新
        time.sleep(random.uniform(0.7, 1.2))
        driver.switch_to.default_content()
        driver.find_element(By.XPATH, '//span[text()="预约"]//..').click()
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="Conframe"]'))


if __name__ == '__main__':
    addres = input("请输入配置文件地址：")
    if '"' in addres:
        addres = addres[1:-1]
    with open(addres, 'r', encoding='utf-8') as file:
        content = file.read()
        contentList = content.split('\n')
        print(contentList)
    over = True
    # 初始化发邮件对象
    mail = yagmail.SMTP(user="2403577910@qq.com",
                        password="vzyengsrfkcaebia",
                        host="smtp.qq.com")
    # 初始化基本信息
    username, password, name_list = contentList[0], contentList[1], []
    # username = input("用户名：")
    # password = input("密码：")
    # name_list = []
    print("")
    # temp_str = input('请输入预约人，输入多人时请用空格分开: ')
    temp_str = contentList[2]
    if temp_str.find(' ') != -1:
        name_list = temp_str.split(' ')
    else:
        name_list.append(temp_str)
    # 游玩时间
    # date = input('请输入游玩时间（具体日期例如“2023-9-10”，不需指定输入 0 ）：')
    date = contentList[3]
    # 上下午
    # sxw = input('请输入游玩时间（上午/下午）：')
    sxw = contentList[4]
    # 显示模式
    # mode_code1 = int(input('请输入显示模式（1为不显示浏览器，2为显示浏览器）：'))
    mode_code1 = int(contentList[5])
    driver, r1 = init_spider(mode_code1)
    # 初始化爬虫
    try:
        driver, r1 = init_spider(mode_code1)
    except Exception:
        result = input('谷歌浏览器版本问题，请重新安装！')
    # 开始
    while over:
        try:
            # 登录
            print('正在进行登录...')
            driver.get(r'https://ticket.wisdommuseum.cn/reservation/userOut/outSingle/toLoginSingle.do')
            # 获取并输入验证码
            driver.implicitly_wait(5)
            driver.maximize_window()  # 窗口最大化处理
            try:
                driver.find_element(By.XPATH, '//*[@id="telephone"]').send_keys(username)  # 定位并输入账号
                driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)  # 定位并输入密码
            except TimeoutException:
                print("超时，正在刷新！")
                driver.refresh()
                continue
            # mode_code2 = int(input('输入验证码处理方式(1、手动输入 2、自动识别)：'))
            mode_code2 = int(contentList[6])
            while next:
                if mode_code1 == 1 and mode_code2 == 1:
                    driver.save_screenshot('screen.png')  # 截取并保存当前页面
                    screen = Image.open('screen.png')  # 打开屏幕截图
                    screen.crop(r1).save('verifycode.png')  # 截取图片并放入指定位置
                    screen.close()
                    # 打开图片
                    image = Image.open('verifycode.png')
                    image.show()
                    # 输入验证码
                    verifycode = input('请输入验证码:')
                    # 识别后删除图片
                    image.close()
                    os.remove('screen.png')
                    os.remove('verifycode.png')
                elif mode_code1 == 2 and mode_code2 == 1:
                    # 输入验证码
                    verifycode = input('请输入验证码:')
                elif mode_code2 == 2:
                    driver.save_screenshot('screen.png')  # 截取并保存当前页面
                    screen = Image.open('screen.png')  # 打开屏幕截图
                    screen.crop(r1).save('verifycode.png')  # 截取图片并放入指定位置
                    screen.close()
                    # 调用百度文字识别API，识别验证码
                    verifycode = get_test_bybaidu('verifycode.png')
                    # 识别后删除图片
                    os.remove('screen.png')
                    os.remove('verifycode.png')
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
                        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="Conframe"]'))
                        if exist_by_xpath(driver, '/html/body/div[1]/div[2]/h3[text()="请选择您需要预约的日期"]'):
                            print('进入成功！')
                            work(driver, arg_date=date, arg_sxw=sxw, arg_name_list=name_list)
                            over = False
                            break
                        print('进入失败！')
                    else:  # 存在滑块
                        driver = handle_block(driver)
                        time.sleep(3)
                        work(driver, arg_date=date, arg_sxw=sxw, arg_name_list=name_list)
                        over = False
                        break
            break
        except Exception:
            print('错误！ 正在重试...')
            # 刷新网页
            driver.refresh()
