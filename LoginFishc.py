'''
author: Darkmans
blog: https://fanfanblog.cn
github: https://github.com/Darkmans
bbs: http://bbs.fishc.org
'''
import time

from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_NAME = '零度非安全'
USER_PASSWD = 'jxycsgliaofan1994'
BORDER = 18

class LoginFishc:
    def __init__(self):
        self.url = 'http://bbs.fishc.org'
        self.browser = webdriver.Chrome()
        self.explicit_wait = WebDriverWait(self.browser, 10)
        self.user_name = USER_NAME
        self.user_passwd = USER_PASSWD

    def __del__(self):
        self.browser.close()

    # 打开鱼C网页并登录
    def loginFishc(self):
        self.browser.get(self.url)
        user_name = self.explicit_wait.until(EC.presence_of_element_located((By.ID, 'ls_username')))
        time.sleep(1)
        user_passwd = self.explicit_wait.until(EC.presence_of_element_located((By.ID, 'ls_password')))
        user_name.send_keys(self.user_name)
        user_passwd.send_keys(self.user_passwd)

    # 获取顶象验证码图片的位置
    def getDxVerifyImagePosition(self):
        dx_verify_image = self.explicit_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dx_captcha_basic_bg')))
        time.sleep(2)
        location = dx_verify_image.location
        size = dx_verify_image.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom - 42, left, right

    # 获取顶象验证码截图
    def getDxVerifyImageScreenshot(self):
        dx_verify_image_screenshot = self.browser.get_screenshot_as_png()
        dx_verify_image_screenshot = Image.open(BytesIO(dx_verify_image_screenshot))
        return dx_verify_image_screenshot

    # 获取顶象验证码图片
    def getDxVerifyImage(self, image_name='dx.png'):
        top, bottom, left, right = self.getDxVerifyImagePosition()
        dx_verify_image_screenshot = self.getDxVerifyImageScreenshot()
        dx = dx_verify_image_screenshot.crop((left, top, right, bottom))
        dx.save(image_name)
        return dx

    # 获取顶象验证码滑块对象
    def getDxVerifySlider(self):
        dx_verify_slider = self.explicit_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'dx_captcha_basic_slider')))
        return dx_verify_slider

    # 判断顶象验证码图片前后两张同一位置的像素是否相同
    def verifyPixelEqual(self, verify_image_font, verify_image_behind, x, y):
        # 获取两张图片的像素点
        verify_image_font_pixel = verify_image_font.load()[x, y]
        verify_image_behind_pixel = verify_image_behind.load()[x, y]
        # 设置比较的阈值
        threshold_value = 60
        # 如果绝对值均在阈值之内，则代表像素点相同，否则代表不相同的像素点，也就是缺口的位置
        if abs(verify_image_font_pixel[0] - verify_image_behind_pixel[0]) < threshold_value \
                and abs(verify_image_font_pixel[1] - verify_image_behind_pixel[1]) < threshold_value \
                and abs(verify_image_font_pixel[2] - verify_image_behind_pixel[2]) < threshold_value:
            return True
        else:
            return False

    # 获取顶象验证码缺口的偏移量
    def getNotch(self, verify_image_front, verify_image_behind):
        image_left = 60
        for i in range(image_left, verify_image_front.size[0]):
            for j in range(verify_image_front.size[1]):
                if not self.verifyPixelEqual(verify_image_front, verify_image_behind, i, j):
                    image_left = i
                    return image_left
        return image_left

    # 获取顶象滑块移动轨迹
    def getDxSliderTrack(self, distance):
        # 储存移动轨迹
        dx_slider_track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 设置初速度
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正 2
                a = 2
            else:
                # 加速度为负 3
                a = -3
            # 设置初速度为v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0 * t + 1 / 2 * a * t ^ 2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            dx_slider_track.append(round(move))
        return dx_slider_track

    # 移动顶象滑块
    def moveDxSlider(self, dx_slider, dx_slider_track):
        ActionChains(self.browser).click_and_hold(dx_slider).perform()
        for x in dx_slider_track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    # 开始登录鱼C
    def startLogin(self):
        # 打开鱼C并输入用户信息
        self.loginFishc()
        # 点击登录按钮
        login_button = self.explicit_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pn')))
        login_button.click()
        # 获取顶象验证码图片
        dx_verify_image_front = self.getDxVerifyImage('dx1.png')
        dx_verify_slider = self.getDxVerifySlider()
        dx_verify_slider.click()
        # 获取顶象验证码缺口图片
        dx_verify_image_behind = self.getDxVerifyImage('dx2.png')
        # 获取缺口位置
        notch = self.getNotch(dx_verify_image_front, dx_verify_image_behind)
        print('缺口位置:', notch)
        # 减去缺口位移
        notch -= BORDER
        # 获取移动轨迹
        dx_slider_track = self.getDxSliderTrack(notch)
        self.moveDxSlider(dx_verify_slider, dx_slider_track)

if __name__ == '__main__':
    login_fishc = LoginFishc()
    login_fishc.startLogin()
