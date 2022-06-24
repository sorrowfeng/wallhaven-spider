import requests      #爬虫
import re            #正则表达式
import os            #文件操作
import threading     #线程


class Spider(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exit = False

    def exit_spider(self):
        self.exit = True

    def set_message(self, callback_func):
        self.send_message = callback_func

    def set_progress(self, callback_func):
        self.update_progress = callback_func

    def set_finish(self, callback_func):
        self.download_finish = callback_func

    def get_url(self, base_url):
        if self.keyword=='toplist': #获取排行榜的url模板
            base_url=base_url+self.keyword+'?page='
        else: #获取基于关键词的url模板
            base_url=base_url+'search?q='+self.keyword+'&page='
        return base_url         #返回模板

    def get_img_url(self, base_url):
        header={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
        }  #模拟浏览器头部，伪装成用户
        img_url_list=[]  #创建一个空列表
        page_num=2 #"请输入下载页数:(一页24张)"
        now_num=1
        while True: #循环遍历每页
            if self.exit:
                self.update_progress(0)
                self.send_message('停止下载')
                return []
            new_url=base_url+str(now_num)   #将模板进行拼接得到每页壁纸完整的url(实质:字符串的拼接)
            page_text=requests.get(url=new_url,headers=header).text #获取url源代码
            ex='<a class="preview" href="(.*?)"'
            img_url_list+=re.findall(ex,page_text,re.S) #利用正则表达式从源代码中截取每张壁纸缩略图的url并全部存放在一个列表中
            if now_num==2:
                expage = '<span class="thumb-listing-page-num">2</span> / (.*?)</h2>'
                list = re.findall(expage, page_text, re.S)
                if len(list) > 0:
                    page_num = int(list[0])
                    self.send_message('总页数:'+str(page_num))
                    self.send_message('正在获取列表')
            if now_num == page_num:
                break
            now_num += 1
            if now_num > 2:
                self.update_progress(float(now_num) / float(page_num) * 100.0)

        return img_url_list #返回列表


    def download_img(self, img_url_list):
        if len(img_url_list) == 0:
            return

        header={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        } #模拟浏览器头部，伪装成用户
        if not os.path.exists('./wallpapers'):     #在目录下创建一个名为wallpapers的文件夹
            os.mkdir('./wallpapers')
        path='./wallpapers/'+self.keyword
        self.send_message("图片下载文件夹:"+path)
        self.send_message("开始下载")
        self.update_progress(0)

        if not os.path.exists(path):#在wallpapers文件夹下创建一个以关键词命名的子文件夹以存放此次下载的所有壁纸
            os.mkdir(path)
        for i in range(len(img_url_list)): #循环遍历列表，对每张壁纸缩略图的url进行字符串的增删获得壁纸原图下载的url  注：jpg或png结尾
            if self.exit:
                self.update_progress(0)
                self.send_message('停止下载，已经下载' + str(i) + '张图片')
                return
            x=img_url_list[i].split('/')[-1]  #获取最后一个斜杠后面的字符串
            a=x[0]+x[1] #获取字符串的前两位
            img_url='https://w.wallhaven.cc/full/'+a+'/wallhaven-'+x+'.jpg'  #拼接字符串,先默认jpg结尾
            code=requests.get(url=img_url,headers=header).status_code
            if code==404:    #若网页返回值为404，则为png结尾
                img_url='https://w.wallhaven.cc/full/'+a+'/wallhaven-'+x+'.png'
            img_data=requests.get(url=img_url,headers=header,timeout=20).content  #获取壁纸图片的二进制数据,加入timeout限制请求时间
            img_name=self.keyword+'-'+img_url.split('-')[-1] #生成图片名字
            img_path=path+'/'+img_name    #生成图片存储路径
            with open(img_path,'wb') as fp:    #('w':写入,'b':二进制格式)
                fp.write(img_data)
                self.send_message('['+str(i)+'/'+str(len(img_url_list))+']\t'+img_name+'下载成功')     #每张图片下载成功后提示
            self.update_progress(float(i) / float(len(img_url_list)) * 100.0)

    def set_word(self, word):
        self.keyword = word

    def run(self):
        self.exit = False
        url = 'https://wallhaven.cc/'
        self.send_message('开始爬取：'+url)
        self.send_message('关键字：'+self.keyword)
        base_url=self.get_url(url)
        img_url_list=self.get_img_url(base_url)
        self.download_img(img_url_list)
        self.download_finish()

