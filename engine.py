# -*- coding: utf-8 -*-
from browserapi import Browser,BrowserApi
from db import insert_process,select_process,select_process_name,delete_process
from models import Process
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


def create_browser(url,name):
    bro = Browser()
    browser = bro.start_request(url)
    session_id = browser.session_id
    process_url = browser.command_executor._url
    insert_process(Process(session_id,name,process_url))


def attachToSession(session_id,url):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=url, desired_capabilities={})
    driver.session_id = session_id
    WebDriver.execute = original_execute
    return driver


def carry_browser(session_id,process_url,request_url,request_type,formdata):
    browser = attachToSession(session_id,process_url)
    broapi = BrowserApi(browser)
    if request_type=='get':
        result = broapi.browser_get(request_url)
    else:
        result = broapi.browser_post(request_url,formdata)
    return result


def close_browser(session_id,process_url,process_name):
    browser = attachToSession(session_id,process_url)
    browser.close()
    browser.quit()
    delete_process(process_name)


def select_all_process():
    return select_process()
<<<<<<< HEAD

=======
  
>>>>>>> b18b67a76d07979298f7a343ec5602532ccab217
