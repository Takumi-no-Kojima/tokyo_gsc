# -*- coding: utf-8 -*-

"""
ここではNewsPicks上の特定のユーザーが保存もしくはコメントした記事を全てスクレイピングします。
その後、自然言語処理で、タイトルで使われていた言葉を出てきた回数順に並んだものがcsvで出力されます。
ユーザーの番号さえ分かれば使用でき、複数を一気に調べることも可能です。
"""

from selenium import webdriver
import time
import pandas as pd
import MeCab
import analysis
import collections


driver = webdriver.Chrome(executable_path='/Users/takumi/Desktop/tokyougsc/chromedriver')

list = [] #ここに調べたい人全員の番号をいれる

for num in list:
    url = "https://newspicks.com/user/" + str(num)
    driver.get(url)

    e_user_name = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[1]/h1")
    user_name = e_user_name.text

    e_job = driver.find_element_by_class_name("job")
    job = e_job.text

    e_btn = driver.find_element_by_class_name("login")
    e_btn.click()

    e_username = driver.find_element_by_id("login-username")
    e_username.click()
    e_username.send_keys("") #ここにメールアドレス

    e_password = driver.find_element_by_id("login-password")
    e_password.click()
    e_password.send_keys("") #ここにパスワード

    e_login_btn = driver.find_element_by_class_name("form")
    e_login_btn = e_login_btn.find_element_by_class_name("login-btn")
    e_login_btn.click()

    for i in range (1, 30):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    all = driver.find_elements_by_class_name("news-card")

    article_list = []

    for one in all:
        article = one.find_element_by_tag_name("a").get_attribute("href")
        article_list.append(article)

    driver.close()


    article_word_list = []

    for item in article_list:
        url = "https://newspicks.com" + item
        driver.get(url)

        e_title = driver.find_eent_by_xpath("/html/body/div[4]/div[2]/div[2]/div/div[1]/div[2]/a/h1")
        article_word_list.append(e_title)

    # 下記の形態素分析については https://qiita.com/hyo_07/items/ba3d53868b2f55ed9941 を参考にした
    mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd") #辞書のパス

    def tokenize(text):
        node = mecab.parseToNode(text)
        while node:
            if node.feature.split(',')[0] == '名詞':
                yield node.surface.lower()
            node = node.next

    def get_words(contents):
        ret = []
        for content in contents:
            ret.append(get_words_main(content))
        return ret

    def get_words_main(content):
        return [token for token in tokenize(content)]

    words = analysis.get_words(article_word_list)

    collect = collections.Counter(words)

    out = pd.DataFrame(list(collect.items()), columns=['word', 'count'])
    out_name = user_name + "_" + job + ".csv"
    out.to_csv(out_name, index=False)

