#下载视频的小软件

import tkinter as tk
import subprocess
import os

filename = 'sp\\'
if not os.path.exists(filename):
    os.mkdir(filename)


root = tk.Tk()
root.title("万能下载器")

#设置窗口大小
root.geometry('360x50+150+150')

#下载功能实现
def download():
    link = f'you-get -o sp {Key_word.get()}'
    print("少女祈祷中...")
    print(link)
    subprocess.run(link,shell=True)



def clear():
    e.delete(0,'end')

# 设置文本内容
txt = tk.Label(text='请输入下载网址:',font=80)
txt.grid(row=0,column=0)



#设置可变变量
Key_word = tk.StringVar()


#整一个输入框框
e = tk.Entry(root,textvariable=Key_word)
e.grid(row=0,column=1)

#下载按钮
bt = tk.Button(text="下载",command=download)
bt.grid(row=0,column=2)


#清空
qk = tk.Button(text='清空',command=clear)
qk.grid(row=0,column=3)



root.mainloop()