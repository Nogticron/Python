from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import re
import csv

# ブラウザーを起動
options = Options()
options.add_argument('--headless')
# Chromeのドライバを得る
browser = webdriver.Chrome(chrome_options=options)

url = "https://www.carsensor.net/usedcar/search.php?SKIND=1"

# 暗黙的な待機を最大3秒行う(サーバーの負担軽減)
browser.implicitly_wait(3)
# URLを読み込む
browser.get(url)
# htmlを取得
html = browser.page_source
# 「メーカー 車種」選択ボタンをクリック
browser.find_element_by_id('shashuAnc').click()
# HTMLを解析する --- (※3)
soup = BeautifulSoup(html, "html.parser")
# メーカー名を取得
makers = soup.find_all("a","js_makerMenu",href="#")
makers_list = []
# 除外する項目
skip_list = ["こだわらない","国産車その他","輸入車その他"]

for maker in makers:
  maker = maker.text
  # 正規表現で余分なものを取る
  maker = re.sub(r'\(\d*\)', "", maker) #(数字)
  maker = re.sub(r'\s', "", maker) #空白
  #除外項目をスキップ
  if not maker in skip_list:
    makers_list.append(maker)

#csvに書き込み
with open('makers.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerow(makers_list)

# ブラウザを終了
browser.quit()