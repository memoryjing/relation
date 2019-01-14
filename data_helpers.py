# -*- coding: utf-8 -*-
import numpy as np
import re
import itertools
from collections import Counter
from src.data_helper import Constants,helpFunction


CLASS_NUMS=11

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

# create y_one_hot according to class number
def create_one_hot(num):
    one_hot=[0]*CLASS_NUMS
    one_hot[num]=1
    return one_hot

# CPR:3	 bbbbb1 Tomudex eeeee1  treatment resulted in the decrease in p27(kip1) expression, with an increase in cyclin E and cdk2 protein expression and  bbbbb2 kinase eeeee2  activities 24 h after a 2-h exposure#
#generate x_text and y_one_hot from list text
def split_x_text_and_create_y_one_hot(original_x):
    x_text=[]
    x_pos1=[]
    x_pos2=[]
    y_one_hots=[]
    for x in original_x:
        y_chars=re.search('\d+',x)
        y_one_hot=create_one_hot(int(y_chars.group().strip())-1)
        y_one_hots.append(y_one_hot)
        #generate x information
        x_str=x.split('\t')[-1]
        text,pos1,pos2=helpFunction.create_xtext_and_pos(x_str)
        x_text.append(text)
        x_pos1.append(pos1)
        x_pos2.append(pos2)
    return x_text,x_pos1,x_pos2,y_one_hots

#由文件获取句子词信息，分别相对于entity1 和 entity2 的位置信息，以及labels向量
def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(positive_data_file, "r",encoding='UTF-8').readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r",encoding='UTF-8').readlines())
    negative_examples = [s.strip() for s in negative_examples]

    #读进来的原始数据
    # x_text_temp = [clean_str(sent) for sent in positive_examples]+\
    #                 [clean_str(sent) for sent in negative_examples]
    if positive_data_file==negative_data_file:
        x_text_temp=positive_examples
    else:
        x_text_temp=positive_examples+negative_examples
    #generate training sample (x and y)
    x_text,x_pos1,x_pos2,y_one_hots=split_x_text_and_create_y_one_hot(x_text_temp)
    return [x_text,x_pos1,x_pos2,y_one_hots]

def createJsonData(positive_data_file):
    # Load data from files
    positive_examples = list(open(positive_data_file, "r", encoding='UTF-8').readlines())
    x_text, x_pos1, x_pos2, y_one_hots = split_x_text_and_create_y_one_hot(positive_examples)




def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]

if __name__=="__main__":
    positive_data_file="data/ChEMPROT/chemprot_training/train.embed"
    negative_data_file="data/ChEMPROT/chemprot_training/negativeIn.embed"
    x_text,_,_,y_one_hots=load_data_and_labels(positive_data_file, negative_data_file)

    i=1
    for item_x,item_y in zip(x_text,y_one_hots):
        i=i+1
        print(item_x)
        print(item_y)
        if i>50:
            break

#     original_x=['CPR:10	 bbbbb1 Tomudex eeeee1  treatment resulted in the decrease in p27(kip1) expression, with an increase in cyclin E and cdk2 protein expression and  bbbbb2 kinase eeeee2  activities 24 h after a 2-h exposure',
# 'CPR:3	These results suggest that the megabase DNA fragmentation is induced as a consequence of inhibition of thymidylate synthase by  bbbbb1 Tomudex eeeee1  and kilobase DNA fragmentation may correlate with the reduction of p27(kip1) expression and the increase in  bbbbb2 cyclin E eeeee2  and cdk2 kinase activities']
#     split_x_text_and_create_y_one_hot(original_x)