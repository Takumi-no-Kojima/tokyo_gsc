# -*- coding: utf-8 -*-

"""
ここではNewsPicks上の特定の記事から全てのコメントをスクレイピングします。
そのコメントに関する情報全てをcsvで書き出します。
記事の番号さえ分かれば使用でき、複数を一気に調べることも可能です。
"""

from selenium import webdriver
import time
import pandas as pd


driver = webdriver.Chrome(executable_path='/Users/takumi/Desktop/tokyougsc/chromedriver')

list= [] #ここに調べたい記事の番号を全ていれる

for num in list:
    url = "https://newspicks.com/news/" + str(num)
    driver.get(url)

    e_title = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div/div[1]/div[2]/a/h1")
    title = e_title.text

    e_date = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[2]/span")
    date = e_date.text

    e_btn = driver.find_element_by_class_name("register-or-login")
    e_btn.click()

    e_link_btn = driver.find_element_by_class_name("go-login")
    e_link_btn.click()

    e_username = driver.find_element_by_id("login-username")
    e_username.click()
    e_username.send_keys("") #ここにメールアドレス

    e_password = driver.find_element_by_id("login-password")
    e_password.click()
    e_password.send_keys("") #ここにパスワード

    e_login_btn = driver.find_element_by_class_name("form")
    e_login_btn = e_login_btn.find_element_by_class_name("login-btn")
    e_login_btn.click()

    for i in range (1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    otherpick_btn = driver.find_element_by_class_name("show-other-pick")
    otherpick_btn.click()

    for i in range (1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    comment_boxes = []
    names = []
    jobs = []
    times = []
    comments = []
    counts = []
    user_profiles = []

    all = driver.find_elements_by_class_name("comment-row")

    for one in all:

        user = one.find_element_by_class_name("user-profile")

        e_name = user.find_element_by_class_name("name")
        name = e_name.text
        names.append(name)

        e_job = user.find_element_by_class_name("job")
        job = e_job.text
        jobs.append(job)

        e_time = user.find_element_by_class_name("picktime")
        time = e_time.text
        times.append(time)

        e_comment = one.find_eent_by_class_name("comment")
        comment = e_comment.text.split("\n")
        comments.append(comment)

        e_count = one.find_element_by_class_name("count")
        count = e_count.text
        counts.append(count)

    out = pd.DataFrame([names, jobs, times, comments, counts, user_profiles])
    out = out.T
    out_name = date + "_" + title + ".csv"
    out.to_csv(out_name, index=False)

    driver.close()

