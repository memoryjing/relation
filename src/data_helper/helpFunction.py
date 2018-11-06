from data_helper.Constants import *
sentence="These results suggest that the megabase DNA fragmentation is induced as \
a consequence of inhibition of thymidylate synthase by  bbbbb1 Tomudex eeeee1  and kilobase DNA fragmentation may \
correlate with the reduction of p27(kip1) expression and the increase in cyclin E and cdk2  bbbbb2 kinase eeeee2  activities"

def create_xtext_and_pos(string):    
    x_pos1=[]
    x_pos2=[]        
    x_splited=string.replace("  ", " ").strip(".").split(" ")
    en1_pos=x_splited.index(E1_B.strip())
    en2_pos=x_splited.index(E2_B.strip())-2
    
    x_splited.remove(E1_B.strip())
    x_splited.remove(E2_B.strip())
    
    for index,value in enumerate(x_splited):
        x_pos1.append(str(index-en1_pos))
        x_pos2.append(str(index-en2_pos))
        
    x_text=" ".join(x_splited)
    x_pos1=" ".join(x_pos1)
    x_pos2=" ".join(x_pos2)
    return x_text,x_pos1,x_pos2

def create_negative_cases(sentence,entities,relations=None):
    print("==========================")
    start=sentence[1][0]
    end=sentence[1][1]
    print(start)
    print(end)
    entities=[item for item in entities.items() if int(item[1][1])>=start and int(item[1][2])<=end]
    print(entities)
    
    #找实体
    chemical_entities=[item for item in entities if item[1][0]=="CHEMICAL"]
    gene_entities=[item for item in entities if item not in chemical_entities]
    
    print("chemical_entities"+str(chemical_entities))
    print("gene_entities"+str(gene_entities))
    
    #构造实体对，然后生成负例
    all_pairs=[[i,j] for i in chemical_entities for j in gene_entities]
    negative_cases=[]
    for pair in all_pairs:
        #小的在前，大的在后
        if int(pair[0][0].replace("T",""))>int(pair[1][0].replace("T","")):
            temp=pair[0]
            pair[0]=pair[1]
            pair[1]=temp
        #处理relation为空的情况，也就是pid不在relation的情况，所有的实体对都要生成负例
        if relations==None:
            negative_instance=create_negative_case(pair,sentence)
            print(negative_instance)   
            negative_cases.append(negative_instance)
        #只有不在relation中的才需要生成负例
        elif [pair[0][0],pair[1][0]] not in relations:
            negative_instance=create_negative_case(pair,sentence)
            print(negative_instance)   
            negative_cases.append(negative_instance)
    print("==========================")
    return negative_cases  



#将abstract分成单独的句子，并且每个句子有起始和结束的位置{"sentence":[start,end],....}
def create_sentence_map(abs):
    sentence_map={}
    length=len(abs)   
    start=0
    end = 0
    pre = abs[start:end+1]
    #这个循环是找到所有的句子
    while end<length:
        #这个循环是要找到一个句号
        while end < length:
            #这里原先得到的是int，需要转化为char才能判断大小写
            if pre.endswith('i.e') or pre.endswith('i.v') \
                or pre.endswith('vs')\
                or pre.endswith('i.p') or pre.endswith('i.c'):
                print(pre)
                end = abs.find('. ', end + 1)
            elif  end+1==length or abs[end+2].isupper():
                break
            else:
                end = abs.find('. ', end + 1)
            if end==-1:
                end=length-1
                break
            pre = abs[start:end]
        sentence=pre
        sentence_map[sentence]=[start,end]
        start=end+2
        end=end+3
    return sentence_map
    
    
       
def create_negative_case(pair,sentence):
    
    sent=sentence[0]
    sent_b=sentence[1][0]
    
    #find arg1 information
    arg1_b=int(pair[0][1][1])-sent_b
    arg1_e=int(pair[0][1][2])-sent_b
    #find arg2 information
    arg2_b=int(pair[1][1][1])-sent_b
    arg2_e=int(pair[1][1][2]) -sent_b
    
    sent=sent[:arg1_b]+E1_B+sent[arg1_b:arg1_e]+E1_E+sent[arg1_e:arg2_b]\
    +E2_B+sent[arg2_b:arg2_e]+E2_E+sent[arg2_e:]
    negative_case="CRP11"+'\t'+sent
    return negative_case

def get_plain_sentence(sentence):
    
    sentence=sentence.replace(E1_B,"")
    sentence=sentence.replace(E2_B,"")
    sentence=sentence.replace(E1_E,"")
    sentence=sentence.replace(E2_E,"")
    return sentence


if __name__ == '__main__':
    get_plain_sentence(sentence)