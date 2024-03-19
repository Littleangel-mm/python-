import requests
import re
import os

#网易云的爬取

#新建文夹夹
filename = 'xtsdpc\\'
if not os.path.exists(filename):
    os.mkdir(filename)

url = 'https://music.163.com/discover/toplist?id=19723756'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}
response = requests.get(url = url,headers=headers)
# print(response.text)

#正则表达，获取歌名和id
html_data = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a>',response.text)
# print(html_data)

#遍历网页的数据，使用接口下载
for num_id,title in html_data:
# http://music.163.com/song/media/outer/url?id={music}.mp3
    music_url = f'http://music.163.com/song/media/outer/url?id={num_id}.mp3'
    music_content=requests.get(url=music_url,headers=headers).content
    #保存
    with open(filename+ title +'.mp3',mode='wb') as f:
        f.write(music_content)

print(num_id,title)





