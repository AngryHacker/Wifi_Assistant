# -*- coding:utf-8 -*-
__author__ = 'AngryRookie'

from Tkinter import *
from PIL import Image, ImageTk
import os
import subprocess
import sys

#获得当前脚本所在目录
def getpwd():
    pwd = sys.path[0]
    if os.path.isfile(pwd):
        pwd = os.path.dirname(pwd)
    return pwd

#窗口主体
class App():
     def __init__(self, master):

         #标题
         dirname = getpwd() + '\image\\';
         image = Image.open(dirname + 'head.jpg')
         photo = ImageTk.PhotoImage(image)
         self.top = Label(image = photo, width = 480, height = 100)
         self.top.image = photo
         self.top.grid(row = 0,column = 0, columnspan = 6)

         #名称标签
         font = "Times 10"
         self.nlabel = Label(text = '名称：',height = 2,font = font)
         self.nlabel.grid(row = 1, column = 0,sticky = E,pady = 20)
         
         #密码标签
         self.plabel = Label(text = '密码：',height = 2,font = font)
         self.plabel.grid(row = 2, column = 0,sticky = E)

         # Wifi 名称 和 密码 输入框
         #获取用户上一次最后设置的名称和密码
         dirname2 = getpwd() + '\config\\';
         file = open(dirname2 + 'pass.txt','r')
         c1 = file.readline()
         c2 = file.readline()
         c1 = c1.strip('\n')
         c2 = c2.strip('\n')
         file.close()
         v1 = StringVar()
         v2 = StringVar()
         v1.set(c1)
         v2.set(c2)
         vcmd = (master.register(self.OnValidate),'%S')
         self.nentry = Entry(master,textvariable = v1)
         self.nentry.grid(row = 1, column = 1, columnspan = 3,sticky = W,padx = 5)
         self.pentry = Entry(master,textvariable = v2, validate="key", validatecommand=vcmd)
         self.pentry.grid(row = 2, column = 1, columnspan = 3,sticky = W,padx = 5)
         self.name = self.nentry.get()
         self.password = self.pentry.get()

         #右侧图片
         photo2 = PhotoImage(file = dirname + 'kaka.gif')
         self.right = Label(master, image = photo2,padx = 500)
         self.right.photo = photo2
         self.right.grid(row = 1, column = 3, rowspan = 2, columnspan = 3,sticky = S,pady = 5)

         #启动按钮
         font1 = "Helvetica 12 bold"
         self.start = Button(master, text = '启动', command = self.start, width = 6, height = 2, font = font1)
         self.start.grid(row = 4, column = 0,rowspan = 3, columnspan = 2, sticky = E, padx = 40, pady = 10)

         #停止按钮
         self.stop = Button(master, text = '停止',command = self.stop, width = 6, height = 2, font = font1)
         self.stop.grid(row = 4, column = 2,rowspan = 3, columnspan = 2, sticky = W,padx = 20, pady = 10)

         #状态栏
         font2 = "Helvetica 10 bold"
         self.state = Label(master, text = '状态:', font = font2)
         self.state.grid(row = 7, column = 0, sticky = E)
         
         self.s = StringVar()
         self.s.set("尚未启动 Wifi ...")
         self.state = Label(master, textvariable = self.s, font = font2)
         self.state.grid(row = 7, column = 1, columnspan = 2, sticky = W)

         #声明
         font3 = "Times 10"
         ending = '\n    声明：本软件最终解释权归作者 AngryRookie 所有！\n软件虽小，bug很多！请小伙伴们好好对待它，不要把它玩坏了！\n 联系方式：QQ: 243695261   微博请粉：@涯_锦城'
         self.end = Label(master, text = ending, font = font3)
         self.end.grid(row = 8, column = 0, sticky = E, rowspan = 2, columnspan = 5)

         

     #打开Wifi
     def start(self):
         dirname = getpwd() + '\config\\';

         #检测 Wifi 名称 和密码有无修改
         if str(self.nentry.get()) == str(self.name) and str(self.pentry.get()) == str(self.password) :
              command = "netsh wlan start hostednetwork" + ' >null'
              os.system(command)
              self.s.set('Wifi 已启动！')
         else:
              self.name = self.nentry.get()
              self.password = self.pentry.get()

              #弹出密码设置不正确窗口
              if len(self.password) < 8:
                   top = Toplevel()
                   top.title("Invalid Password!")
                   top.geometry('150x80')
                   top.maxsize(width = 150,height = 80)
                   top.minsize(width = 150,height = 80)

                   font = "Times 10 bold"
                   about = "密码应该至少8位！"
                   msg = Message(top, text = about,font = font,justify=LEFT,anchor=E)
                   msg.pack()
                   
                   font = "Times 10"
                   button = Button(top, text="确定",command=top.destroy,width = 4,height = 3,font = font)
                   button.pack()
                   return 
              #将修改的名称和密码写入文件
              file = open(dirname + 'pass.txt','w')
              file.write("%s\n%s" % (self.name, self.password))
              file.close()
              command1 = "netsh wlan set hostednetwork mode=allow ssid=" + self.name + " key=" + self.password
              command2 = "netsh wlan start hostednetwork"
              command = command1 + ' >null' + '&' + command2 + ' >null'
              #两种方式运行开启命令，第一种为接下来的第一行，第二种为接下来的第二行和第三行
              os.system(command)   #使用 python os 模块
              #proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE) #使用子进程
              #stdout, stderr = proc.communicate(command)
              self.s.set('Wifi 已启动！')

     #关闭Wifi
     def stop(self):
         command = "netsh wlan stop hostednetwork" + ' >null'
         os.system(command)
         #proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
         #stdout, stderr = proc.communicate(command)
         self.s.set('Wifi 已停止！')

     #检验用户输入，必须为数字
     def OnValidate(self,S):
          flag = True
          for x in S:
               if not x.isdigit():
                    flag = False
          return flag

         
         

root = Tk()
root.title('一键Wifi小助手')
root.geometry('480x380')
root.iconbitmap(getpwd() + '\image\\' + 'icon.ico')
root.maxsize(width = 480,height = 380)
root.minsize(width = 480,height = 380)

app = App(root)

mainloop()



         
