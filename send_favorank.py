#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

from selenium import webdriver


def send_favorank():
    Date = datetime.date.today()
    print(Date)
    driver = webdriver.Firefox(executable_path="/Users/kudouhibiki/Desktop/python_program/twitter_scraping/geckodriver")
    driver.get("https://buzz-matome.xyz/wp-login.php?loggedout=true")

    with open("scr_text.txt", "r", encoding="utf-8") as f:
        inputText = f.read()

    driver.find_element_by_id('user_login').send_keys("sh05")
    driver.find_element_by_id('user_pass').send_keys("roto2535")
    driver.find_element_by_id('wp-submit').click()

    time.sleep(3)
    print(inputText)

    driver.get("https://buzz-matome.xyz/wp-admin/post-new.php")
    driver.find_element_by_name('post_title').send_keys(str(Date.strftime("%Y年%m月%d日")) + "のバズツイートランキング")

    driver.find_element_by_id("content").send_keys(str(inputText))

    time.sleep(8)
    driver.execute_script("window.scrollTo(0, document.head.scrollHeight)")
    time.sleep(10)
    driver.find_element_by_xpath('//div[@id="publishing-action"]').click()
    # str(date.datetime.now().strptime('%Y年%m月%日')
    driver.close()
