import pandas as pd
import numpy as np
import math
import operator
from operator import attrgetter
from collections import OrderedDict
import sys
import os

class InfoGain_RootNode:
    RuleList = []
    def __init__(self, TrgtAttrKey,headerKey,headervalue,lineKey,linevalue):
        self.TrgtAttrKey = TrgtAttrKey
        self.headerKey = headerKey
        self.headervalue = headervalue
        self.lineKey = lineKey
        self.linevalue = linevalue
        self.RuleList.append(self)


def searchKey(TrgtAttrKey,headerKey,lineKey):
    count=0
    for i in InfoGain_RootNode.RuleList:
        if i.lineKey == lineKey and i.headerKey==headerKey and i.TrgtAttrKey ==TrgtAttrKey:
            count = i.linevalue
            return count
    return count

def addValueToExistingList(TrgtAttrKey,headerKey,linekey,lineval):
    for i in InfoGain_RootNode.RuleList:
        if  (i.headerKey==headerKey) and (i.TrgtAttrKey==TrgtAttrKey) and (i.lineKey==linekey):
            i.linevalue +=1
            i.headervalue += 1
            break
#This is a recursive function which keeps on calling himself unless only pure node is remaining or the number of split attributes are over.
def Recursion(dataFrame,Root,child,TrgtIndex,listOfattributes,ParentOrChild):
    counter=0
    check = 0
    Root_New = CalculateBestAttributetoSplit(dataFrame)
    df_1 = dataFrame[[Root_New, target_attribute]]
    for j in df_1[Root_New].unique():
        df1_new = df_1[df_1[Root_New]==j]
        df1_Full = dataFrame[dataFrame[Root_New] == j]
        attr1 = ''
        attr1Val = 0
        attr2 = ''
        attr2Val = 0
        for key,val in df1_new.iteritems():
            for  c in val:
                if j!=c:
                    if attr2 != '' and attr2!=c:
                        attr1 = c
                        attr1Val += 1
                    else:
                        attr2 = c
                        attr2Val += 1
        if attr1Val!=0 and attr2Val!=0:
            Entropy = - (float(attr1Val)/(attr1Val + attr2Val) * math.log(float(attr1Val)/(attr1Val + attr2Val))/math.log(2)) - (float(attr2Val)/(attr1Val + attr2Val) * math.log(float(attr2Val)/(attr1Val + attr2Val))/math.log(2))
            infoOFAttribute = (float(attr1Val + attr2Val)/TotalRowsOfDataSet) * Entropy
            if listOfattributes - (TrgtIndex+1) == 1:
                positive=''
                positiveCnt = 0
                negative=''
                negativeCnt = 0
                #check the values of positives and negatives in dataset, and based on that decide which one to print.
                for vn in df_1[[Root_New,target_attribute]].groupby([target_attribute]):
                    for v1 in vn[-1:]:
                        for index,v2 in v1.iterrows():
                            if positive!='' and positive!=v2[target_attribute]:
                                negative=v2[target_attribute]
                                negativeCnt+=1
                            else:
                                positive = v2[target_attribute]
                                positiveCnt += 1
                P=''
                N=''
                for j in df_1[Root_New].unique():
                    for key, val in df_1.iteritems():
                        for c in val:
                            if positiveCnt > negativeCnt:
                                if c == positive and P!=j:
                                    f.write( '------If ' + Root_New + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(positive)+ '\n')
                                    ListToStoreDataForAccuracy.append(Root_New)
                                    ListToStoreDataForAccuracy.append(j)
                                    ListToStoreDataForAccuracy.append(key)
                                    ListToStoreDataForAccuracy.append(positive)
                                    P = j
                            else:
                                if c == negative and N!=j:
                                    f.write( '------If ' + Root_New + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(negative)+ '\n')
                                    ListToStoreDataForAccuracy.append(Root_New)
                                    ListToStoreDataForAccuracy.append(j)
                                    ListToStoreDataForAccuracy.append(key)
                                    ListToStoreDataForAccuracy.append(positive)
                                    N=j
                break
            else:
                f.write( '---If ' +Root_New+ ' is ' + str(j) + ' ,Then ' + '\n')
                ListToStoreDataForAccuracy.append(Root_New)
                ListToStoreDataForAccuracy.append(j)
                dataframe = df1_Full[df1_Full[Root_New] == j]
                Recursion(dataframe, Root_New, child, TrgtIndex+1,listOfattributes,2)
        elif attr1Val==0:
            Entropy =  0 - (float(attr2Val) / (attr1Val + attr2Val) * math.log(float(attr2Val) / (attr1Val + attr2Val)) / math.log(2))
            infoOFAttribute = (float(attr1Val + attr2Val) / TotalRowsOfDataSet) * Entropy
            if int(ParentOrChild)==1:
                f.write( '---If ' + Root_New + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(c) + '\n')
                ListToStoreDataForAccuracy.append(Root_New)
                ListToStoreDataForAccuracy.append(j)
            if int(ParentOrChild)==2:
                f.write( '-------If ' + Root_New + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(c) + '\n')
                ListToStoreDataForAccuracy.append(Root_New)
                ListToStoreDataForAccuracy.append(j)
            check+=1
        attr1Val = 0
        attr2Val = 0
        attr2 = ''
        attr1 = ''
    counter+=1

