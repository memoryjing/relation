from sklearn.metrics import f1_score, accuracy_score
import os
import csv
import collections

y_test=[]
all_predictions=[]
#data path
checkpoint_dir="./runs/1545206525/checkpoints/"
out_path = os.path.join(checkpoint_dir, "..", "prediction.csv")
#read data from csv
csv_reader=csv.reader(open(out_path))
for row in csv_reader:
    y,y_=int(float(row[1])),int(row[2])
    if y_ in [2,3,4,5,8]:
        y_test.append(y_)
        all_predictions.append(y)

counter=collections.Counter(all_predictions)
print("pred-counter:{}".format(counter))
counter=collections.Counter(y_test)
print("label-counter:{}".format(counter))

# # calc evaluate metric
print("pred:length:{},result:{}".format(len(all_predictions),all_predictions))
print("label:length:{},result:{}".format(len(all_predictions),y_test))

f1=f1_score(y_test,all_predictions,average='micro')
print("f1_score_micro:{}".format(f1))
f1=f1_score(y_test,all_predictions,average='macro')
print("f1_score_macro:{}".format(f1))
f1=f1_score(y_test,all_predictions,average='weighted')
print("f1_score_weighted:{}".format(f1))

f1=f1_score(y_test,all_predictions,average=None)
print("f1_score_weighted:{}".format(f1))



accuracy_s=accuracy_score(y_test,all_predictions)
print("accuracy_acore:{}".format(accuracy_s))
