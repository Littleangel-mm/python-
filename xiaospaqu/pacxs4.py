
import requests
from bs4 import BeautifulSoup
import time

# 小说基础URL
base_url = "https://wap.biqige.info/0/573/"
output_file = "蛊真人.txt"

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}

# 抓取并保存章节内容
def fetch_and_save_chapter(chapter_url):
    response = requests.get(chapter_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # 定位内容部分，确认使用正确的 class
        content = soup.find("div", class_="novelcontent")  # 确保这个 class 是正确的
        title = soup.find("title")  # 获取章节标题

        # 如果标题中包含特定字符，提取所需部分
        if title:
            chapter_title = title.get_text().split(" - ")[0]  # 可能需要调整，根据实际格式
        else:
            chapter_title = "未知章节"

        if content:
            with open(output_file, "a", encoding="utf-8") as file:
                file.write(chapter_title + "\n")  # 使用获取到的章节标题
                file.write(content.get_text(separator="\n") + "\n\n")
            print(f"已保存章节：{chapter_title}")
        else:
            print(f"章节内容未找到: {chapter_url}")
    else:
        print(f"无法访问章节：{chapter_url}，状态码：{response.status_code}")

# 抓取某一章节的所有分页
def fetch_chapter_with_pagination(chapter_id):
    page_number = 1  # 从第一页开始
    while page_number<=3:
        chapter_url = f"{base_url}{chapter_id}-{page_number}.html"  # 拼接章节URL
        response = requests.get(chapter_url, headers=headers)

        if response.status_code == 200:
            fetch_and_save_chapter(chapter_url)
            page_number += 1  # 进入下一页
            time.sleep(1)  # 添加延时，避免被封禁
        else:
            # 如果返回状态码不是200，说明没有更多的页面了
            print(f"章节 {chapter_id} 的所有页面已抓取完毕。")
            break

# 抓取所有章节
def fetch_all_chapters(start_chapter, end_chapter):
    for chapter_id in range(start_chapter, end_chapter + 1):
        fetch_chapter_with_pagination(chapter_id)  # 抓取每个章节的所有页面
        time.sleep(1)  # 添加延时，避免被封禁

# 调用函数，开始抓取章节
fetch_all_chapters(start_chapter=517662, end_chapter=19765683)




