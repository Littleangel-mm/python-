
# import os
# import requests
# import time

# # 创建存放视频的文件夹
# download_folder = 'nvpu'
# if not os.path.exists(download_folder):
#     os.makedirs(download_folder)

# # 基础 URL 和集数范围
# base_url = "https://play.xfvod.pro/X/X-%E6%96%B0%E6%9D%A5%E7%9A%84%E5%A5%B3%E4%BD%A3%E6%9C%89%E7%82%B9%E6%80%AA/"
# total_episodes = 11

# def download_video(episode_number, retries=3):
#     # 拼接每集的 URL
#     episode_url = f"{base_url}{episode_number:02}.mp4"
#     video_path = os.path.join(download_folder, f"episode_{episode_number:02}.mp4")
#     print(f"正在下载第 {episode_number} 集，保存为: {video_path}")

#     # 设置请求重试机制
#     for attempt in range(retries):
#         try:
#             # 发送请求，设置超时时间
#             response = requests.get(episode_url, stream=True, timeout=10)
            
#             # 检查请求状态
#             if response.status_code == 200:
#                 with open(video_path, "wb") as video_file:
#                     for chunk in response.iter_content(chunk_size=1024):
#                         if chunk:
#                             video_file.write(chunk)
#                 print(f"第 {episode_number} 集下载完成！\n")
#                 return
#             else:
#                 print(f"第 {episode_number} 集请求失败，状态码: {response.status_code}")
#                 break
#         except requests.RequestException as e:
#             print(f"第 {episode_number} 集下载失败，尝试 {attempt + 1}/{retries} 次。错误: {e}")
#             time.sleep(2)  # 等待 2 秒后重试

#     print(f"第 {episode_number} 集下载失败，跳过。")

# # 执行下载
# for episode in range(3, total_episodes + 1):
#     download_video(episode)
#     time.sleep(1)  # 等待 1 秒，避免请求过于频繁

# print("全部视频下载完成！")



#**********************************************************************
#加进度条
import os
import requests
import time
from tqdm import tqdm

# 创建存放视频的文件夹
download_folder = 'nvpu'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 基础 URL 和集数范围
base_url = "https://play.xfvod.pro/X/X-%E6%96%B0%E6%9D%A5%E7%9A%84%E5%A5%B3%E4%BD%A3%E6%9C%89%E7%82%B9%E6%80%AA/"
total_episodes = 11

def download_video(episode_number, retries=3):
    # 拼接每集的 URL
    episode_url = f"{base_url}{episode_number:02}.mp4"
    video_path = os.path.join(download_folder, f"episode_{episode_number:02}.mp4")
    print(f"正在下载第 {episode_number} 集，保存为: {video_path}")

    # 设置请求重试机制
    for attempt in range(retries):
        try:
            # 发送请求，获取文件大小
            response = requests.get(episode_url, stream=True, timeout=10)
            
            # 检查请求状态
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                with open(video_path, "wb") as video_file, tqdm(
                    total=total_size, unit='B', unit_scale=True, desc=f"第 {episode_number} 集"
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            video_file.write(chunk)
                            progress_bar.update(len(chunk))
                print(f"第 {episode_number} 集下载完成！\n")
                return
            else:
                print(f"第 {episode_number} 集请求失败，状态码: {response.status_code}")
                break
        except requests.RequestException as e:
            print(f"第 {episode_number} 集下载失败，尝试 {attempt + 1}/{retries} 次。错误: {e}")
            time.sleep(2)  # 等待 2 秒后重试

    print(f"第 {episode_number} 集下载失败，跳过。")

# 执行下载
for episode in range(1, total_episodes + 1):
    download_video(episode)
    time.sleep(1)  # 等待 1 秒，避免请求过于频繁

print("全部视频下载完成！")




