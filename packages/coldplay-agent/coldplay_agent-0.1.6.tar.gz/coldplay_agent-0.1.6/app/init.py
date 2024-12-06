import json
import shutil
import os

def initialize():
    # 获取用户输入的配置信息
    apiserver_host = input("Enter the API server host (e.g., http://172.16.10.24:9099):\n")
    apiserver_user = input("Enter the API server user (e.g., coldplay@163.com):\n")
    apiserver_pwd = input("Enter the API server password:\n")

    config_dest = os.path.expanduser('~/.coldplay_config.ini')
    # 创建配置文件内容
    config_content = f"""
    [DEFAULT]
    apiserver_host = {apiserver_host}
    apiserver_user = {apiserver_user}
    apiserver_pwd = {apiserver_pwd}
    """
    
    # 将输入的配置信息写入配置文件
    with open(config_dest, 'w') as config_file:
        config_file.write(config_content)
    
    print(f"Config file created at {config_dest}")
    print(f"Configuration saved: \n{config_content}")
