#Loading the Data
setwd("D:/dm-2/final/q2/b-c")
data_dump<-read.table("wine.csv", header=FALSE,sep=",")
colnames(data_dump) <- c("Alcohol","Malic_acid","Ash","Alcalinity_of_ash","Magnesium","Total_phenols","Flavanoids","Nonflavanoid_phenols","Proanthocyanins","Color_intensity","Hue","OD280/OD315_of_diluted_wines","Proline")
  data_dump
  eucledian(data_dump)
  eucledian<-function(data_dump){
    
    #Just go to each data point and then calculate with every other data point.
    total = nrow(data_dump)
    #cat(total)
    flag = 0
    count = 0
    total_class1 = total - 60
    total_class2 = total - 15
    total_class3 = total - 43
    count_class1 = 0
    count_class2 = 0
    count_class3 = 0
    #For Standard Normalising the data first
    #Eliminate the Class variable column while normalising
    #Before computation add it
    #for(a in 1:total){
     # 
      #  temp = normalise(data[a])
      #  data[a] = temp
      #
    #}
    for (each_row in 1:total){
      minimum = Inf
      flag = total - 1
      point1=data_dump[each_row,1]
      #cat(point1)
      #Find out minimum distance for that particular point
      for (other_row in 1:total){
        if(each_row!=other_row){
          point2 = data_dump[other_row,1]
          distance = dist(rbind(point1,point2))
          #cat(minimum,distance)
          if(distance[1]<=minimum){
            minimum = distance[1]
            #cat("MIN")
            #cat(distance[1])
            #cat(minimum)
            flag = other_row
            #point = data[flag,1]
          }
        }
      if((data_dump[each_row,1]==data_dump[flag,1]))
        #print(count)
        count = count+1
      if((data_dump[each_row,1]==1))
        if(data_dump[flag,1]==1)
          count_class1 = count_class1+1
      if((data_dump[each_row,1]==data_dump[60,1]))
        if(data_dump[each_row,1]==2)
          count_class2 = count_class2 + 1
      if((data_dump[each_row,1]==data_dump[178,1] ))
        if((data_dump[178,1])==3)
        count_class3 = count_class3 + 1
      }
    }
    #print(data_dump[178,1])
    print(count_class1/total_class1)
    print(count_class2/total_class2)
    print(count_class3/total_class3)
  }
#0-1 Normalisation
normalise  <- function(x) {
    final_data1 <- (x - min(x, na.rm=TRUE))/(max(x,na.rm=TRUE) -min(x, na.rm=TRUE))
  return (final_data1)
  }
  
#Z Score Normalisation
z_score<-function(x){
    scale(x)
    final_data <- x - mean(x) / sd(x)
    return (final_data)
  }