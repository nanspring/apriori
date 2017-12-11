import numpy as np
import pandas as pd
import itertools
import timeit

def find_frequent_1_itemsets(data,minSupport,names):

    freq_1_itemset={}
    for attName in names:
        freq_temp=list()
        attData=np.array(data.ix[:,attName].copy())
        uniqueData=np.unique(attData)
        for element in uniqueData:
            support=np.count_nonzero(attData==element)
            if ((support>=minSupport)and(element not in freq_temp)):
                freq_temp.append(element)
        if(len(freq_temp)>0):
            freq_1_itemset.update({attName:freq_temp})
    print("frequent 1: ",freq_1_itemset)
    print()
    return freq_1_itemset

def infrequent_subset(candidates,itemset_prev):
    candSubset=list()
    t=itertools.combinations(candidates, len(candidates)-1)
    for i in t:
        temp=[]
        for j in i:
            temp.append(j)
        candSubset.append(temp)
    for c in candSubset:
        if c not in itemset_prev:
            return True
    return False

def gen_candidate(item_prev,k):#item_prev is a dictionary
    #print("k  ",k)
    candidates=list()
    if(k==2):
        iteralAtt=list(itertools.combinations(item_prev.keys(),k))
        itemset=list(item_prev.values())
        for nameComb in iteralAtt:
            temp=list()
            for j in nameComb:
                temp2=item_prev.get(j)
                temp.append(temp2)
            for element in itertools.product(*temp):
                candidates.append(list(element))
        for c in candidates:
            if(infrequent_subset(c,itemset)==True):
                candidates.remove(c)
    else:

        for i in item_prev:
            for j in item_prev:
                cand=[]
                if(len(set(j)-(set(i)))==1):
                    temp=set(j)-(set(i))
                    for n in i:
                        cand.append(n)
                    for m in temp:
                        cand.append(m)
                    #print("cand ",cand)
                    if(infrequent_subset(cand,item_prev)==False):
                        #print("add")
                        candidates.append(cand)

    finalResult=list()

    for c in candidates:
        if c not in finalResult:
            finalResult.append(c)
    #print("finalResult ",finalResult)
    return finalResult


def apriori_algo(dataframe,minSupport,names):
    L_Total={}
    dataValue=dataframe.values.tolist()
    L_1=find_frequent_1_itemsets(dataframe,minS,names)
    L_Total.update({1:L_1})
    k=2
    while(L_Total.get(k-1)!=None):
        candidates_prev=gen_candidate(L_Total.get(k-1),k)
        candTuple=(tuple(l) for l in candidates_prev)
        if(len(candidates_prev)==0):
            return
        L_count=dict.fromkeys(candTuple,0)
        for transaction in dataValue:
            for cand in candidates_prev:
                if(set(cand)<set(transaction)):
                    L_count[tuple(cand)]=L_count[tuple(cand)]+1
        final=list()
        for cand in candidates_prev:
            #print("candidate ",cand," count",L_count.get(tuple(cand)))
            if(L_count.get(tuple(cand))>=minSupport):
                #print("remove")
                final.append(cand)
        candidates_prev=final


        L_Total.update({k:candidates_prev})
        print("L_",k,candidates_prev)
        print()
        print()
        k=k+1

#since the first frequent itemset, we know capital gain and loss item is 0. Therefore, to solve the confusion between
#two zeros, I change captain gain 0 to 'Cap_G_0' and captain loss 0 to 'Cap_L_0'
url="http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

attributeNames=['age','workclass','final sample weight','education','education num','martial status','occupation',
'relationship','race','sex','captain_gain','captain_loss','hours per week','native country','50K']
data=pd.read_csv(url,names=attributeNames)
data.loc[data['captain_gain']!=0, 'captain_gain'] = 'Cap_G_not_0'
data.loc[data['captain_gain']==0, 'captain_gain'] = 'Cap_G_0'
data.loc[data['captain_loss']!=0, 'captain_loss'] = 'Cap_L_not_0'
data.loc[data['captain_loss']==0, 'captain_loss'] = 'Cap_L_0'
minS=32561*0.4
apriori_algo(data,minS,attributeNames)
