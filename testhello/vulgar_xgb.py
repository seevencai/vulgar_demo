# coding=utf-8
# RedundanceReduction(Red2) is used for removing those redundant texts.
import gensim
import re
import math
import random
import numpy as np
from collections import defaultdict
import sys
import os
import pickle
from sklearn.neighbors import KDTree
import time
import jieba
import xgboost as xgb
# # read in data
# time0 = time.time()
# print 'reading data'
# dtrain = xgb.DMatrix('xgboost_training')
dtest = xgb.DMatrix('data/weibo_xgboost_training')
# print 'finish loading'
# print time.time() - time0
# # specify parameters via map
# param = {'max_depth':6, 'eta':0.3, 'silent':0, 'objective':'binary:logistic' }
# num_round = 50
label0_1 = 0
label0_0 = 0
label1_0 = 0
label1_1 = 0
# time0 = time.time()
# print 'creating model'
bst = xgb.Booster({'nthread':4}) #init model
bst.load_model("model/vulgar_xgboost")
# bst = xgb.train(param, dtrain, num_round)
# print 'finish modeling'
# print time.time() - time0
# # make prediction
# time0 = time.time()
# print 'make prediction'
preds = bst.predict(dtest)
# print 'finish predicting'
# print time.time() - time0
test_labels = dtest.get_label()
pkl_file1 = open('model/vulgar_balltree', 'rb')
test_data_set = pickle.load(pkl_file1)
test_vectors = test_data_set['vectors']
test_sentences = test_data_set['sentences']
result = []
for i in range(len(test_labels)):
    flag = False
    if preds[i] > 0.5:
        if test_labels[i] == 0:
            label0_1 = label0_1 + 1
            flag = True
        else:
            label1_1 = label1_1 + 1
            flag = True
    else:
        if test_labels[i] == 0:
            label0_0 = label0_0 + 1
        else:
            label1_0 = label1_0 + 1
            flag = True
    if flag:
        result.append(test_sentences[i] + ',' + str(test_labels[i]) + ',' + str(preds[i]) + '\n')
print 'precission:'
print 'label0_0: ' + str(label0_0)
print 'label0_1: ' + str(label0_1)
print 'label1_0: ' + str(label1_0)
print 'label1_1: ' + str(label1_1)
f = open('weibo_training_vulgar','w')
f.write(''.join(result))
f.close()
pkl_file1.close()
# fn = 'vulgar_xgboost'
# bst.save_model('vulgar_xgboost')
# with open(fn, 'w') as f:                 # open file with write-mode
#     picklestring = pickle.dump(bst, f)
# pkl_file.close()
# test_vectors = test_data_set['vectors']
# test_sentences = test_data_set['sentences']
# test_labels = test_data_set['labels']
# vulgarWords = {}
# result = []
# for line in open('vulgarWords'):
#     word = line.strip()
#     if word not in vulgarWords:
#         vulgarWords[word] = True
#         result.append(word + '\n')

