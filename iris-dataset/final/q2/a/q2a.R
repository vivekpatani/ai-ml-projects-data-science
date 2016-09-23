library(Hmisc)
data<-read.table("D:/dm-2/q-2/q-2a/results/wine.csv", header=FALSE,sep=",")
colnames(data) <- c("Alcohol","Malic_acid","Ash","Alcalinity_of_ash","Magnesium","Total_phenols","Flavanoids","Nonflavanoid_phenols","Proanthocyanins","Color_intensity","Hue","OD280/OD315_of_diluted_wines","Proline")
data_matrix <- as.matrix(data)
pearson <- rcorr(data_matrix, type="pearson")


flattenCorrMatrix <- function(cormat, pmat) {
  ut <- upper.tri(cormat)
  data.frame(
    row = rownames(cormat)[row(cormat)[ut]],
    column = rownames(cormat)[col(cormat)[ut]],
    cor  =(cormat)[ut],
    p = pmat[ut]
  )
}

cor_table<-flattenCorrMatrix(pearson$r, pearson$P)
cor_table<-cor_table[rev(order(cor_table$cor)),]
View(cor_table)  

data_max <- data[,c("Flavanoids","Nonflavanoid_phenols","Proline","Color_intensity")]
data_min <- data[,c("Alcalinity_of_ash","Magnesium","Proline","Color_intensity","Hue")]
pairs(data_max)
pairs(data_min)