# -*- coding: utf-8 -*-
import undetected_chromedriver as webdriver
from undetected_chromedriver.options import ChromeOptions
from settings import *
from selenium.webdriver import ActionChains
from middlerware import Slide
import time
import platform


class Browser():
    """Browser Env : undetected_chromedriver + stealth.js
    headless_enable: 无头模式
    images_enable: 图像开关
    incognito_enable: 无痕模式
    logging_enable: 开启日志
    stealth_enable: stealth 伪装模式
    proxy: 启用代理, 格式：http://127.0.0.1:8888
    """
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--lang=en-us")

        if headless_enable:
            options.add_argument("--headless")

        if plugin_enable:
            options.add_argument('--disable-images')
            options.add_argument('--disable-plugins')
            options.add_argument('disable-audio')
            options.add_argument('disable-translate')

        if proxy:
            options.add_argument('--proxy-server=' + proxy)

        if logging_enable:
            options.add_argument('log-level=3')

        if incognito_enable:
            options.add_argument("--incognito")

        if platform.system().lower()=='linux':
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(driver_executable_path=driverpath, options=options)
        if stealth_enable:
            self.stealth_enable()

    def stealth_enable(self):
        with open(stealth_path,'r',encoding='utf-8') as file:
            stealth_min_js = file.read()
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": stealth_min_js
        })


    def start_request(self,url):
        self.browser.get(url)
        return self.browser


    def close(self):
        self.browser.close()
        self.browser.quit()


class BrowserApi():
    def __init__(self,browser):
        self.browser = browser

    def browser_ps(self,url):
        self.browser.get(url)
        return self.browser.page_source


    def browser_get(self, url):
        doc = self.browser.execute_script('''
            function queryData(url) {
               var p = new Promise(function(resolve,reject) {
                   var e={
                           "url":"%s",
                           "method":"GET"
                    };
                   var h = new XMLHttpRequest;
                   h.open(e.method, e.url, true);
                   h.setRequestHeader("salute-by","lx");
                   h.onreadystatechange =function() {
                        if(h.readyState === 4 && h.status  === 200) {
                            resolve(h.responseText);
                        } else {}
                   };
                   h.send(null);
                   });
                   return p;
                }
            var p1 = queryData('lx');
            res = Promise.all([p1]).then(function(result){
                    return result
            })
            return res
        ''' % (url))
        return doc[0]


    def browser_post(self, url, formdata=""):
        doc = self.browser.execute_script('''
                    function queryData(url) {
                       var p = new Promise(function(resolve,reject) {
                           var e={"url":"%s",
                                    "method":"POST",
                                    "data" : '%s'
                                  };
                           var h = new XMLHttpRequest;h.open(e.method, e.url, true);
                           h.setRequestHeader("accept","application/json, text/plain, */*");  
                           h.setRequestHeader("content-type","application/json;charset=UTF-8");
                           h.setRequestHeader("salute-by","lx");
                           h.onreadystatechange =function() {
                                if(h.readyState != 4) return;
                                if(h.readyState === 4 && h.status  ===200) {
                                   resolve(h.responseURL);
                                } else {
                                 }
                           };
                           h.send(e.data);
                           });
                           return p;
                        }
                    var p1 = queryData('lx');
                    res = Promise.all([p1]).then(function(result){
                    return result
                    })
                    return res;
        ''' % (url, formdata))
        return doc[0]


    def check_slide(self,bg_xpath,gap_xpath,slider_xpath,domain=None):
        """params:
            bg_xpath : 带缺口的背景图片的 xpath
            gap_xpath: 缺口滑块图片的 xpath
            slider_xpath: 待拖动滑块的 xpath
            domain: 图片doamin，非 http开头需补全链接
        """
        while 1:
            try:
                bg = self.browser.find_element_by_id(bg_xpath).get_attribute('src')
                gap = self.browser.find_element_by_xpath(gap_xpath).get_attribute('src')
                if not bg.startswith('http'):bg = domain+bg
                if not gap.startswith('http'):gap = domain+gap
                slide_app = Slide(gap=gap, bg=bg)
                distance = slide_app.discern()
            except:
                break
            try:
                slider = self.browser.find_element_by_xpath(slider_xpath)
                ActionChains(self.browser).click_and_hold(slider).perform()
                _tracks = slide_app.get_tracks(distance)
                new_1 = _tracks[-1] - (sum(_tracks) - distance)
                _tracks.pop()
                _tracks.append(new_1)
                for mouse_x in _tracks:
                    ActionChains(self.browser).move_by_offset(mouse_x, 0).perform()
                ActionChains(self.browser).release().perform()
                time.sleep(1)
            except:
                break
