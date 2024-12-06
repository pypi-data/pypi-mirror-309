import requests

from app.service.util_service import UtilService
 
class CurlService:
    def get_token():
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        apiserver_user = coldplay_config['DEFAULT'].get('apiserver_user')  # 从配置文件中获取API用户名
        apiserver_pwd = coldplay_config['DEFAULT'].get('apiserver_pwd')  # 从配置文件中获取API密码
        # 登陆API URL
        url = f"{apiserver_host}/api/login"
        # 设置请求头
        headers = {
            "Content-Type": "application/json"  # 可选：如果你发送JSON数据
        }

        # 要发送的数据
        payload = {
            "username": apiserver_user,
            "password": apiserver_pwd
        }
        try:
            # 发送POST请求
            response = requests.post(url, headers=headers, json=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()  # 解析JSON响应
                if data['code'] == 200:
                    token  = data['token']
                    return token
                else:
                    print(f"请求失败：{data['msg']}")
            else:
                print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
        except requests.exceptions.RequestException as e:
            print(f"请求出现错误：{e}")
        return None
    
    def update_task_status(task_id: str, task_status: str):
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        # 修改状态API接口
        url = f"{apiserver_host}/api/task/update/status"
        token = CurlService.get_token()
        if token == None:
            print(f"获取token失败")
        else:
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  # 可选：如果你发送JSON数据
            }
            # 要发送的数据
            payload = {
                "taskId": task_id,
                "taskStatus": task_status
            }
            try:
                # 发送POST请求
                response = requests.post(url, headers=headers, json=payload)
                # 检查请求是否成功
                if response.status_code == 200:
                    data = response.json()  # 解析JSON响应
                    return data
                else:
                    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
            except requests.exceptions.RequestException as e:
                print(f"请求出现错误：{e}")
        return None
    
    def add_user_queue(queue_name: str):
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        # 修改状态API接口
        url = f"{apiserver_host}/api/task/queue/create"
        token = CurlService.get_token()
        if token == None:
            print(f"获取token失败")
        else:
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  # 可选：如果你发送JSON数据
            }
            # 要发送的数据
            payload = {
                "queueName": queue_name
            }
            try:
                # 发送POST请求
                response = requests.post(url, headers=headers, json=payload)
                # 检查请求是否成功
                if response.status_code == 200:
                    data = response.json()  # 解析JSON响应
                    return data
                else:
                    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
            except requests.exceptions.RequestException as e:
                print(f"请求出现错误：{e}")
        return None
    