from os import path
import sys

#对应替换文本
replaced_dict={
    "CHEMICAL":["CHEMICALIN","CHEMICALNOTIN"],
    "GENE-Y":["GENEIN","GENENOTIN"],
    "GENE-N":["GENEIN","GENENOTIN"]
}
EPLACED_GENE_IN = "GENEIN"
REPLACED_CHEMICAL_IN = "CHEMICALIN"
EPLACED_GENE_NOT_IN = "GENENOTIN"
REPLACED_CHEMICAL_NOT_IN = "CHEMICALNOTIN"

def test(entity_map,relation_map):
    in_relation=0
    not_in_relation=0
    wrong_entity=0
    for pid,entities in entity_map.items():
        if pid in relation_map.keys():
            in_relation += 1
            print("Article_id:{}".format(pid))
            for entity in entities.values():
                if entity[3] not in ["CHEMICALIN","CHEMICALNOTIN","GENEIN","GENENOTIN"]:
                    print(entity)
                    wrong_entity+=1

        else:
            print("Article_id:{}===============================".format(pid))
            not_in_relation+=1
    print(in_relation)
    print(not_in_relation)
    print(wrong_entity)




def map_to_abs(abs_map,save_path):
    with open(save_path,"w") as f:
        for key,abstract in abs_map.items():
            f.writelines(key+"\t"+abstract+"\n")

def map_to_entity(entity_map,save_path):
    with open(save_path,"w") as f:
        for pid,entities in entity_map.items():

            for entity,value in entities.items():
                write_instance = list()
                write_instance.append(pid)
                write_instance.append(entity)
                write_instance.extend(value)
                write_instance="\t".join(write_instance)+"\n"
                f.writelines(write_instance)






def get_abs_map(abs_file):
    abs_map = {}
    for line in open(abs_file):
        line = line
        pid, _, text = line.strip().partition('\t')
        abs_map[pid] = text.replace('\t', ' ')
    return abs_map
def get_relation_map(rel_file):
    relation_map={}
    for line in open(rel_file):
        rel_splited = line.strip().split('\t')
        pid = rel_splited[0]
        arg1,arg2=rel_splited[4].split(":")[1],rel_splited[5].split(":")[1]
        if pid not in relation_map.keys():
            relation_map[pid]=[]
        relation_map[pid].append(arg1)
        relation_map[pid].append(arg2)
    for key,value in relation_map.items():
        relation_map[key]=set(value)
    return relation_map
def get_entity_map(entity_file):
    entity_map = {}
    count_entity = 0
    for line in open(entity_file):
        line = line
        count_entity = count_entity + 1
        splited = line.strip().split('\t')
        if splited[0] in entity_map.keys():
            entity_map[splited[0]][splited[1]] = splited[2:]
        else:
            entity_map[splited[0]] = {splited[1]: splited[2:]}
    return entity_map

def replacement_strategy1(abs_map,entity_map,relation_map):
    pass



