# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8') 
from django.http import HttpResponse
from django.shortcuts import render_to_response
import gensim
import re
import math
import random
import numpy as np
from collections import defaultdict
import sys
import os
import pickle
import time
import jieba
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
import json
import lightgbm as lgb
import pandas as pd

def normalize(v):
    n = 0.0
    for i in range(len(v)):
        n = n + v[i] * v[i]
    if n == 0.0:
        return v
    return v / math.sqrt(n)
 
# 表单
def search_form(request):
    return render_to_response('search_form.html')

def get_vulgar_score(s):
    line = s.decode('utf8')
    sentence = ''
    w2vModel = gensim.models.Word2Vec.load('testhello/word_embedding_model')
    vocab = w2vModel.wv.vocab
    for uchar in line:
        if uchar == '，' or uchar == '。' or uchar == '！' or uchar == '？':
            sentence = sentence + uchar
        elif uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            sentence = sentence + uchar
        elif uchar >= 'a' and uchar <= 'z' or (uchar >= 'A' and uchar <= 'Z'):
            sentence = sentence + uchar    
    words = jieba.lcut(sentence)
    vector = []
    for word in words:
        word = word.encode('utf8')
        if word not in vocab or vocab[word].count > 2000:
            continue
        if len(vector) == 0:
            vector = normalize(w2vModel[word]) / math.log(vocab[word].count + 0.001)  
        else :
            vector = vector + normalize(w2vModel[word]) / math.log(vocab[word].count + 0.001)
    if len(vector) == 0:
        return '您输入的文本无法解析'
        print('Load model to predict')
    # bst = lgb.Booster(model_file='model.txt')
    with open('testhello/model.pkl', 'rb') as fin:
        bst = pickle.load(fin)
    # bst = xgb.Booster(params = {'nthread':1}) #init model
    # bst.load_model("testhello/vulgar_xgboost")
    # testv = xgb.DMatrix([vector])
    preds = bst.predict([vector])
    score = preds[0]
    # del testv
    # del vector
    # del bst
    return score
# 接收请求数据
def search(request):
    request.encoding='utf8' 
    if 'q' in request.GET:
        score = get_vulgar_score(request.GET['q']) 
        message = '你搜索的内容低俗概率为: ' + str(score)
    else:
        message = '你提交了空表单'
    return HttpResponse(message)