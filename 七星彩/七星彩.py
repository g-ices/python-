import shutil
import tkinter
import requests
from lxml import etree
from collections import Counter
from matplotlib import pyplot
from tkinter import *
import tkinter.filedialog


class Data_Spider(object):
    def spider(self):
        """
        爬虫
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        url = 'http://datachart.500.com/qxc/history/inc/history.php'
        try:
            newest_resp = requests.get(url, headers=headers)
            newest_html = etree.HTML(newest_resp.text)
            newest_page = newest_html.xpath('//*[@id="end"]/@value')
            all_data_url = f'http://datachart.500.com/qxc/history/inc/history.php?limit={newest_page[0]}&start=0&end={newest_page[0]}'
            all_data_resp = requests.get(all_data_url, headers=headers)
            all_data_html = etree.HTML(all_data_resp.text)
            all_data = all_data_html.xpath('//*[@class="cfont2"]/text()')
            all_data_time = all_data_html.xpath('//*[@id="tablelist"]//tr/td[5]/text()')
            return all_data
        except Exception as e:
            return []


class Data_Handle(object):
    def data_handle(self, all_data, front_manay, front_stage):
        """
        数据处理
        :param all_data:
        :return:
        """

        all_data = [''.join(i.split(' '))[front_manay[0]:front_manay[1]] for i in all_data]
        data = [i for i in all_data[1:front_stage + 1]]
        return data

    def data_show(self, data, front_manay, front_stage):
        """
        数据可视化
        :param data:
        :return:
        """
        data_group = {}
        for keys, values in Counter(data).items():
            if values != 1:
                data_group[keys] = values
        xticks = [int(i) for i in data_group.keys()]
        yticks = [i for i in data_group.values()]
        pyplot.bar(xticks, yticks, align='center')
        pyplot.xticks(xticks, xticks)
        pyplot.rcParams['font.sans-serif'] = ['SimHei']
        pyplot.rcParams['axes.unicode_minus'] = False

        pyplot.ylabel('次数展示')
        pyplot.xlabel('出现的数字')
        if front_manay[1] - front_manay[0] == 1:
            front_manay = str(front_manay[1])
        else:
            front_manay = str(front_manay[0] + 1) + "-" + str(front_manay[1])
        pyplot.title(f'七星彩前{str(front_stage)}期第{front_manay}个数字出现次数图示')
        pyplot.savefig('seven_colour.png', bbox_inches='tight')
        shutil.copyfile('seven_colour.png', 'seven_colour.ico')
        pyplot.close()
        dic = {}
        li = []
        for i, j in zip(xticks, yticks):
            dic[i] = j
            li.append(i)
        li.sort()
        xticks, yticks = [i for i in li], [dic[i] for i in li]
        return xticks, yticks


# pythonGUI
class Seven_Colour(object):
    def __init__(self, all_data):
        self.all_data = all_data
        self.root = tkinter.Tk()
        self.root.title("七星彩小工具")
        self.root.geometry('800x700')

        self.canvas = tkinter.Canvas(self.root, height=450, width=580)  # 创建画布
        self.label_account = tkinter.Label(self.root, text='第几位: ')
        self.label_password = tkinter.Label(self.root, text='前多少期: ')
        self.input_email = tkinter.Entry(self.root, width=30)
        self.input_password = tkinter.Entry(self.root, width=30)
        self.login_button = tkinter.Button(self.root, command=self.backstage_interface, text="展示", width=10)

    def gui_arrang(self):
        self.label_account.place(x=250, y=480)
        self.label_password.place(x=250, y=510)
        self.input_email.place(x=310, y=480)
        self.input_password.place(x=310, y=510)
        self.login_button.place(x=370, y=560)

    def logger_note(self, logmsg_in):
        # 创建一个日志框
        self.log_data_Text = tkinter.Text(self.root, width=85, height=6)  # 日志框
        self.log_data_Text.place(x=100, y=600)
        self.log_data_Text.insert(CURRENT, logmsg_in)

    def backstage_interface(self):
        front_manay = self.input_email.get().ljust(10, " ").strip()
        front_stage = self.input_password.get().ljust(10, " ").strip()
        if not self.all_data:
            self.logger_note('网络错误')
        if front_manay and front_stage:
            try:
                front_manay = int(front_manay)
                front_manay = [front_manay - 1, front_manay]
            except:
                if ':' in front_manay:
                    front_manay = [int(i) for i in front_manay.split(':')]
                    front_manay = [front_manay[0] - 1, front_manay[1]]
                else:
                    self.logger_note('第几位: 输入错误')
            try:
                front_stage = int(front_stage)
            except:
                self.logger_note('前多少期: 输入错误')

            data_handle = Data_Handle()
            data = data_handle.data_handle(self.all_data, front_manay, front_stage)
            xticks, yticks = data_handle.data_show(data, front_manay, front_stage)
            xticks = '\t'.join([str(i) for i in xticks])
            yticks = '\t'.join([str(i) for i in yticks])
            self.logger_note('数字:\t' + xticks + '\n次数\t' + yticks)
            self.image_file = tkinter.PhotoImage(file='seven_colour.ico')  # 加载图片文件
            self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.image_file)  # 将图片置于画布上
            self.canvas.pack(side='top')  # 放置画布（为上端）


def run():
    all_data = Data_Spider().spider()
    a = Seven_Colour(all_data)
    a.gui_arrang()
    tkinter.mainloop()


if __name__ == '__main__':
    run()
