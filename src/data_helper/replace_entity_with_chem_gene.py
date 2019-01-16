import os
import sys

dir ='/Users/lijingjing/Documents/PycharmProjects/relation/data/ChEMPROT/'

save_entity_file = dir + 'chemprot_training/chemprot_training_entities_replaced.tsv'
save_abs_file = dir + 'chemprot_training/chemprot_training_abstracts_replaced.tsv'

choice=sys.stdin.readline().strip()
if choice !='test':
    entity_file = dir + 'chemprot_training/chemprot_training_entities.tsv'
    abs_file = dir + 'chemprot_training/chemprot_training_abstracts.tsv'
    rel_file = dir + 'chemprot_training/chemprot_training_relations.tsv'
else:
    entity_file = dir + 'chemprot_test_gs/chemprot_test_entities_gs.tsv'
    abs_file = dir + 'chemprot_test_gs/chemprot_test_abstracts_gs.tsv'
    rel_file = dir + 'chemprot_test_gs/chemprot_test_relations_gs.tsv'

abs_map = {}
for line in open(abs_file):
    line = line
    pid, _, text = line.strip().partition('\t')
    if pid in abs_map.keys():
        print('Nao Gui Le!')
        os._exit(0)
    else:
        abs_map[pid] = text.replace('\t', ' ')


relation_map={}
for line in open(rel_file):
    rel_splited = line.strip().split('\t')
    pid = rel_splited[0]
    arg1=rel_splited[4].split(":")[1]
    arg2=rel_splited[5].split(":")[1]
    if pid not in relation_map.keys():
        relation_map[pid]=[]
    relation_map[pid].append(arg1)
    relation_map[pid].append(arg2)
print(relation_map)
for key,value in relation_map.items():
    relation_map[key]=set(value)


entity_map = {}
count_entity = 0
for line in open(entity_file):
    line = line
    count_entity = count_entity + 1
    splited = line.strip().split('\t')
    if splited[0] in entity_map.keys():
        if splited[1] in entity_map[splited[0]].keys():
            print('Jian Gui Le!')
            os._exit(0)
        else:
            entity_map[splited[0]][splited[1]] = splited[2:]
    else:
        entity_map[splited[0]] = {splited[1]: splited[2:]}




entity_all=0
entity_overlap=0
all=0
for article_id in entity_map.keys():
    print("\narticle_id:{}".format(article_id))
    # print(entity_map[article_id])
    entity_sorted=sorted(entity_map[article_id].items(),key=lambda x:int(x[1][1]))
    entity_num=len(entity_sorted)
    entity_all+=entity_num
    for i in range(entity_num-1):
        if entity_sorted[i][1][1]==entity_sorted[i+1][1][1]:
            if article_id in relation_map.keys():
                if entity_sorted[i][0] in relation_map[article_id] and\
                    (entity_sorted[i + 1][0] in relation_map[article_id]):
                    print("=======")
                    print("{}".format(entity_sorted[i]))
                    print("{}".format(entity_sorted[i + 1]))
                    print("=======")
                    all+=1
                    entity_overlap += 1
                else:
                    if entity_sorted[i][0] in relation_map[article_id]:
                        print("\nin:{}".format(entity_sorted[i]))
                        print("not in:{}".format(entity_sorted[i+1]))
                        entity_overlap += 1
                    if entity_sorted[i+1][0] in relation_map[article_id]:
                        print("\nin:{}".format(entity_sorted[i + 1]))
                        print("not in:{}".format(entity_sorted[i]))
                        entity_overlap += 1
print("entity总数：{}".format(entity_all))
print("entity重合：{}".format(entity_overlap))
print(all)
print("abstract 文章总数：{}".format(len(abs_map)))
print("entity 中 文章总数：{}".format(len(entity_map)))
print("relation 中 文章总数：{}".format(len(relation_map)))

#计算entity中实体数，与relation中出现的实体数的差值
print(len(entity_map.keys()-relation_map.keys()))
print(len(relation_map.keys()-entity_map.keys()))

minus_entity_count={}
for key in entity_map.keys():
    minus_entity_count[key]=[len(entity_map[key]),len(relation_map[key]),len(entity_map[key])-len(relation_map[key])]
for key,value in minus_entity_count.items():
    print("key:{},values:{}".format(key,value))