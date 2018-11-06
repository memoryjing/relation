# -*- coding: utf-8 -*-

from data_helper.Constants import *


string="The  bbbbb1 kinase eeeee1  activity of EGFR was little inhibited by  bbbbb2 TT-B eeeee2  in a cell-free system."
def create_xtext_and_pos(string):     
    x_pos1=[]
    x_pos2=[]       
    x_splited=string.replace("  ", " ").strip(".").split(" ")
    print(x_splited)
    en1_pos=x_splited.index(E1_B.strip())
    en2_pos=x_splited.index(E2_B.strip())-2
    print(en1_pos)
    print(en2_pos)
    
    x_splited.remove(E1_B.strip())
    x_splited.remove(E2_B.strip())
    
    for index,value in enumerate(x_splited):
        x_pos1.append(index-en1_pos)
        x_pos2.append(index-en2_pos)
        
        print(x_pos1)
        print(x_pos2)
    x_text=" ".join(x_splited)
    x_pos1=" ".join(x_pos1)
    x_pos2=" ".join(x_pos2)
    print(x_pos1)
    print(x_pos2)
    return x_text,x_pos1,x_pos2

create_xtext_and_pos(string)



