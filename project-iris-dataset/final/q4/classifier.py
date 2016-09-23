# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 00:39:51 2016

@author: Vivek Patani
"""

import operator

def mdclassify(observation,tree):
    if tree.results!=None:
        return max(tree.results,key=lambda i:tree.results[i])
    else:
        v=observation[tree.col]
        if v==None:
            tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
            true_count=sum(tr.values())
            false_count=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            result={}
            for k,v in tr.items(): result[k]=v*tw
            for k,v in fr.items(): 
                if (k in result): result[k]=result[k] + v*fw
                else: result[k]=result.setdefault(k,0) + v*fw
            return result
        else:
            #Checking int or float
            if isinstance(v,int) or isinstance(v,float):
                if v>=tree.value: branch=tree.tb
                else: branch=tree.fb
            else:
                #Categorical
                if v==tree.value: branch=tree.tb
                else: branch=tree.fb
        return mdclassify(observation,branch)
