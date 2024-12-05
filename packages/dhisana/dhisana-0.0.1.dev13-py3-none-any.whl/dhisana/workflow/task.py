from functools import wraps

class Task:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.next_task = None

    def set_next(self, task):
        self.next_task = task

    def run(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if self.next_task:
            return self.next_task.run(result)
        return result

def task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_instance = Task(func)
        return task_instance.run(*args, **kwargs)
    return wrapper

def flow(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Starting flow: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Flow {func.__name__} completed.")
        return result
    return wrapper

@task
def extract_data():
    data = {"key": "value"}
    print(f"Extracted data: {data}")
    return data

@task
def transform_data(data):
    transformed = {k: v.upper() for k, v in data.items()}
    print(f"Transformed data: {transformed}")
    return transformed

@task
def load_data(data):
    print(f"Loading data: {data}")
    # Implement loading logic here


@flow
def etl_workflow():
    data = extract_data()
    transformed = transform_data(data)
    load_data(transformed)


if __name__ == "__main__":
    etl_workflow()
