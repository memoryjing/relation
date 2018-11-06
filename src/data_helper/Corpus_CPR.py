'''
Created on 2017.9.18

@author: 
'''
# -*- coding: utf-8 -*-
import os
from data_helper.Constants import *
import types
import sys
#from Constants import *
from data_helper import FileUtil

e_type_map = {'CHEMICAL':'chemical', 'GENE-N':'gene', 'GENE-Y':'gene'}

def analyse_two_offsets(offset1, offset2):
    if offset1[1] < offset2[0]:
        return 'normal'
    else:
        if offset1[1] == offset2[1]:
            return 'nested'
        elif offset1[1] > offset2[1]:
            return 'nested'
        else:
            return 'overlap'

#这里的begin和end指的是整个一个instance的位置，而不是仅仅在abstract中的位置
def extract_instance_from_abs(abs, e1_begin, e1_end, e2_begin, e2_end):
    print(abs[e1_begin:e1_end])
    #find sentence end .
    end = abs.find('. '.encode("utf-8"), e2_end)
    if end == -1:
        abs += '.'.encode("utf-8")
    else:
        pre = abs[:end]
        while end != -1:
            #这里原先得到的是int，需要转化为char才能判断大小写
            if pre.endswith('i.e'.encode("utf-8")) or pre.endswith('i.v'.encode("utf-8")) \
                or pre.endswith('vs'.encode("utf-8"))\
                or pre.endswith('i.p'.encode("utf-8")) or pre.endswith('i.c'.encode("utf-8")):
                print(pre)
                end = abs.find('. '.encode("utf-8"), end + 1)
            elif chr(abs[end+2]).strip()[0].isupper():
                break
            else:
                end = abs.find('. '.encode("utf-8"), end + 1)
            pre = abs[:end]
        
    begin = abs[:end].rfind('. '.encode("utf-8"))
    if begin == -1:
        begin = -2
    else:
        pre = abs[:begin]
        print(abs[begin+2:end])
        while begin != -1:
            if pre.endswith('i.e'.encode("utf-8")) or pre.endswith('i.v'.encode("utf-8")) \
                or pre.endswith('vs'.encode("utf-8"))\
                or pre.endswith('i.p'.encode("utf-8")) or pre.endswith('i.c'.encode("utf-8")):
                begin = abs[:begin].rfind('. '.encode("utf-8"))
            #修改此处
            elif chr(abs[begin+2]).strip()[0].isupper():
                break
            else:
                begin = abs[:begin].rfind('. '.encode("utf-8"))        
            pre = abs[:begin]
            
    if begin <= e1_begin and (end >= e2_end or end == -1):
        sent = abs[begin+2:end]
        #print(sent)
        offset = len(abs[:begin+2])
        e1, e2 = sent[e1_begin-offset: e1_end-offset], sent[e2_begin-offset: e2_end-offset]
        sent = sent[:e1_begin-offset] + E1_B.encode("utf-8") \
           + sent[e1_begin-offset: e1_end-offset] + E1_E.encode("utf-8")\
            + sent[e1_end-offset: e2_begin-offset] + E2_B.encode("utf-8")\
             + sent[e2_begin-offset: e2_end-offset] + E2_E.encode("utf-8")\
              + sent[e2_end-offset:]
        return e1, e2, sent
    else:
        return None, None, None
    

