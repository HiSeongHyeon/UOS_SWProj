# 판단할 자세별 클래스
class angle_waist:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt 
        self.data = data 
        self.output = output 
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2

class monitor_near:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2

class monitor_far:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  

class turttle_neck:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  

class hands:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  
