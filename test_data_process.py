import time
import os
from threading import Thread

class NodeParameters:
    '定义节点相关结构体变量，用类表示'
    def __init__(self):
        self.com_count = []  #通信次数，计算上电复位次数
        self.com_content = []   #通信内容
        '发送相关'
        self.send_count = [] #发送次数
        self.send_freq = []  #发送频点
        self.send_power = [] #发送功率
        self.send_datarate = []  #发送速率
        self.send_len = []   #发送数据长度
        self.send_tips_content = []  # 发送提示内容（超时帧、业务帧、入网请求帧、入网确认帧）
        '接收相关'
        self.recv_count = [] #接收次数
        self.recv_len = []   #接收数据长度
        self.recv_frame_num = [] #接收帧序号
        self.recv_rssi = []  #接收信号强度
        self.recv_snr = []   #接收信噪比
        self.recv_loss_count = []    #丢帧数
        self.recv_loss_percent = []  #丢包率
        self.send_package = []  #发送包（长包、中包、短包）

class GatewayParameters:
    '定义网关相关结构体变量，用类表示'
    def __init__(self):
        '接收相关'
        self.recv_node_label = []   #节点号
        self.recv_type = [] #接收数据类型
        self.recv_count = []    #接收帧计数
        self.recv_frame_num = []    #接收帧序号
        self.recv_channel = []  #接收通道号
        self.recv_freq = [] #接收频点
        self.recv_rssi = [] #接收信号强度
        self.recv_snr = []  #接收信噪比
        self.recv_len = []  #接收数据长度
        self.recv_datarate = [] #接收空中速率
        '发送相关'
        self.send_type = [] #发送数据类型
        self.send_freq = [] #发送频点
        self.send_power = []    #发送功率
        self.send_count = []    #发送计数
        self.send_len = []  #发送数据长度
        self.send_datarate = [] #发送空中速率

node_para = NodeParameters()    #节点全局变量
gw_para = GatewayParameters()   #网关全局变量

class GetInputTxt:
    '创建与输入txt文件相关的类，用于获取要处理的文件名与文件路径'
    '命名规则：文件名.txt = 模块属性（网关）+ 日期（年月日20200911）+ .txt'
    all_file_path = []  #定义所有文件路径
    txt_file_path = []  #定义所有txt文件路径

    def get_all_file(self,cwd):
        '闭包获取路径文件夹及子文件夹下的所有文件'
        get_dir = os.listdir(cwd)   #列出输入文件夹路径下的所有文件及子文件夹
        for i in get_dir:
            sub_dir = os.path.join(cwd, i)  #名称拼接
            if os.path.isdir(sub_dir):  #判断是否为文件夹
                GetInputTxt.get_all_file(self,sub_dir)    #闭包判断子文件夹
            else:
                GetInputTxt.all_file_path.append(sub_dir)

    def get_txt_file(self,file_name):
        '获取路径中的所有txt文件'
        GetInputTxt.get_all_file(self,file_name)
        for each_path in GetInputTxt.all_file_path:
            path_type = str.lower(each_path)
            if path_type.find('.txt') > 0:
                GetInputTxt.txt_file_path.append(each_path)
        GetInputTxt.all_file_path.clear()  # 清空列表

    def get_current_file(self,open_path,open_file):
        '从文件夹众多txt文件中中筛选出与当前日期相符合的文件'
        GetInputTxt.get_txt_file(self,open_path)
        for each_path in GetInputTxt.txt_file_path:
            path_name = str.lower(each_path)
            if path_name.find(open_file) > 0:
                GetInputTxt.txt_file_path.clear()  # 清空列表
                return each_path

    def txt_input(self):
        '手动输入文件路径名和文件名'
        current_path = '/home/pi/Desktop/python'
        current_file = '节点1-20200915.txt'
        # current_path = input('请输入log文件存放路径：\n')  # 定义测试log文件存放路径
        # current_file = input('请输入log文件名：\n')  # 定义要处理的log文件名
        txt_type = GetInputTxt.get_current_file(self,current_path, current_file)
        print(txt_type)
        return txt_type

