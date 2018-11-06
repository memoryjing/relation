# -*- coding: utf-8 -*-
import os
from data_helper.Constants import *
import types
import data_helper.helpFunction
from data_helper.helpFunction import get_plain_sentence,create_negative_case,\
create_sentence_map,create_negative_cases
import pprint
from data_helper import FileUtil
import sys





def read_CPR_corpus(abs_file, entity_file, rel_file=None):
    
    '''
        read abstracts as a map from pmid to the abstract content
    '''   
    abs_map = {}
    for line in open(abs_file,encoding="utf-8"):
        #line = line.encode("utf-8")
        pid, _, text =line.strip().partition('\t')
        if pid in abs_map.keys():
            print ('Nao Gui Le!')
            os._exit(0)
        else:
            abs_map[pid] = text.replace('\t', ' ')
    
    '''
        read entity file as a nested map from pmid to Eid to entity content 
    '''
    entity_map = {}
    count_entity=0
    for line in open(entity_file,encoding="utf-8"):
        count_entity=count_entity+1
        splited = line.strip().split('\t')
        if splited[0] in entity_map.keys():
            if splited[1] in entity_map[splited[0]].keys():
                print ('Jian Gui Le!')
                os._exit(0)
            else:
                entity_map[splited[0]][splited[1]] = splited[2:]
        else:
            entity_map[splited[0]] = {splited[1]:splited[2:]}
    
    relation_map={}
    for line in open(rel_file):
        rel_splited = line.strip().split('\t')
        pid = rel_splited[0]
        if pid in entity_map.keys():
            e1_id = rel_splited[4].partition(':')[2]
            e2_id = rel_splited[5].partition(':')[2]
            if pid in relation_map.keys():
                relation_map[pid].append([e1_id,e2_id])
            else:
                relation_map[pid]=[[e1_id,e2_id]]
        else:
            print("relation map:Jian Gui Le")
            pass
    
    
    negativeIn_instances=[]
    negativeNotIn_instances=[]
    sentence_map={}
    for pid,abs in abs_map.items():
        if pid not in relation_map.keys():
            #处理不在relation中的abs
            sentence_map=create_sentence_map(abs)
            for sentence in sentence_map.items():
                negativeNotIn_instance=create_negative_cases(sentence,entity_map[pid])
                negativeNotIn_instances.extend(negativeNotIn_instance)
            continue
        
        #分割句子
        #将abstract分成单独的句子，并且每个句子有起始和结束的位置{"sentence":[start,end],....}
        sentence_map=create_sentence_map(abs)
        for sentence in sentence_map.items():
            negative_instance=create_negative_cases(sentence,entity_map[pid],relation_map[pid])
            negativeIn_instances.extend(negative_instance)
    return negativeIn_instances,negativeNotIn_instances 
     


if __name__ == '__main__':
    dir ='C:/Users/Administrator/Desktop/ChEMPROT/'
    
    #选择处理的是训练集还是测试集的数据
    choice=sys.stdin.readline().strip()
    if choice=="test":
        entity_file = dir + 'chemprot_test_gs/chemprot_test_entities_gs.tsv'
        abs_file = dir + 'chemprot_test_gs/chemprot_test_abstracts_gs.tsv'
        rel_file = dir + 'chemprot_test_gs/chemprot_test_relations_gs.tsv'
        
    else:
        entity_file = dir + 'chemprot_training/chemprot_training_entities.tsv'
        abs_file = dir + 'chemprot_training/chemprot_training_abstracts.tsv'
        rel_file = dir + 'chemprot_training/chemprot_training_relations.tsv'
    instancesIn,instancesNotIn = read_CPR_corpus(abs_file, entity_file, rel_file)
    i=0
    while(i<10): 
        print(instancesIn[i])  
        i=i+1
    print("==================================")
    i=0
    while(i<10): 
        print(instancesNotIn[i])  
        i=i+1
    print("==================================")
    if choice=="test":
        FileUtil.writeStrLines(dir + 'chemprot_test_gs/negativeIn.embed', instancesIn)           
        FileUtil.writeStrLines(dir + 'chemprot_test_gs/negativeNotIn.embed', instancesNotIn)           
        
    else:
        FileUtil.writeStrLines(dir + 'chemprot_training/negativeIn.embed', instancesIn)           
        FileUtil.writeStrLines(dir + 'chemprot_training/negativeNotIn.embed', instancesNotIn)           
    

# pprint.pprint(sentence_map)      

        