filename = raw_input("Enter a file name:")
filename = filename.strip()
if os.path.exists(filename)==False:
    filename = raw_input("Please Enter correct file name:")
    filename = filename.strip()

filename1 = raw_input("Enter a file name for Test data:")
filename1 = filename.strip()
if os.path.exists(filename1)==False:
    filename1 = raw_input("Please Enter correct file name for Test data:")
    filename1 = filename.strip()

tgtAttr={}
headers={}

df2 = pd.read_csv(filename,delim_whitespace=True)
TotalRowsOfDataSet =   len(df2.index)
TargetAttributes = df2.unstack().groupby(level=0).nunique()
tgtAttrDict={}
print 'The list of target attributes available are: '
count=0
countHeadr=0
for i,v in TargetAttributes.iteritems():
    #print i,v
    if v<=2:
        tgtAttr[i]=v
        count+=1
        tgtAttrDict[i]=count
        print('{:2}: {:2}'.format(count,i))
    countHeadr += 1
    headers[i]=countHeadr

TargetInput = raw_input("Please Enter only one Integer value from the above:")
tgtfound=0
for ktgt,valtgt in tgtAttrDict.items():
    if valtgt == int(TargetInput):
        target_attribute = ktgt
        tgtfound=1
if tgtfound==0:
    TargetInput = raw_input("You have entered an incorrect value. Please Re-Enter one Integer value from the above:")


#Find the Information gain of target attribute
dic={}
dic2={}
infoGain_Trgt=0
dic = df2.groupby([target_attribute]).count()
SumOfTargerAttr = df2.groupby([target_attribute]).count().sum()[0]
check=0
for k,v in dic.iteritems():
    if check<2:
        for k2,v2 in v.iteritems():
            infoGain_Trgt -= float(v2)/float(SumOfTargerAttr) * math.log(float(v2)/float(SumOfTargerAttr))/math.log(2)
            check+=1
    else:
        break

rootNode={}

#process to calculate entropy and info gain for each attributes.
def CalculateBestAttributetoSplit(Dataset):
    #calculate info gain of target attribute first
    infoGain_Trgt = 0
    dic = Dataset.groupby([target_attribute]).count()
    SumOfTargerAttr = Dataset.groupby([target_attribute]).count().sum()[0]
    check = 0
    for k, v in dic.iteritems():
        if check < 2:
            for k2, v2 in v.iteritems():
                infoGain_Trgt -= float(v2) / float(SumOfTargerAttr) * math.log(
                    float(v2) / float(SumOfTargerAttr)) / math.log(2)
                check += 1
        else:
            break

    #calculate info gain of rest attributes
    df1 = Dataset.transpose()
    ChildNode = {}
    InfoGain_RootNode.RuleList = []

    for key,val in headers.items():
        for k,val in df1.iteritems():
            trgtAttr=''
            attr=''
            line=''
            count=1
            check=1
            for k2,val2 in val[[key,target_attribute]].iteritems():
                if trgtAttr=='':
                    trgtAttr=k2
                if attr =='':
                    attr=val2
                if check==2:
                    line=val2
                check+=1
            if searchKey(trgtAttr,attr,line)>0:
                addValueToExistingList(trgtAttr, attr, line, count)
            else:
                Rule = InfoGain_RootNode(trgtAttr, attr,count, line, count)

        trgtattr=''
        attr1=''
        attrVal=0
        attr2=''
        attr2Val = 0
        infoOFAttribute=0
        Entropy=0
        gainofChild=0
        for i in  df2[[trgtAttr]].groupby([trgtAttr]):
            for j in i[:1]:
                trgtattr=j
                for i in InfoGain_RootNode.RuleList:
                    if i.headerKey == trgtattr:
                        if attr2!='':
                            attr1=i.lineKey
                            attrVal+=i.linevalue
                        else:
                            attr2 = i.lineKey
                            attr2Val += i.linevalue
                if attrVal!=0 and attr2Val!=0:
                    Entropy = - (float(float(attrVal)/ float(attrVal + attr2Val)) * math.log(float(attrVal)/ float(attrVal + attr2Val))/math.log(2)) - (float(float(attr2Val)/float(attrVal + attr2Val)) * math.log(float(attr2Val)/ float(attrVal + attr2Val))/math.log(2))
                    infoOFAttribute += (float(attrVal + attr2Val)/SumOfTargerAttr) * Entropy
                elif attrVal==0:
                    if attr2Val!=0:
                        Entropy =  0 - (float(float(attr2Val) / float(attrVal + attr2Val)) * math.log(float(attr2Val) / float(attrVal + attr2Val)) / math.log(2))
                        infoOFAttribute += (float(attrVal + attr2Val) / SumOfTargerAttr) * Entropy
                attrVal = 0
                attr2Val = 0
                attr2 = ''
                attr1 = ''
        gain = infoGain_Trgt - infoOFAttribute
        if trgtAttr != target_attribute:
            rootNode[trgtAttr]=gain
    sorterDictOnValues = sorted([(v, k) for (k, v) in rootNode.items()], reverse=True)
    check =0
    Root=''
    for k in sorterDictOnValues:
        if check==0:
            Root = str(k).split(',')[1]
            Root = Root.replace("'", '')
            Root = Root.replace(")", '').strip()
            check+=1
    return Root

