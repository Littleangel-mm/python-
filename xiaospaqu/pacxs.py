import requests
from bs4 import BeautifulSoup

# 目标URL
url = "https://wap.biqige.info/0/573/517662.html"

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}

# 保存文件路径
output_file = "chapter_517662.txt"

# 抓取并保存章节内容
def fetch_and_save_chapter(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # 根据页面结构找到内容部分
        content = soup.find("div", class_="novelcontent")  # 根据实际class调整
        if content:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(content.get_text(separator="\n"))
            print("章节内容保存成功")
        else:
            print("章节内容未找到")
    else:
        print("无法访问该章节")

# 执行函数
fetch_and_save_chapter(url)

