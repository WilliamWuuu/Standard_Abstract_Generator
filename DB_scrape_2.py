from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import re
from time import sleep

def clean_filename(filename):
    # 移除文件名中的无效字符
    return re.sub(r'[<>:"/\\|?*]', '', filename)


# 模拟浏览器打开动态网页获取pdf文件链接id目录
driver = webdriver.Edge()
driver.get("https://dbba.sacinfo.org.cn/stdList")

link_list = []
driver.implicitly_wait(30)

for n in range(600):
    for link in driver.find_elements(By.XPATH, "//tr//a[@href]"):
        link_list.append(link.get_attribute('href'))
    next_page = driver.find_element(By.XPATH, '//li[@class="page-item page-next"]//a[@class="page-link"]')
    next_page.click()
    sleep(1)

# 本地设置保存pdf文件的目录
pdf_dir = "pdf_files"
os.makedirs(pdf_dir, exist_ok=True)

# 遍历链接id目录发送请求
for link in link_list:
    url = link
    # 参数封装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    for page in range(1, 2):
        page = str(page)
        data = {
            "current": page,
            "size": "15",
            "key": "",
            "ministry": "",
            "industry": "",
            "pubdate": "",
            "date": "",
            "status": "现行",
        }

        # 发送请求并获取响应
        response = requests.get(url=url, headers=headers)

        # 使用BeautifulSoup解析响应内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找 <a> 标签，找到链接到 PDF 文件的元素
        pdf_link = soup.find("a", title="点击查看标准全文")
        pdf_name_link = soup.find("b")
        if pdf_link != None:
            pdf_relative_url = pdf_link["href"]

            # 添加协议部分
            pdf_full_url = "https://dbba.sacinfo.org.cn" + pdf_relative_url

            # 设置文件名
            pdf_filename = pdf_name_link.text
            pdf_filename = clean_filename(pdf_filename + ".pdf")

            # 发送请求获取 PDF 文件内容
            pdf_response = requests.get(pdf_full_url)

            # 将 PDF 文件内容以二进制形式写入文件
            with open(os.path.join(pdf_dir, pdf_filename), "wb") as f:
                f.write(pdf_response.content)
                print(f"已下载 PDF 文件：{pdf_filename}")