#################################################################### Main Program ##############################
#start recursive loop
path = '/users/grad/bhalla/assign4/Output.txt'
ListToStoreDataForAccuracy=[]
# Delete file test2.txt
if os.path.exists(path):
    os.remove(path)

cnt = 1
f = open(path, 'w+')

firstIteration=0
if firstIteration==0:
    CalculateBestAttributetoSplit(df2) #This finction will calculate the best attribute to split on
sorterDictOnValues = sorted([(v,k) for (k,v) in rootNode.items()], reverse=True)
indexOfSortedDic=0
loopTill1=0
for k in sorterDictOnValues:
    if loopTill1==0:
        Root =  str(k).split(',')[1]
        Root = Root.replace("'",'')
        Root = Root.replace(")", '').strip()
        f.write('\n')
        f.write('The Target Attribute is: ' + target_attribute + '\n')
        f.write('\n')
        f.write('Decision Tree:' + '\n')
        f.write('\n')
        ListToStoreDataForAccuracy.append(target_attribute)
        df1= df2[[Root, target_attribute]]

        for j in df1[Root].unique():
            df1_new = df1[df1[Root]==j]
            attr1 = ''
            attr1Val = 0
            attr2 = ''
            attr2Val = 0
            for key,val in df1_new.iteritems():
                for  c in val:
                    if j!=c:
                        if attr2 != '' and attr2!=c:
                            attr1 = c
                            attr1Val += 1
                        else:
                            attr2 = c
                            attr2Val += 1
            if attr1Val!=0 and attr2Val!=0:
                Entropy = - (float(attr1Val)/(attr1Val + attr2Val) * math.log(float(attr1Val)/(attr1Val + attr2Val))/math.log(2)) - (float(attr2Val)/(attr1Val + attr2Val) * math.log(float(attr2Val)/(attr1Val + attr2Val))/math.log(2))
                infoOFAttribute = (float(attr1Val + attr2Val)/TotalRowsOfDataSet) * Entropy
                gain = infoGain_Trgt - infoOFAttribute
                indexOfSortedDic+=1
                if len(sorterDictOnValues) - indexOfSortedDic ==1: #No Further attribute to split
                    f.write( 'If ' + Root + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(attr1) + '\n')
                    f.write( 'If ' + Root + ' is ' + str(j) + ' then, ' + str(key) + ' is ' + str(attr2) + '\n')
                    ListToStoreDataForAccuracy.append(j)
                    ListToStoreDataForAccuracy.append(key)
                    ListToStoreDataForAccuracy.append(attr2)
                    break
                else:
                    f.write( 'If ' + Root + ' is ' + j + ' ,Then ' + '\n')
                    ListToStoreDataForAccuracy.append(j)
                    ListToStoreDataForAccuracy.append(Root)
                    dataframe = df2[df2[Root]==j]
                    Recursion(dataframe, Root, str(j), 1, len(sorterDictOnValues),1)
            elif attr1Val==0:
                Entropy =  0 - (float(attr2Val) / (attr1Val + attr2Val) * math.log(float(attr2Val) / (attr1Val + attr2Val)) / math.log(2))
                infoOFAttribute = (float(attr1Val + attr2Val) / TotalRowsOfDataSet) * Entropy
                gain = infoGain_Trgt - infoOFAttribute
                f.write('\n')
                f.write( 'If ' +Root+ ' is ' +str(j)+ ' then, ' + str(key) + ' is ' + str(c) + '\n')
                ListToStoreDataForAccuracy.append(j)
                ListToStoreDataForAccuracy.append(Root)
                ListToStoreDataForAccuracy.append(key)
                f.write('\n')
            attr1Val = 0
            attr2Val = 0
            attr2 = ''
            attr1 = ''
    else:
        break
    loopTill1+=1
f.close()
print('')
print('Decision Tree Generated!' + '\n')
print('file is saved in the following path: ' +path + '\n')

