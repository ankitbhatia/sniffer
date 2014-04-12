#!/usr/bin/python
import csv
import Queue
import os
import sys
import datetime
import time
def nonull(stream):
  for line in stream:
    yield line.replace('\x00', '')
class sniffer:
  threshold= -50
  # knownMAC = {'34:C8:03:8A:D5:64':'ankit'}
  knownMAC = {}
  track = Queue.Queue(5)
  persistant = dict([])


  def load_data(self):
    """docstring for load_data"""
    self.MAC=[]
    self.first_seen=[]
    self.pwr=[]
    self.last_seen=[]
    with open('knownMAC.txt','rb') as file:
      macs = csv.reader(file,delimiter=" ")
      for row in macs:
        self.knownMAC[row[0]]=row[1]
    with open('output-01.csv',"rb") as csvfile:
      data = csv.reader(nonull(csvfile), delimiter=',')
      count = 0
      for row in data:
        if len(row)==0:
          count+=1
          continue
        else:
          if count is 2:
            count+=1
            continue
          if count is 3:
            self.MAC.append(row[0].replace(" ",""))
            self.first_seen.append(datetime.datetime.strptime(row[1]," %Y-%m-%d %H:%M:%S"))
            self.last_seen.append(datetime.datetime.strptime(row[2]," %Y-%m-%d %H:%M:%S"))
            self.pwr.append(int(row[3].replace(" ","")))
    pers_del = []
    for mac in self.persistant:
      if mac not in self.MAC or self.pwr[self.MAC.index(mac)]<self.threshold:
        pers_del.append(mac)
    for mac in pers_del:
      del self.persistant[mac]
    for i in range(0,len(self.MAC)):
      if self.MAC[i] not in self.persistant:
        if self.pwr[i]>self.threshold:
          if not self.pwr[i]==0:
            if self.MAC[i] in self.knownMAC:
              if not self.knownMAC[self.MAC[i]]=="no":
                os.system('./tts.py Welcome back ' + self.knownMAC[self.MAC[i]])
            else:
              os.system('./tts.py Hi I have not been introduced to this person')
              os.system('./tts.py Would you like me too add this in my database')
              os.system('cls' if os.name == 'nt' else 'clear')
              print self.MAC[i]
              a = raw_input("(yes/no)\n")
              if a[0]=='y':
                self.knownMAC[self.MAC[i]] = raw_input("I haven't seen this person before,\n"+self.MAC[i] + "please intoduce me...\n")
              else:
                self.knownMAC[self.MAC[i]] = "no"
              with open('knownMAC.txt','a') as f:
                f.write(self.MAC[i] + " " + self.knownMAC[self.MAC[i]]+"\n")
            self.persistant[self.MAC[i]] = self.knownMAC[self.MAC[i]],self.pwr[i],self.first_seen[i],self.last_seen[i]


    csvfile.close()

  def extract(self):
    """docstring for extract"""
    

def main():
  sniff = sniffer()
  while True:
    time.sleep(1)
    try:
      sniff.load_data()
      os.system('cls' if os.name == 'nt' else 'clear')
      print sniff.persistant
    except KeyboardInterrupt:
      print "Exiting..."
      sys.exit(0)









if __name__ == '__main__':
  main()