def replace_func(abs_map,entity_map,relation_map):
    entity_all=0
    entity_overlap=0
    all=0
    for article_id in entity_map.keys():
        print("\narticle_id:{}".format(article_id))
        #按照坐标位置排序
        if article_id not in relation_map.keys():
            print("这篇文章不存在关系集合，跳过。")
            continue
        entity_sorted=sorted(entity_map[article_id].items(),key=lambda x:int(x[1][1]))
        entity_num=len(entity_sorted)
        entity_all+=entity_num
        #遍历所有的实体，查询重合部分
        flag=0
        this_overlap=0
        for i in range(entity_num):
            if flag==1:

                flag=0
            i = i - this_overlap
            if i >=len(entity_sorted):
                break
            if i<(len(entity_sorted)-1) and int(entity_sorted[i+1][1][1])<int(entity_sorted[i][1][2]) and\
                    int(entity_sorted[i + 1][1][1]) > int(entity_sorted[i][1][1]) :
                del entity_sorted[i+1]
                this_overlap+=1
                flag=1
                continue
            # 重合部分
            if i<len(entity_sorted)-1 and entity_sorted[i][1][1]==entity_sorted[i+1][1][1]:
                #前者和后者都在关系集合中
                if entity_sorted[i][0] in relation_map[article_id] and\
                    (entity_sorted[i + 1][0] in relation_map[article_id]):
                    print("=======")
                    print("{}".format(entity_sorted[i]))
                    print("{}".format(entity_sorted[i + 1]))
                    print("=======")
                    all+=1
                    entity_overlap += 1
                    this_overlap += 1
                    if entity_sorted[i][1][2] >= entity_sorted[i + 1][1][2]:
                        del entity_sorted[i + 1]
                    else:
                        del entity_sorted[i]
                    choice=0

                else:
                    #前者在关系集合中
                    if entity_sorted[i][0] in relation_map[article_id]:
                        print("\n前者in:{}".format(entity_sorted[i]))
                        print("not in:{}".format(entity_sorted[i+1]))
                        entity_overlap += 1
                        del entity_sorted[i+1]
                        choice=0
                        this_overlap += 1
                    #后者在关系集合中
                    elif entity_sorted[i+1][0] in relation_map[article_id]:
                        print("\n后者in:{}".format(entity_sorted[i + 1]))
                        print("not in:{}".format(entity_sorted[i]))
                        entity_overlap += 1
                        del entity_sorted[i]
                        choice=0
                        this_overlap += 1
                    else:
                        #entity不在关系集合中，就长原则替换
                        if int(entity_sorted[i][1][2])>=int(entity_sorted[i+1][1][2]):
                            del entity_sorted[i+1]
                        else:
                            del entity_sorted[i]
                        choice=1
                        this_overlap += 1
                flag=1
                continue
            # 非重合部分,直接替换
            else:
                #不在relation集合中的实体，采取的操作，是直接替换
                if entity_sorted[i][0] not in relation_map[article_id]:
                    choice=1
                else:
                    choice=0
            #只要修改entity和abs中
            # 更改abs.
            string = abs_map[article_id]
            string = string[:int(entity_sorted[i][1][1])] + replaced_dict[entity_sorted[i][1][0]][
                choice] + string[int(entity_sorted[i][1][2]):]
            abs_map[article_id] = string

            entity_sorted[i][1][2]=int(entity_sorted[i][1][1])+len(replaced_dict[entity_sorted[i][1][0]][choice])
            entity_sorted[i][1][2]=str(entity_sorted[i][1][2])
            minus=len(entity_sorted[i][1][3])-len(replaced_dict[entity_sorted[i][1][0]][choice])
            entity_sorted[i][1][3]=replaced_dict[entity_sorted[i][1][0]][choice]
            #更改entity_sorted后边的部分
            def modify_residual_entity_sorted(i, entity_sorted,minus):
                for j in range(i+1,len(entity_sorted)):
                    entity_sorted[j][1][1]=str(int(entity_sorted[j][1][1])-minus)
                    entity_sorted[j][1][2]=str(int(entity_sorted[j][1][2])-minus)
                return entity_sorted
            entity_sorted=modify_residual_entity_sorted(i,entity_sorted,minus)
        new_entity_dict={}
        for item in entity_sorted:
            new_entity_dict[item[0]]=item[1]
        entity_map[article_id]=new_entity_dict





    print("entity总数：{}".format(entity_all))
    print("entity重合：{}".format(entity_overlap))
    print("在关系集合中都出现的对数：{}".format(all))
    print("abstract 文章总数：{}".format(len(abs_map)))
    print("entity 中 文章总数：{}".format(len(entity_map)))
    print("relation 中 文章总数：{}".format(len(relation_map)))
    return abs_map,entity_map,relation_map

def analyse(abs_map,entity_map,relation_map):
    minus_entity_count={}
    for key in entity_map.keys():
        if key in relation_map.keys():
            minus_entity_count[key]=[len(entity_map[key]),len(relation_map[key]),len(entity_map[key])-len(relation_map[key])]

    entity_all=0
    entity_in_relation=0
    minus=0
    for key,value in minus_entity_count.items():
        print("key:{},values:{}".format(key,value))
        entity_all+=value[0]
        entity_in_relation+=value[1]
        minus+=value[2]

    print("all:{},in relation:{},mnius:{}".format(entity_all,entity_in_relation,minus))

def main():
    # dir ='/Users/lijingjing/Documents/PycharmProjects/relation/data/ChEMPROT/'
    # data root dir
    this_dir = path.dirname(__file__)
    parent_path = path.dirname(this_dir)
    dir = path.dirname(parent_path) + "/data/ChEMPROT/"
    print(dir)


    choice = sys.stdin.readline().strip()
    if choice != 'test':
        entity_file = dir + 'chemprot_training/chemprot_training_entities.tsv'
        abs_file = dir + 'chemprot_training/chemprot_training_abstracts.tsv'
        rel_file = dir + 'chemprot_training/chemprot_training_relations.tsv'

        save_entity_file = dir + 'chemprot_training/chemprot_training_entities_replaced.tsv'
        save_abs_file = dir + 'chemprot_training/chemprot_training_abstracts_replaced.tsv'
        save_rel_file = dir + 'chemprot_training/chemprot_training_relations_replaced.tsv'

    else:
        entity_file = dir + 'chemprot_test_gs/chemprot_test_entities_gs.tsv'
        abs_file = dir + 'chemprot_test_gs/chemprot_test_abstracts_gs.tsv'
        rel_file = dir + 'chemprot_test_gs/chemprot_test_relations_gs.tsv'

        save_entity_file = dir + 'chemprot_test_gs/chemprot_test_entities_gs_replaced.tsv'
        save_abs_file = dir + 'chemprot_test_gs/chemprot_test_abstracts_gs_replaced.tsv'
        save_rel_file = dir + 'chemprot_test_gs/chemprot_test_relations_gs_replaced.tsv'

    #主函数部分
    abs_map=get_abs_map(abs_file)
    entity_map=get_entity_map(entity_file)
    relation_map=get_relation_map(rel_file)
    # analyse(abs_map,entity_map,relation_map)
    abs_map, entity_map, relation_map=replace_func(abs_map,entity_map,relation_map)
    map_to_abs(abs_map,save_abs_file)
    # print(entity_map)
    map_to_entity(entity_map,save_entity_file)
    # abs_map, entity_map, relation_map = replace_func(abs_map, entity_map, relation_map)
    # test(entity_map,relation_map)

if __name__=="__main__":
    main()