class ThreadTxt:
    '线程'
    def thread_input(self):
        txt_process = TxtProcess()
        txt_file_get = GetInputTxt()
        file_name = txt_file_get.txt_input()
        thd_input = Thread(target=txt_process.module_process(file_name))
        thd_input.daemon = True
        thd_input.start()
        print('数据处理完毕！')

def datebase():
    '获取与系统时间相关联的文件名'
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    datetime = int(year) * 10000 + int(month) * 100 + int(day)
    return datetime

def ensure_dir_exist(path):
    '确保目录是否存在，不存在就新创建目录，用于保存生成文件'
    if not os.path.isdir(path):
        os.makedirs(path)

def save_txt_file(num,name,count):
    '创建txt文件，以名字加数字的方式保存'
    file_name = name + str(count) + '.txt'
    with open(file_name,"w") as f1:
        f1.writelines(num)

class TxtProcess:
    '对文件的数据处理'
    def module_judgement(self,file_name):
        '判断输入文件是网关数据还是节点数据'
        txt_name = ''
        txt_split = []  #将路径分割成列表中的独立元素
        txt_split = file_name.split('/')    #以文件分隔符分割路径名字符串
        for each in txt_split:
            if each.find('.txt') > 0:
                txt_name = each
        if txt_name.find("节点") == 0:
            print('当前处理数据为 %s log数据' % txt_name[0:3])
            return True
        elif txt_name.find("网关") == 0:
            print('当前处理数据为 网关 log数据')
            return False
        else:
            pass

    def module_process(self,file_name):
        '根据文件名选择处理网关或节点文件'
        if TxtProcess.module_judgement(self,file_name):
            TxtProcess.node_process(self,file_name)
        else:
            TxtProcess.gateway_process(self,file_name)

    def node_process(self,file_name):
        '节点数据处理函数'
        com_cnt = [0 for i in range(100)]
        line_count = 0
        with open(file_name, encoding='utf-8') as node_file:  # 打开文件并定义文件操作类型
            for each_line in node_file.readlines():
                line_count += 1
                if each_line.find('通信开始') > 0 and com_cnt[0] == 0:
                    com_cnt = 1
                    node_para.com_count.append(com_cnt)
                    coma[0].append(com_cnt)
                    print(coma)
                elif each_line.find('通信开始') > 0 and com_cnt == 1:
                    com_cnt = 2
                    node_para.com_count.append(com_cnt)


                # while com_cnt > 0:
                #     line_count += 1
                #     node_para.com_content.append(each_line)

    def node_once_recv(self,content):
        '节点单次接收处理'
        for each in content:
            if each.find('发送数据') > 0:
                node_para.recv_count.append(each[1])
                # print(node_para.recv_count)

    def node_once_send(self,content):
        '节点单次发送处理'
        return 0

    def gateway_process(self,file_name):
        '网关数据处理函数'
        send_once_content = []  #单次发送数据内容
        recv_once_content = []  #单次接收数据内容
        with open(file_name,encoding='utf-8') as gw_file:
            for each_line in gw_file.readlines():
                if each_line.find('TX') == 0:   #发送处理
                    each_line = each_line[3:]
                    send_once_content = each_line.split(None)   #以空格作为文件分割条件
                    TxtProcess.gw_once_send(self,send_once_content)
                elif each_line.find('RX') == 0: #接收处理
                    each_line = each_line[3:]
                    recv_once_content = each_line.split(None)
                    TxtProcess.gw_once_recv(self,recv_once_content)
                else:
                    pass
            TxtProcess.gateway_export(self) #网关处理数据打印

    def gw_once_recv(self,content):
        '网关单次接收处理'
        name = []   #接收名称
        value = []  #接收参数
        recv_type = []  #接收类型
        for each in content:
            (name,value) = each.split(':',1)    #以冒号为分隔符分割参数
            if name == 'id':    #接收节点ID号
                gw_para.recv_node_label.append(value)
            elif name == 'type':    #接收帧类型
                (recv_type,value) = value.split('_',1)  #以下划线为分隔符分割帧类型参数
                gw_para.recv_type.append(recv_type)
            elif name == 'freq_hz': #接收频点
                gw_para.recv_freq.append(value)
            elif name == 'if_chain':    #接收通道号
                gw_para.recv_channel.append(value)
            elif name == 'size':    #接收数据长度
                gw_para.recv_len.append(value)
            elif name == 'datarate':    #接收空中速率
                gw_para.recv_datarate.append(value)
            elif name == 'cnt': #接收帧计数
                gw_para.recv_count.append(value)
            elif name == 'sn':  #接收帧序号
                gw_para.recv_frame_num.append(value)
            elif name == 'rssi':    #接收信号强度
                gw_para.recv_rssi.append(value)
            elif name == 'snr': #接收信噪比
                gw_para.recv_snr.append(value)
            else:
                pass

    def gw_once_send(self,content):
        '网关单次发送处理'
        name = []   #发送名称
        value = []  #发送参数
        send_type = []  #发送帧类型
        for each in content:
            (name, value) = each.split(':', 1)
            if name == 'freq_hz':   #发送频点
                gw_para.send_freq.append(value)
            elif name == 'rf_power':    #发送功率
                gw_para.send_power.append(value)
            elif name == 'size':    #发送数据长度
                gw_para.send_len.append(value)
            elif name == 'datarate':    #发送空中速率
                gw_para.send_datarate.append(value)
            elif name == 'cnt': #发送帧计数
                gw_para.send_count.append(value)
            elif name == 'type':    #发送帧类型
                (send_type,value) = value.split('_',1)
                gw_para.send_type.append(send_type)
            else:
                pass

    def gateway_export(self):
        print('************send*************')
        print('count:%s' % gw_para.send_count)
        print('type:%s' % gw_para.send_type)
        print('freq:%s' % gw_para.send_freq)
        print('power:%s' % gw_para.send_power)
        print('len:%s' % gw_para.send_len)
        print('datarate:%s' % gw_para.send_datarate)
        print('*****************************')

        print('***********receive************')
        print('count:%s' % gw_para.recv_count)
        print('id:%s' % gw_para.recv_node_label)
        print('type:%s' % gw_para.recv_type)
        print('freq:%s' % gw_para.recv_freq)
        print('datarate:%s' % gw_para.recv_datarate)
        print('channel:%s' % gw_para.recv_channel)
        print('frame_num:%s' % gw_para.recv_frame_num)
        print('len:%s' % gw_para.recv_len)
        print('rssi:%s' % gw_para.recv_rssi)
        print('snr:%s' % gw_para.recv_snr)
        print('*****************************')

