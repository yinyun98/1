import asyncio
import os
import random
import string
import time
import re

from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon import events
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import JoinChannelRequest
import json
from telethon import functions, types
from telethon.sync import TelegramClient

api_id = 10614217
api_hash = '10f5a0dba4661f050934f9676046f01c'


# json 文件写入
def js_file_write(path, content):
    """
    json 文件写入
    :param path: json 文件路径
    :param content: 写入内容
    :return:
    """
    with open(path, "w+", encoding="UTF-8") as f:
        json.dump(content, f)


# json 文件读取
def js_file_read(path):
    """
    json 文件读取
    :param path: json 文件路径
    :return: 读取内容
    """
    try:
        with open(path, "r", encoding="UTF-8") as f:
            document = json.load(f)
        return document
    except FileNotFoundError:
        print("没有这个json文件")


# 登陆文件夹内正常的账号
def Login_account(path):
    """
    登陆文件夹内正常的账号
    :param path: 文件夹路径
    :return:    客户端的列表,字典
                "客户端": client,
                "账号名": me.first_name,
                "账号id": me.id,
                "状态": "可用",
                "路径": path
    """

    # 文件夹包含的协议号名
    def file_name(path2):
        """
        文件夹包含的协议号名
        :param path2: 文件夹路径
        :return: 列表形式的文件名
        """
        # 筛选文件夹里是否包含session
        file_result = []
        for dir_qq in os.listdir(path2):
            if dir_qq.endswith(".session"):
                file_result.append(path2 + "\\" + str(dir_qq.strip()[0:-8]))
        return file_result

    session_list = file_name(path)
    client_list = list()
    for session in session_list:
        try:
            client_8 = TelegramClient(session, api_id, api_hash).start()
            me = client_8.get_me()
            dadt = {
                "名称": me.first_name,
                "id": me.id,
                "状态": "可用",
                "客户端": client_8,
                "路径": session,
                "账号分配账号": "未分配",
                "最后发消时间": None,
                "绑定转发号ID": None
            }
            if dadt["id"] == 5838252967:
                dadt["绑定转发号ID"] = 5008477055
                dadt["账号分配账号"] = "已分配"
            if dadt["id"] == 5917395084:
                dadt["绑定转发号ID"] = 5737150951
                dadt["账号分配账号"] = "已分配"
            client_8(JoinChannelRequest("https://t.me/asdawqeq"))  # 加群
            # client_8(JoinChannelRequest(target_group))  # 加群
            try:
                client_8(ImportChatInviteRequest('z3RiLiTO63o5NTIx'))   # 加私有链接群聊
            except:
                pass
            client_8.send_message(entity="asdawqeq", message="123456")  # 直接把这条信息转发到群聊
            client_list.append(dadt)
            print(f"{session}----账号正常")
        except:
            # os.remove(f'{account_path}\\{session}.session')   # 是否删除账号
            # client_list.append([session, False])
            print(f"{session}----账号已死")
            pass
    return client_list


# 复制头像和姓名以及用户名
def set_data(client_1, entity_1, client_2, photo):
    """
    :param client_1: "客户端"
    :param entity_1: "实体"
    :param client_2: "监控客户端"
    :return:
    """

    # 更改名
    if entity_1.first_name:
        client_1(UpdateProfileRequest(
            first_name=entity_1.first_name
        ))
    else:
        client_1(UpdateProfileRequest(
            first_name=""
        ))
    # 更改姓
    if entity_1.last_name:
        client_1(UpdateProfileRequest(
            last_name=entity_1.last_name
        ))
    else:
        client_1(UpdateProfileRequest(
            last_name=""
        ))
    try:
        # 更改用户名
        sj = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, 5))
        if entity_1.username:
            client_1(UpdateUsernameRequest(f'{sj}{entity_1.username}'))
    except:
        pass
    try:
        # 获取头像
        result = client_1(functions.photos.GetUserPhotosRequest(
            user_id=client_1.get_me(),
            offset=0,
            max_id=0,
            limit=100
        ))
        # 删除头像
        for d_Photos in result.photos:
            client_1(functions.photos.DeletePhotosRequest(
                id=[types.InputPhoto(
                    id=d_Photos.id,
                    access_hash=d_Photos.access_hash,
                    file_reference=d_Photos.file_reference
                )]
            ))
        # 下载头像
        path = client_2.download_profile_photo(photo)
        # 删除头像
        # client_1(DeletePhotosRequest())
        # 更改头像
        client_1(UploadProfilePhotoRequest(
            client_1.upload_file(path)
        ))
    except:
        pass


