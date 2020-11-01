#coding=utf-8
#File: openfile.py

import math,time
import csv
import jieba.posseg as pseg
import jieba


class SoPmi:
    def _init_(self):
        self.train_path = './外卖评论.csv'
        self.sentiment_path = './sentiment_words.txt'

    '''分词'''
    def seg_corpus(self, train_data, sentiment_path):
        sentiment_words = [line.strip().split('\t')[0] for line in open(sentiment_path)]
        for word in sentiment_words:
            jieba.add_word(word)
        seg_data = list()
        count = 0
        for line in open(train_path, 'r'):
            line = line.strip()
            count += 1
            if line:
                seg_data.append([word.word for word in pseg.cut(line) if
                    word.flag[0] not in ['u', 'w', 'x', 'p', 'q', 'm']])
            else:
                continue
        return seg_data

    '''统计搭配次数'''
    def collect_cowords(self, sentiment_path, seg_data):
        def check_words(sent):
            if set(sentiment_words).intersection(set(sent)):
                return True
            else:
                return False
        cowords_list = list()
        window_size = 5
        count = 0
        sentiment_words = [line.strip().split('\t')[0] for line in open(sentiment_path)]
        for sent in seg_data:
            count += 1
            if check_words(sent):
                for index, word in enumerate(sent):
                    if index < window_size:
                        left = sent[:index]
                    else:
                        left = sent[index - window_size: index]
                    if index + window_size > len(sent):
                        right = sent[index + 1:]
                    else:
                        right = sent[index: index + window_size + 1]
                    context = left + right [word]
                    if check_words(context):
                        for index_pre in range(0, len(context)):
                            if check_words([context[index_pre]]):
                                for index_post in range (index_pre + 1, len(context)):
                                    cowords_list.append(context[index_pre] + '@' + context[index_post])
        return cowords_list

    def collect_candiwords(self, seg_data, cowords_list, sentiment_path):
        def compute_mi(p1, p2, p12):
            return math.log2(p12) - math.log2(p1) - math.log2(p2)
        '''统计词频'''
        def collect_worddict(seg_data):
            word_dict = dict()
            all = 0
            for line in seg_data:
                for word in line:
                    if word not in word_dict:
                        word_dict[word] = 1
                    else:
                        word_dict[word] += 1
            all = sum(word_dict.values())
            return word_dict, all
        '''统计此共现次数'''
        def collect_cowordsdict(cowords_list):
            co_list = dict()
            candi_words = list()
            for co_words in cowords_list:
                candi_words.extend(cowords.split('@'))
                if co_words not in co_dict:
                    co_dict[co_words] = 1
                else:
                    co_dict[co_words] += 1
            return co_dict, candi_words
        '''收集种子情感词'''
        def collect_sentiwords(sentiment_path, word_dict):
            pos_words = set([line.strip().split('\t')[0] for line in
                open(sentiment_path) if line.strip().split('\t')[1] ==
                'pos']).intersection(set(word_dict.keys()))
            neg_words = set([line.strip().split('\t')[0] for line in
                open(sentiment_path) if line.strip().split('\t')[1] ==
                'neg']).intersection(set(word_dict.key()))
            return pos_words, neg_words
        '''计算sopmi值'''