def test_process(file_name):
    '对字符型文件按需求进行分割，将所有序列按奇偶进行排序并去除掉首字母序号，将剩下的字符创建新的文件并保存'
    odd_file = []  # 定义奇数列表
    even_file = []  # 定义偶数列表
    num_char = []  # 定义数字的字符型列表
    word_char = []  # 定义余下的字符列表
    date = []  # 定义当前系统日期
    count_odd = 0  # 定义计数值,用于按顺序生成分割的文件名
    count_even = 0  # 定义计数值,用于按顺序生成分割的文件名
    with open(file_name, encoding='utf-8') as file_init:  # 打开文件并定义文件操作类型

        # 以文件中的第一个空格作为分割标识，将文件每一行分割成两部分；
        # 分别将每部分使用append函数保存到数字列表和文字列表中。
        # 判断数字列表中的每一个数字，若数字为偶数则将文字列表中文字保存到偶数列表；
        # 奇数同理
        for each_line in file_init:
            (number, sp_word) = each_line.split(None, 1)  # 以第一个空格为标识分割为2
            num_char.append(number)
            word_char.append(sp_word)
        for each in num_char:
            i = int(each)
            if i % 2:
                odd_file.append(word_char[i - 1])
                count_odd += 1
            else:
                even_file.append(word_char[i - 1])
                count_even += 1

        datetime = datebase()
        save_txt_file(odd_file, 'odd_', datetime)
        save_txt_file(even_file, 'even_', datetime)

if __name__ == '__main__':
    threadtxt = ThreadTxt()
    threadtxt.thread_input()




