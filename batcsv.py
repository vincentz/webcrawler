# -*- coding: utf-8 -*-
__author__ = 'zhuqiuhan'
import csv
import datetime
import sys
import os
import string
reload(sys)
#中文错误
sys.setdefaultencoding( "utf-8" )

class BatchProcessCSV:
    def __init__(self,inputfolder,outputfolder):
        self.inputfolder=inputfolder
        self.outputfolder=outputfolder
    #批处理
    def doBatchAction(self):
        startTime=datetime.datetime.now()
        print(u"开始处理...")
        if (os.path.exists(self.outputfolder)==False):
            #pass
            os.makedirs(self.outputfolder)
        list_dirs = os.walk(self.inputfolder)
        for root, dirs, files  in list_dirs:
            # del files[0]
            # print files[1]
            for file in files:
                otput=self.outputfolder+file
                self.readcsv2csv(self.inputfolder+file,otput)
                # print(u"Running.........................\n")
 
        endTime=datetime.datetime.now()
        print(u"处理完成，耗时：%f秒"%(endTime-startTime).seconds)
 
    #读取一个csv提取部分信息生成新的CSV
    def readcsv2csv(self,inputfile,outputfile):
      with open(inputfile, 'rb') as csvfile:
        o=open(outputfile,"wb")
  #解决csv浏览乱码问题
        o.write('\xEF\xBB\xBF');
        writer=csv.writer(o)
        #读取列 将字符串转为数组
        column=csvfile.readline().split(",")
        #print(column.index('App Release Date'))
        new_item = inputfile.split("/")[-1].replace('.csv','')
        writer.writerow(['小区','成交日期','成交价','单价','户型','面积','楼层','朝向'])
        reader = csv.reader(csvfile)
        #table = reader[0]
        for row in reader:
            row.insert(0,new_item)
            writer.writerow(row)
        print new_item
 
#process
if __name__=="__main__":
    #此处为输入输出文件夹相对路径 可供修改
    csvProcess=BatchProcessCSV("./house_price/","./house_price_new/")
    csvProcess.doBatchAction()