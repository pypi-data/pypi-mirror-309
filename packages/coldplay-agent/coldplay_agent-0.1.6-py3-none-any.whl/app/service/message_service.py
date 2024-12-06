# app/service/message_service.py

import json
from app.service.task_service import TaskService 

class MessageService:
    @staticmethod
    def process_message(body):
        """
        处理消息的核心逻辑
        """
        try:
            message = json.loads(body)
            print(f"Processing message: {message}")
            print(f"Processing message: {message['type']}")
            # 在这里添加实际的业务逻辑处理，比如保存到数据库
            match message['type']: 
                case 'task_run':
                    TaskService.task_run(message['data'])
                    print(f"{message['type']}OK") 
                case 'task_stop':
                    TaskService.task_stop(message['data'])
                    print(f"{message['type']}OK") 
                case 'task_pause':
                    TaskService.task_pause(message['data'])
                    print(f"{message['type']}OK") 
                case 'task_restart':
                    TaskService.task_restart(message['data'])
                    print(f"{message['type']}OK") 
        except json.JSONDecodeError as e:
            print(f"Error decoding message: {e}")
            return False
        return True