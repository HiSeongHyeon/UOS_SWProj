# 판단할 자세 별 클래스
class angle_waist:
    def __init__(self, data, queue, output): 
        self.data = data 
        self.queue = queue
        self.output = output 
    
    # 큐의 데이터에 대한 평균 계산
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output
    
    # 선입 선출을 고려한 큐 정보 저장
    def enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class turttle_neck:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output 
    
    def enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class hands:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output  
    
    def enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class brightness:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output
    
    def enqueue(self, data):
        self.queue.get()
        self.queue.put(data)
