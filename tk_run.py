from tkinter import Label, END, messagebox, Tk, StringVar, PhotoImage
from tkinter.ttk import Button, Entry, Radiobutton
from tkinter.filedialog import askopenfilename
from 百度云_人脸识别.baidu_test import *
import cv2
import os, re


class App(object):
    def __init__(self):
        self.w = Tk()
        self.w.title('图片识别器')
        self.w.geometry('500x350')
        self.creat_res()
        self.res_config()
        self.w.mainloop()

    def creat_res(self):  # 布局控件
        self.pic_var1 = StringVar()  # 图片1
        self.pic_var2 = StringVar()  # 图片2
        self.L_info = Label(self.w, fg='#1E90FF', text='请输入网络图片地址或者选择本地图片', bg='#E3E3E3')
        self.E_pic1 = Entry(self.w, textvariable=self.pic_var1)
        self.E_pic2 = Entry(self.w, textvariable=self.pic_var2)
        self.B_pic1 = Button(self.w, text='选择')
        self.B_pic2 = Button(self.w, text='选择')
        self.L_pic1_info = Label(self.w, bg='#63B8FF')
        self.L_pic2_info = Label(self.w, bg='#63B8FF')
        self.L_pic1 = Label(self.w, bg='#E3E3E3')
        self.L_pic2 = Label(self.w, bg='#E3E3E3')
        self.B_go = Button(self.w, text='GO')
        self.L_message = Label(self.w, bg='#E3E3E3')
        self.res_place()

    def res_place(self):
        self.L_info.place(x=10, y=6, width=260, height=30)
        self.E_pic1.place(x=10, y=45, width=200, height=30)
        self.E_pic2.place(x=270, y=45, width=200, height=30)
        self.B_pic1.place(x=170, y=85, width=40, height=28)
        self.B_pic2.place(x=430, y=85, width=40, height=28)
        self.L_pic1_info.place(x=10, y=85, width=150, height=30)
        self.L_pic2_info.place(x=270, y=85, width=150, height=30)
        self.L_pic1.place(x=10, y=120, width=200, height=200)
        self.L_pic2.place(x=270, y=120, width=200, height=200)
        self.B_go.place(x=215, y=150, width=50, height=50)
        self.L_message.place(x=280, y=6, width=215, height=30)

    def res_config(self):  # 配置文件
        self.B_pic1.config(command=self.file_path1_config)
        self.B_pic2.config(command=self.file_path2_config)
        self.B_go.config(command=self.contrast_pics)

    def file_path1_config(self):
        # 配置打开文件路径1
        self.path_1 = askopenfilename()
        self.pic_var1.set(self.path_1)
        self.view_pics1(self.pic_var1.get())
        self.L_pic1.config(image=self.ima1)

    def file_path2_config(self):
        # 配置打开文件路径2
        self.path_2 = askopenfilename()
        self.pic_var2.set(self.path_2)
        self.view_pics2(self.pic_var2.get())
        self.L_pic2.config(image=self.ima2)

    def change_jpg_to_png(self, a):#转换图片格式
        print('转换图片格式')
        print(a)
        img = cv2.imread(a)
        new_name=a.replace('jpg','png')
        # new_file='image/'+new_name.split('/')[-1]
        cv2.imwrite(new_name,img)
        print('转换完成')
        return new_name

    def view_pics1(self, path):  # 显示打开的照片
        print('显示')
        print(path)
        flag=''
        if re.match('[c-zC-Z]:/.+.jpg', path):
            new_name=self.change_jpg_to_png(path)
            self.ima1 = PhotoImage(file=new_name)
        elif re.match('[c-zC-Z]:/.+.png', path):
            self.ima1 = PhotoImage(file=path)
        face_num, face_age, face_beaty=self.get_pic_info(flag,path)
        self.L_pic1_info.config(text='人脸:{} 年龄:{} 颜值:{:.2f}'.format(face_num, face_age, face_beaty))


    def view_pics2(self, path):  # 显示打开的照片
        print('显示')
        print(path)
        flag=''
        if re.match('[c-zC-Z]:/.+.jpg', path):
            new_name=self.change_jpg_to_png(path)
            self.ima2 = PhotoImage(file=new_name)
        elif re.match('[c-zC-Z]:/.+.png', path):
            self.ima2 = PhotoImage(file=path)
        face_num, face_age, face_beaty=self.get_pic_info(flag,path)
        self.L_pic2_info.config(text='人脸:{} 年龄:{} 颜值:{:.2f}'.format(face_num, face_age, face_beaty))


    def get_pic_info(self,flag,path):#获得图片信息
        if re.match('http.+.[jpg]|[png]]',path):#如果匹配url
            flag='1'
        elif re.match('[c-zC-Z]:/.+.[png]|[jpg]]',path):#如果匹配本地图片base64
            flag='2'
        face_num,face_age,face_beaty=check_img(flag,path)
        return face_num,face_age,face_beaty

    def contrast_pics(self):#对比图片
        path1=self.pic_var1.get()
        path2=self.pic_var2.get()
        flag1,flag2='',''
        if re.match('http.+.[jpg]|[png]]',path1):#如果匹配url
            flag1='1'
        elif re.match('[c-zC-Z]:/.+.[png]|[jpg]]',path1):#如果匹配本地图片base64
            flag1='2'
        if re.match('http.+.[jpg]|[png]]',path2):#如果匹配url
            flag2='1'
        elif re.match('[c-zC-Z]:/.+.[png]|[jpg]]',path2):#如果匹配本地图片base64
            flag2='2'
        face_res=check_face(flag1,flag2,path1,path2)
        self.L_message.config(text='两张图片相似度{:.2f}'.format(face_res))


a = App()
