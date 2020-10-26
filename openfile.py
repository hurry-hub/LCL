#coding=utf-8
import csv
import jieba
#import uniout
with open('外卖评论.csv', 'r') as f:
    reader = csv.reader(f)
    result = list(reader)
    print(result[5])
    seg_list = jieba.cut(result[5][1])
    print(",".join(seg_list))