# 查找客户端列表字典内容
def find_client(ginseng, condition):
    """
    :param ginseng: key
    :param condition: 匹配内容
    :return: 客户端字典,查找不到返回None
    """
    global clients_list
    for client_4 in clients_list:
        axs = client_4[ginseng]
        if condition == axs:
            return client_4
    return None


# 修改客户端列表字典内容
def modify_client(client_s, key, modify_value):
    """
    :param client_s:客户端字典
    :param key: 字典的key
    :param modify_value: 需要修改的值
    :return:
    """
    global clients_list
    for ss in clients_list:
        if client_s["id"] == ss["id"]:
            ss[key] = modify_value


# 处理消息
def send_message(message_1, client_1):
    global message_dictionary
    if message_1.message is not None:  # 有内容的信息
        client_1.parse_mode = 'html'
        my_string = message_1.message
        # 匹配所有浮点数
        pattern = r"\d+\.\d+"
        float_list = re.findall(pattern, my_string)
        if float_list:
            for float_str in float_list:
                float_num = float(float_str)
                if 6.5 <= float_num <= 10:
                    new_float_num = round(float_num - 0.1, 2)
                    new_float_str = str(new_float_num)
                    my_string = my_string.replace(float_str, new_float_str)
                    # 不带图片消息
                    if message_1.reply_to is not None:  # 是否回复
                        # 回复
                        try:
                            ids = message_dictionary[message_1.reply_to.reply_to_msg_id]  # 查找字典获取到对接的ID
                            var = client_1.get_messages(target_group, ids=ids)  # 回复
                            message_success = var.reply(my_string)  # 直接把这条信息转发到群聊
                            message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                            return True
                        except Exception as e:
                            print(e)
                            message_success = client_1.send_message(entity=target_group,
                                                                    message=my_string)  # 直接把这条信息转发到群聊
                            message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                            return True
                    else:
                        try:
                            # 直接把这条信息转发到群聊
                            success = client_1.send_message(entity=target_group, message=my_string)
                            message_dictionary[message_1.id] = success.id
                            return True
                        except:
                            # 直接把这条信息转发到群聊
                            pass
        else:
            print("未匹配到浮点数")
        if message_1.media is not None:  # 中转图片消息
            # 带图片的消息
            client_id = client.send_message(entity="asdawqeq",
                                            message=message_1)  # 直接把这条信息转发到群聊
            transit_message = client_1.get_messages("asdawqeq", ids=client_id.id)
            if message_1.reply_to is not None:  # 是否回复
                # 回复
                try:
                    ids = message_dictionary[message_1.reply_to.reply_to_msg_id]  # 查找字典获取到对接的ID
                    var = client_1.get_messages(target_group, ids=ids)  # 回复
                    message_success = var.reply(message_1)  # 直接把这条信息转发到群聊
                    message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                    return True
                except Exception as e:
                    print(e)
                    message_success = client_1.send_message(entity=target_group,
                                                            message=transit_message)  # 直接把这条信息转发到群聊
                    message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                    return True
            else:
                # 直接把这条信息转发到群聊
                success = client_1.send_message(entity=target_group, message=transit_message)
                message_dictionary[message_1.id] = success.id
                return True
        else:
            # 不带图片消息
            if message_1.reply_to is not None:  # 是否回复
                # 回复
                try:
                    ids = message_dictionary[message_1.reply_to.reply_to_msg_id]  # 查找字典获取到对接的ID
                    var = client_1.get_messages(target_group, ids=ids)  # 回复
                    message_success = var.reply(message_1)  # 直接把这条信息转发到群聊
                    message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                    return True
                except Exception as e:
                    print(e)
                    message_success = client_1.send_message(entity=target_group,
                                                            message=message_1)  # 直接把这条信息转发到群聊
                    message_dictionary[message_1.id] = message_success.id  # 增加字典  原id = 发送成功消息参数
                    return True
            else:
                try:
                    # 直接把这条信息转发到群聊
                    success = client_1.send_message(entity=target_group, message=message_1)
                    message_dictionary[message_1.id] = success.id
                    return True
                except:
                    # 直接把这条信息转发到群聊
                    pass


