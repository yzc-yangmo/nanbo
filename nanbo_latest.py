from datetime import datetime
import os
import undetected_chromedriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import threading
import random

from CNN_predict.CNN_predict import CNN_predict # 验证码识别模块


# 初始化爬虫，1为无头模式，2为有头模式
def init_spider(display_mode_code):
    if display_mode_code == 1:
        # 设置无头模式
        options = undetected_chromedriver.ChromeOptions()
        options.add_argument('--headless')
        driver = undetected_chromedriver.Chrome(options=options)
    elif display_mode_code == 2:
        driver = undetected_chromedriver.Chrome()
    else:
        driver = None
        print('参数输入错误')
    return driver


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
            now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(f'进程{n}————————{now_time}————————————')
            td = arg_driver.find_element(By.XPATH, '//tbody//tr//td[@lay-ymd="' + arg_date + '"]')
            if td.get_attribute('class').find('disabled') != -1:
                print('、'.join(arg_name_list) +  ':'  + td.get_attribute('lay-ymd') + ' 无票')
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



def main(n, username, password, name_list, date, sxw, display_mode_code):
    over = True
    # 初始化爬虫
    driver = init_spider(display_mode_code)
    # 开始
    while over:
        try:
            # 登录
            print('正在进行登录...')
            driver.get(r'https://ticket.wisdommuseum.cn/reservation/userOut/outSingle/toLoginSingle.do')
            # 获取并输入验证码
            driver.implicitly_wait(2)

            try:
                driver.find_element(By.XPATH, '//*[@id="telephone"]').send_keys(username)  # 定位并输入账号
                driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)  # 定位并输入密码
                print('账号密码输入完成！')
            except Exception as e:
                print("账号密码输入错误！正在刷新...")
                driver.refresh()
                continue

            while next:
                # 识别并输入二维码
                captcha_element = driver.find_element(By.ID, 'checkNumImage')
                driver.execute_script("arguments[0].scrollIntoView();", captcha_element) # 截取二维码图片
                png_name = datetime.now().strftime('%H-%M-%S-%f')[:-3] + '.png' # 根据时间构造文件名，防止多进程死锁
                captcha_element.screenshot(png_name) # 保存图片
                verify_code = CNN_predict(png_name) # 调用模型识别
                os.remove(png_name) # 删除识别后
                driver.find_element(By.XPATH, '//*[@id="code"]').send_keys(verify_code)  # 定位并输入验证码
                time.sleep(1)
                
                # 同意用户协议
                driver.find_element(By.XPATH, '//*[@id="radio"]').click() 
                time.sleep(1)
                
                driver.find_element(By.XPATH, '//*[@id="form"]/div[1]/div[6]/input').click()  # 点击登录
                time.sleep(1)

                # 判断验证码是否正确
                if pass_verify(driver, verify_code):  # 有验证码错误字样
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
            time.sleep(random.random())




if __name__ == '__main__':
    #addres = input("请输入配置文件地址：")
    addres = './1851.txt'
    if '"' in addres:
        addres = addres[1:-1]
    with open(addres, 'r', encoding='utf-8') as file:
        content = file.read()
        contentList = content.split('\n')
        print(contentList)

    # 初始化基本信息
    username, password, name_list = contentList[0], contentList[1], []
    temp_str = contentList[2]
    # 正常使用
    if temp_str.find(' ') != -1:
        name_list = temp_str.split(' ')
    else:
        name_list.append(temp_str)
    date = contentList[3] # 游玩时间
    sxw = contentList[4] # 上下午
    display_mode_code = int(contentList[5]) # 显示模式 1为不显示浏览器，2为显示浏览器

    # 多线程处理
    thread_nums = int(input('输入线程数:')) # 进程数

    for i in range(thread_nums):
        thread_id = i+1
        print('启动第'+str(thread_id)+'个线程！')
        temp = threading.Thread(target=main, args=(thread_id, username, password, name_list, date, sxw, display_mode_code))
        temp.start()
        time.sleep(random.uniform(20, 30))

    