def read_CPR_corpus(abs_file, entity_file, rel_file=None):
    
    '''
        read abstracts as a map from pmid to the abstract content
    '''
    abs_map = {}
    for line in open(abs_file,encoding="utf-8"):
        #line = line.decode("utf-8")
        line = line.encode("utf-8")
        #修改此处了，partition改为了split
        pid, _, text =line.strip().partition('\t'.encode('utf-8'))
        #if abs_map.has_key(pid):
        if pid in abs_map.keys():
            print ('Nao Gui Le!')
            os._exit(0)
        else:
            abs_map[pid] = text.replace('\t'.encode("utf-8"), ' '.encode("utf-8"))
    
    '''
        read entity file as a nested map from pmid to Eid to entity content 
    '''
    entity_map = {}
    count_entity=0
    for line in open(entity_file,encoding="utf-8"):
        line = line.encode("utf-8")
        count_entity=count_entity+1
        splited = line.strip().split('\t'.encode("utf-8"))
        #if entity_map.has_key(splited[0]):
        if splited[0] in entity_map.keys():
            #if entity_map[splited[0]].has_key(splited[1]):
            if splited[1] in entity_map[splited[0]].keys():
                print ('Jian Gui Le!')
                os._exit(0)
            else:
                entity_map[splited[0]][splited[1]] = splited[2:]
        else:
            entity_map[splited[0]] = {splited[1]:splited[2:]}
            
            
    '''
        read relation files and generate the final output file
    '''
    instances = []
    for line in open(rel_file):
        line = line.encode("utf-8")
        rel_splited = line.strip().split('\t'.encode("utf-8"))
        pid = rel_splited[0]
        #if entity_map.has_key(rel_splited[0]):
        if rel_splited[0] in entity_map.keys():
            e1_id = rel_splited[4].partition(':'.encode("utf-8"))[2]
            e2_id = rel_splited[5].partition(':'.encode("utf-8"))[2]
            e1 = entity_map[pid][e1_id]
            e2 = entity_map[pid][e2_id]
            e1_begin = int(e1[1])
            e1_end = int(e1[2])
            e2_begin = int(e2[1])
            e2_end = int(e2[2])
            
            if e1_begin < e2_begin:
                type = analyse_two_offsets([e1_begin, e1_end], [e2_begin, e2_end])
                if type == 'normal':
                    e11, e22, sent = extract_instance_from_abs(abs_map[pid], e1_begin, e1_end, e2_begin, e2_end)
                    if sent is not None:
                        if e11!= e1[3] or e22 != e2[3]:
                            pass
                        else:
                            print(rel_splited[1])
                            instances.append((rel_splited[1].decode("utf-8") + "\t"+ sent.decode("utf-8")))
                    else:
                        pass
                else:
                    pass
#                     print type, e1[3], e2[3], rel_splited[1]
            else:
                type = analyse_two_offsets([e2_begin, e2_end], [e1_begin, e1_end])
                if type == 'normal':
                    e11, e22, sent = extract_instance_from_abs(abs_map[rel_splited[0]], e2_begin, e2_end, e1_begin, e1_end)
                    if sent is not None:
                        if e11!= e2[3] or e22 != e1[3]:
                            pass
                        else:
                            instances.append((rel_splited[1].decode("utf-8") + '\t'+ sent.decode("utf-8")))
                        pass
                    else:
                        pass
                else:
                    pass
#                     print type, e1[3], e2[3] , rel_splited[1]            
        else:
            print ('Zhen Jian Gui Le!')
            os._exit(0)
    
    return instances

if __name__ == '__main__':
    dir ='C:/Users/Administrator/Desktop/ChEMPROT/'
    choice=sys.stdin.readline().strip()
    if choice=="test":
        entity_file = dir + 'chemprot_test_gs/chemprot_test_entities_gs.tsv'
        abs_file = dir + 'chemprot_test_gs/chemprot_test_abstracts_gs.tsv'
        rel_file = dir + 'chemprot_test_gs/chemprot_test_relations_gs.tsv'
        
    else:
        entity_file = dir + 'chemprot_training/chemprot_training_entities.tsv'
        abs_file = dir + 'chemprot_training/chemprot_training_abstracts.tsv'
        rel_file = dir + 'chemprot_training/chemprot_training_relations.tsv'
    instances = read_CPR_corpus(abs_file, entity_file, rel_file)
    i=0
    instances2=[]
    for item in instances:
        if isinstance(item,bytes):
            instances2.append(item.decode("utf-8"))
        else:
            instances2.append(item)
    while(i<10): 
        print(instances2[i])  
        i=i+1
    if choice=="test":
        FileUtil.writeStrLines(dir + 'chemprot_training/test.embed', instances2)
        
    else:
        FileUtil.writeStrLines(dir + 'chemprot_test_gs/train.embed', instances2)

    
        
        