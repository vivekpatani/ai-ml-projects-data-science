from buildtree import *  
from math import log

def pessimistic_error(rows):
    error=group_by_count(rows)
    pessimistic_error=sum([i for i in error.values() if i!=max(error.values())])
    return pessimistic_error

def  mdl_error(row1,row2): 

     error=group_by_count(row1+row2)
     higher=group_by_count(row1)
     lower=group_by_count(row2)

     no=len(error)
     features=4
     
     e=sum([i for i in error.values() if i!=max(error.values())])
     e1=sum([i for i in higher.values() if i!=max(higher.values())])
     e2=sum([i for i in lower.values() if i!=max(lower.values())])
     
     log2=lambda x:log(x)/log(2)
     
     mdl=log2(features)+2*log2(no)+(e1+e2-e)*log2(1372)
     return mdl




def prune(tree):
  if tree.tb.results==None:
    prune(tree.tb)
  if tree.fb.results==None:
    prune(tree.fb)
    
  if tree.tb.results!=None and tree.fb.results!=None:
    tb,fb=[],[]
    for v,c in tree.tb.results.items():
      tb=tb+[[v]]*c
    for v,c in tree.fb.results.items():
      fb=fb+[[v]]*c
    
    pes_error=pessimistic_error(tb+fb)-((pessimistic_error(tb)+pessimistic_error(fb))+1)
    

    if pes_error<=0:
      tree.tb,tree.fb=None,None
      tree.results=group_by_count(tb+fb)
  return tree