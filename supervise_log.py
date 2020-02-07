import pickle as pkl
from princess import hist
import torch
import numpy as np

class log:
    def __init__(self,counter):
        self.counter = counter
        self.eyes = 0
        self.log = 'temp_data.pkl'
        self.data = [0]*counter
    def log_weight(self, weight):
        if self.eyes >= self.counter:
            self.eyes = 0
        self.data[self.eyes] = hist(weight)
        #print(type([self.data[0][0]]))
        self.eyes += 1

    def log_scalar(self,scalar):
        if self.eyes >= self.counter:
            self.eyes = 0
        self.data[self.eyes] = scalar
        self.eyes += 1
    def log_pie(self,labels,values):
        if self.eyes >= self.counter:
            self.eyes = 0
        self.data[self.eyes] = [labels,values]
        self.eyes += 1
    def log_scalars(self,scalars):
        if self.eyes >= self.counter:
            self.eyes = 0
        self.data[self.eyes] = scalars
        self.eyes += 1
    def log_weights(self,weights):
        if self.eyes >= self.counter:
            self.eyes = 0
        self.data[self.eyes] = [hist(weight) for weight in weights]
        self.eyes += 1

    def log_end(self):
        with open(self.log, 'wb') as f:
            pkl.dump(self.data, f)

