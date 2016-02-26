eucledian(data)
eucledian<-function(data){
  
  total = nrow(data)
  for (each_row1 in 1:nrow(data)){
    min=Inf
    index=nrow(data)-1
    x=data[each_row1,-1]
    for (other_row in 1:nrow(data)){
      if(each_row1!=other_row){
        y=data[other_row,-1]  
        d=dist(rbind(x,y))
        if (d[1]<=min) {
          min=d
          index=other_row
          }
      }
    }
    count_num = 0
    if ((data[each_row1,1])==data[index,1]){count_num=count_num+1}
    class1 = 0
    if(data[each_row1,1]==1){
      if(data[index,1]==1){class1=class1+1}
    }
    class2 = 0
    if(data[other_row,1]==2){
      if(data[index,1]==2){class2 = class2 + 1}
    }
    class3 = 0
    if(data[other_row,14]==3){
      if(data[index,1]==3){class3 = class3 +1}
    }
  }
  overall = count_num / total
  class1t = class1 / count_num
  class2t = class2 / count_num
  class3t = class3 / count_num
  
  cat(class1t,class2t,class3t)
}

normalise(data)
normalise<-function(data){
  
  zero_norm<-cbind(scale(data[2,13]))
  
  z_score <- sd(height)*sqrt((length(height)-1)/(length(height)))
  pop_mean <- mean(height)
}