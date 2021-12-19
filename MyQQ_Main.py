'''
    Name:       LD_LuoTianYiQQ
    Function:   基于MyQQ + Vocaltts 的同人ai天依
    Author:     忆古陌烟(3194775246)
    Support:    0疯_子0(1209711408)
    PS:         该文件并非clone后就可以使用，请自行获取 Vocaltts api 与 天行机器人key， 填写管理员账号
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
# import LD_QQ_Method
import MyQQ_Method
from urllib import parse


url = 'http://127.0.0.1'
callPort = 9999
port = '10002'
apiUrl = 'http://localhost:10002/MyQQHTTPAPI?'

# Vocaltts api 
TTSUrl = ''

# TianXing机器人key
TianXingKey = ''

# 机器人QQ账号
RobotQQ = ''

# myQQ目录
myQQUrl = ''

# 消息回应
class DaenQQ(BaseHTTPRequestHandler):
    def do_POST(self):
        # 回调消息获取
        raw_rev_data = self.rfile.read(int(self.headers['content-length'])).decode()
        '''
            转换为字典类型后读取回调消息(以下为官方API接口返回json详解)
            MQ_robot	用于判定哪个QQ接收到该消息
            MQ_type	接收到消息类型，该类型可在[常量列表]中查询具体定义
            MQ_type_sub	此参数在不同情况下，有不同的定义
            MQ_fromID	此消息的来源，如：群号、讨论组ID、临时会话QQ、好友QQ等
            MQ_fromQQ	主动发送这条消息的QQ，踢人时为踢人管理员QQ
            MQ_passiveQQ	被动触发的QQ，如某人被踢出群，则此参数为被踢出人QQ
            MQ_msg	（此参数将被URL UTF8编码，您收到后需要解码处理）此参数有多重含义，常见为：对方发送的消息内容，但当消息类型为 某人申请入群，则为入群申请理由,当消息类型为收到财付通转账、收到群聊红包、收到私聊红包时为原始json，详情见[特殊消息]章节
            MQ_msgSeq	撤回别人或者机器人自己发的消息时需要用到
            MQ_msgID	撤回别人或者机器人自己发的消息时需要用到
            MQ_msgData	UDP收到的原始信息，特殊情况下会返回JSON结构（入群事件时，这里为该事件data）
            MQ_timestamp	对方发送该消息的时间戳，引用回复消息时需要用到
        '''
        raw_rev_data_temp = json.loads(raw_rev_data)
        recType = raw_rev_data_temp['MQ_type']
        recID = raw_rev_data_temp['MQ_fromID']
        recMsg = parse.unquote(raw_rev_data_temp['MQ_msg'])
        # print(raw_rev_data_temp)
        if not (recType == 2 and not MyQQ_Method.judgeAt(recMsg)):
            threadName = str(random.randint(100, 10000))
            thread = MyQQ_Method.myThread(threadName, raw_rev_data)
            thread.start()
        elif recType == 2 and MyQQ_Method.Crux_judgeExist(recMsg):
            thread = MyQQ_Method.cruxThread(RobotQQ, recID, recMsg)
            thread.start()

# 程序执行入口
if __name__ == '__main__':
    setting = open('setting.txt', 'r+')
    settings = setting.readlines()
    RobotQQ = settings[0].strip()
    myQQUrl = settings[1].strip()
    print('RobotQQ：' + RobotQQ)
    print('myQQUrl：' + myQQUrl)
    timeThread = MyQQ_Method.timeThread(RobotQQ, True)
    timeThread.start()
    MyQQ_Method.myRobot(apiUrl, TTSUrl, TianXingKey, myQQUrl, RobotQQ)
    # 第一参数为回调地址，第二参数为回调接口
    host = ('localhost', callPort)
    # 调用HTTP服务器
    server = HTTPServer(host, DaenQQ)
    # 服务启动控制台提醒
    print('Starting server, listen at: %s:%s' % host)
    # 服务启动挂载(保持服务一直在线)
    server.serve_forever()