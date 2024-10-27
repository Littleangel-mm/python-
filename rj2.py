# import tkinter as tk
# import subprocess
# import os

# # 文件夹路径
# download_folder = 'sp\\'
# if not os.path.exists(download_folder):
#     os.mkdir(download_folder)

# # 创建主窗口
# root = tk.Tk()
# root.title("万能下载器")

# # 设置窗口大小
# root.geometry('360x80+150+150')

# # 下载功能实现
# def download():
#     link = f'you-get -o {download_folder} {Key_word.get()}'
#     print("少女祈祷中...")
#     print(link)
#     # 使用 subprocess.run 执行命令，确保路径在 Windows 下可以被识别
#     subprocess.run(f'cmd /c {link}', shell=True)

# # 清空输入框
# def clear():
#     Key_word.set('')

# # 设置文本内容
# txt = tk.Label(text='请输入下载网址:', font=("Arial", 12))
# txt.grid(row=0, column=0)

# # 设置可变变量
# Key_word = tk.StringVar()

# # 创建输入框
# e = tk.Entry(root, textvariable=Key_word)
# e.grid(row=0, column=1)

# # 创建下载按钮
# bt = tk.Button(text="下载", command=download)
# bt.grid(row=0, column=2)

# # 创建清空按钮
# qk = tk.Button(text='清空', command=clear)
# qk.grid(row=0, column=3)

# # 进入主循环
# root.mainloop()


import tkinter as tk
import subprocess
import os

# 文件夹路径
download_folder = 'sp\\'
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

# 创建主窗口
root = tk.Tk()
root.title("万能下载器")

# 设置窗口大小
root.geometry('360x80+150+150')

# 下载功能实现
def download_all():
    link = f'you-get --playlist -o {download_folder} {Key_word.get()}'
    print("正在下载网页上全部视频...")
    print(link)
    # 使用 subprocess.run 执行命令，确保路径在 Windows 下可以被识别
    subprocess.run(f'cmd /c {link}', shell=True)

# 清空输入框
def clear():
    Key_word.set('')

# 设置文本内容
txt = tk.Label(text='请输入下载网址:', font=("Arial", 12))
txt.grid(row=0, column=0)

# 设置可变变量
Key_word = tk.StringVar()

# 创建输入框
e = tk.Entry(root, textvariable=Key_word)
e.grid(row=0, column=1)

# 创建下载按钮
bt = tk.Button(text="下载全部视频", command=download_all)
bt.grid(row=0, column=2)

# 创建清空按钮
qk = tk.Button(text='清空', command=clear)
qk.grid(row=0, column=3)

# 进入主循环
root.mainloop()

