####################################Kaggle competition###############################################

train <- read.csv("/Users/yuesongli/pitt/data analytics/lab4/train.csv")
test <- read.csv("/Users/yuesongli/pitt/data analytics/lab4/test.csv")
#add another column to the test tbale
test$Survived <- 0
#combine test table and train table
combi <- rbind(train, test)
#find out which embark doesn't have value
which(combi$Embarked == '')
#set the " " value of embrak to "S"
combi$Embarked[c(62,830)] = "S"
#convert the type of embark and name, so that we can deal with these factor. 
combi$Embarked <- factor(combi$Embarked)
combi$Name <- as.character(combi$Name)
#deal with the name, and extract title from the name
combi$Title <- sapply(combi$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
combi$Title <- sub(' ', '', combi$Title)
#combine a few of the most unusual titles
combi$Title[combi$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
combi$Title[combi$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
combi$Title[combi$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
#convert the title into factor
combi$Title <- factor(combi$Title)
#calculate the family size
combi$FamilySize <- combi$SibSp + combi$Parch + 1
#grow a tree on the subset of the data with the age values available, and then replace those that are missing
Agefit <- rpart(Age ~ Pclass + Sex + Embarked + Title,
                data=combi[!is.na(combi$Age),], method="anova")
combi$Age[is.na(combi$Age)] <- predict(Agefit, combi[is.na(combi$Age),])
#find out which fare doesn't have value
which(is.na(combi$Fare))
#using median value to set the " " value
combi$Fare[1044] <- median(combi$Fare, na.rm=TRUE)
#find out the surname of passenger
combi$Surname <- sapply(combi$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][1]})
#using family size and surname to combine familyID
combi$FamilyID <- paste(as.character(combi$FamilySize), combi$Surname, sep="")
#set the family size less than 2 to be small
combi$FamilyID[combi$FamilySize <= 2] <- 'Small'
#divide the combi table into train table and test table
train <- combi[1:891,]
test <- combi[892:1309,]
#install library party
library(party)
#set the random seed
set.seed(400)
#using random forest function to predict
fit <- cforest(as.factor(Survived) ~ Pclass + Sex + Age  + Fare+ Title + FamilySize + FamilyID,
               data = train, controls=cforest_unbiased(ntree=2000, mtry=2))
Prediction <- predict(fit, test, OOB=TRUE, type = "response")
submit <- data.frame(PassengerId = test$PassengerId,Mark=test$Cabin, Survived = Prediction)
#tranfer the data into csv
write.csv(submit, file = "result.csv", row.names = FALSE)

