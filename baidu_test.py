import requests
import json
import base64
from aip import AipFace
from 百度云_人脸识别.config import API_Key,Secret_Key,AppId

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_Key,Secret_Key)
header={'Content-Type':'application/json; charset=UTF-8'}

def get_access_token():#获取 access_token
    res = requests.post(host).content.decode('utf-8')
    res=json.loads(res)
    if 'error' in res:
        print('解析失败')
    else:
        access_token=res['access_token']
        # print(access_token)
        return access_token

def trans_base64(path):# 对图片进行base64编码
    with open(path,'rb') as f:
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        s=str(encodestr, 'utf-8')
        # print(s)
        return s

def check_img(flag,path):#面部识别
    cli=AipFace(AppId,API_Key,Secret_Key)
    image, image_type='',''
    if flag=='1':
        image=path
        image_type = 'URL'
    elif flag=='2':
        image=trans_base64(path)
        image_type = 'BASE64'
    options={}
    options['face_field']='age,beauty'
    options['max_face_num']=1
    options['face_type']='LIVE'
    res=cli.detect(image,image_type,options)
    print(res)
    if res['error_code']==0:
        print('读取成功')
        face_num=res['result']['face_num']
        face_age=res['result']['face_list'][0]['age']
        face_beaty=res['result']['face_list'][0]['beauty']
        print('人脸数量',face_num)
        print('人脸年龄',face_age)
        print('颜值',face_beaty)
        return face_num,face_age,face_beaty
    else:
        print('读取失败')


def check_face(flag1,flag2,path_1,path_2):#对比图片
    url='https://aip.baidubce.com/rest/2.0/face/v3/match'
    options=[{'image':'','image_type':'','face_type':'LIVE','quality_control':'LOW'},
             {'image':'','image_type':'','face_type':'LIVE','quality_control':'LOW'}]
    access_token=get_access_token()#得到access_token
    full_url=url+"?access_token=" + access_token
    if flag1=='1':#通道1 url
        if flag2=='1':#通道2 url
            options[0]['image']=''
            options[0]['image_type'] = 'URL'
            options[1]['image'] = ''
            options[1]['image_type'] = 'URL'
        elif flag2=='2':#通道2 base64
            options[0]['image']=''
            options[0]['image_type'] = 'URL'
            options[1]['image'] = trans_base64(path_2)
            options[1]['image_type'] = 'BASE64'
    elif flag1=='2':#通道1 base64
        if flag2=='1':#通道2 url
            options[0]['image']=trans_base64(path_1)
            options[0]['image_type'] = 'BASE64'
            options[1]['image'] = ''
            options[1]['image_type'] = 'URL'
        elif flag2=='2':#通道2 base64
            options[0]['image']=trans_base64(path_1)
            options[0]['image_type'] = 'BASE64'
            options[1]['image'] = trans_base64(path_2)
            options[1]['image_type'] = 'BASE64'
    res=requests.post(full_url,data=json.dumps(options),headers=header).content.decode('utf-8')
    print(res)
    res=json.loads(res)
    if res['error_code']==0:
        print('读取成功')
        face_res=res['result']['score']
        print('人脸相似度',face_res)
        return face_res
    else:
        print('读取失败')

# trans_base64('1.jpg')
if __name__ == '__main__':
    # check_img('2','image/1.jpg')

    check_face('2','2','image/1.jpg','image/2.jpg')
