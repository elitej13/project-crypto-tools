
import threading
import math
import sympy as sy
from time import perf_counter

exitFlag = 0

class RSA_Cracking_Thread(threading.Thread):
   def __init__(self, threadID, threadCount, name, n):
      threading.Thread.__init__(self)
      global exitFlag
      exitFlat = 0
      self.threadID = threadID
      self.threadCount = threadCount
      self.name = name
      self.n= n
   def run(self):
       global exitFlag
       start = int(math.ceil(self.n**(0.5) * (self.threadID / self.threadCount)))
       stop = int(math.floor(self.n**(0.5) * ((self.threadID - 1) / self.threadCount)))
       candidate_root = start
       if(stop == 0):
           stop = 3
       while(self.n % candidate_root != 0 and candidate_root > stop and exitFlag == 0):
           candidate_root = sy.prevprime(candidate_root)
       if(self.n % candidate_root == 0):
           exitFlag = 1
           self.found = candidate_root

class RSA_Cracking_Thread_Timed (threading.Thread):
   def __init__(self, threadID, threadCount, name, n, max_time):
      threading.Thread.__init__(self)
      global exitFlag
      exitFlat = 0
      self.threadID = threadID
      self.threadCount = threadCount
      self.name = name
      self.n = n
      self.max_time = max_time
   def run(self):
      global exitFlag
      self.found = 0
      start_time = perf_counter()
      start = int(math.ceil(self.n**(0.5) * (self.threadID / self.threadCount)))
      stop = int(math.floor(self.n**(0.5) * ((self.threadID - 1) / self.threadCount)))
      candidate_root = start
      if(stop == 0):
          stop = 3
      while(self.n % candidate_root != 0 and candidate_root > stop and exitFlag == 0):
          if((perf_counter() - start_time) > self.max_time):
              self.found = -1
              break
          candidate_root = sy.prevprime(candidate_root)
      if(self.n % candidate_root == 0):
          exitFlag = 1
          self.found = candidate_root