client = TelegramClient("起源", api_id, api_hash).start()
me = client.get_me()
for dialog in client.get_dialogs(limit=30):  # 列出所有对话（您打开的对话） 前10条
    print(dialog.name, dialog.id)

# 发送数据
js = js_file_read("发送数据.json")
# 账号路径
account_path = r'C:\Users\AG\Desktop\公群375转发\第一批'
# 我们的群ID
target_group = -1001764765801
# 登陆账号
clients_list = Login_account(account_path)
# 对应字典
message_dictionary = dict()
# 目标群ID
group_ID = -1001574768562
# 消息id
process_messages_id = list()
information = list()
qu_ji = 50
# # 获取群成员
# users = client.get_participants(group_ID, aggressive=True)
while True:
    try:
        group_message = client.get_messages(group_ID, qu_ji)  # 变量 = 获取群内消息，  30条
        group_message.reverse()
    except:
        pass
    for message in group_message:
        try:
            process_messages_id.index(message.id)
        except:
            process_messages_id.append(message.id)
            information.append(
                {
                    "消息": message,
                    "原消息ID": message.id,
                    "转发状态": "未转发",
                    "转发后消息": None,
                }
            )
    for event in information:
        if event['转发状态'] == '未转发':
            # 单条信息
            single_message = event['消息']
            # 用户ID
            user_id = single_message.from_id.user_id
            try:
                js.index(single_message.id)
            except:
                js.append(single_message.id)
                # 筛选什么id不发
                if user_id == 2094467068:
                    pass
                elif user_id == 5217006539:
                    pass
                else:
                    # ji_1 = True
                    # # 获取用户实体
                    # for user in users:
                    #     if user_id == user.id:
                    #         user_entity = user
                    #         ji_1 = None
                    # if ji_1:
                    #     users = client.get_participants(group_ID, aggressive=True)
                    #     for user in users:
                    #         if user_id == user.id:
                    #             user_entity = user
                    #             ji_1 = None
                    # 判断用户是否绑定
                    client_7 = find_client("绑定转发号ID", user_id)
                    if client_7:
                        # 处理消息
                        send_message(single_message, client_7["客户端"])
                    else:
                        # 用未分配账号
                        client_5 = find_client("账号分配账号", "未分配")
                        if client_5:
                            modify_client(client_5, "账号分配账号", "已分配")
                            modify_client(client_5, "绑定转发号ID", user_id)
                            # 复制头像和姓名以及用户名
                            set_data(client_5["客户端"], single_message.sender, client, user_id)
                            # 发消息
                            send_message(single_message, client_5["客户端"])
                        else:
                            print("没有账号可分配了，请及时添加账号")
                    # 添加账号
                    try:
                        with open("加账号.txt", "r") as f:
                            f = f.readlines()
                        if f[0].strip('\n') == "是":
                            clients_list += Login_account(f[1].strip('\n'))
                            fin = open('加账号.txt')
                            a = fin.readlines()
                            fin.close()
                            fout = open('加账号.txt', 'w')
                            b = ''.join(a[1:])
                            fout.write(b)
                            fout.close()
                    except:
                        pass
                    # 检测还剩多少账号
                    jis = 0
                    ji = 0
                    for abc in clients_list:
                        if abc["账号分配账号"] == "未分配":
                            jis += 1
                            print(abc["名称"], abc["账号分配账号"], abc["路径"])
                        else:
                            ji += 1
                    print("已分配账号:", ji, "个")
                    print("未分配账号还剩于:", jis, "个")
                    event['转发状态'] = "已转发"
                    js_file_write("发送数据.json", js)
                    time.sleep(3)
    try:
        # 添加账号
        with open("加账号.txt", "r") as f:
            f = f.readlines()
        if f[0].strip('\n') == "是":
            clients_list += Login_account(f[1].strip('\n'))
            fin = open('加账号.txt')
            a = fin.readlines()
            fin.close()
            fout = open('加账号.txt', 'w')
            b = ''.join(a[1:])
            fout.write(b)
            fout.close()
    except:
        pass
    for sx in clients_list:
        sj = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, 10))
        sx["客户端"].send_message(sx["id"], sj)

    time.sleep(5)
