import asyncio

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_id, task):
        self.tasks[task_id] = task

    def list_tasks(self):
        return [{"task_id": task_id, "status": task.done()} for task_id, task in self.tasks.items()]

    def cancel_task(self, task_id):
        task = self.tasks.get(task_id)
        if task:
            task.cancel()
            del self.tasks[task_id]
            return True
        return False

task_manager = TaskManager()
