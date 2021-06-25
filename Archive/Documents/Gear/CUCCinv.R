inv <- read.csv("~/Mahaigaina/CUCCinventory/CUCC_gearInventory_2012.csv", na.strings = "")
inv$year <- as.integer(as.character(inv$year))
inv$count <- as.integer(as.character(inv$count)) #caution!
inv$length <- as.integer(as.character(inv$length)) #caution!
inv$condition <- as.factor(inv$condition)
inv$comments <- as.character(inv$comments)
inv$welliesize <- ordered(inv$welliesize, levels = c("2","3","4","5","6","7","8","9","10","11","11.5","12"))
inv$suit_size <- ordered(inv$suit_size, levels = c("S","M","L","L+","XL","XL+","XXL", "?"))

par(mfrow=c(3,2))
#ropes and year
plot(inv[which(inv$item=="rope"), c("year","length")], main=paste("Rope (",sum(inv[which(inv$item=="rope"), "length"]),"m). ", Sys.Date(), sep=""))
abline(h=c(20,40,60,80,100), col="grey")
#slings
slings <- inv[which(inv$item=="slings"), c("year","count")]
slings <- data.frame(year=slings[,1], count=slings[,2])
slings <- aggregate(slings[2], slings[1], sum)
plot(slings, main=paste("Slings (",sum(inv[which(inv$item=="slings"), "count"]),"). ", Sys.Date(), sep=""), type="h")
abline(h=c(2,4,6,8,10), col="grey")
#wellies
plot(inv[which(inv$item=="wellies_pairs"), c("welliesize","count")], main=paste("Pairs of wellies.", Sys.Date()))
#suits and oversuits
suits <- inv[which(inv$item=="oversuit" | inv$item=="undersuit"), c("suit_size","item")]
suits$item <- as.factor(as.character(suits$item))
suitt <- table(suits)
barplot(t(suitt), beside=TRUE, xlab="Size. Black, oversuits. Grey, undersuits", ylab="Number of suits", col=c("black","grey"), main=paste("Oversuits (",sum(suitt[,1]),") and undersuits (", sum(suitt[,2]), "). ", Sys.Date(), sep=""))
#helmets and lights
head <- inv[which(inv$item=="backup_light" | inv$item=="helmet"| inv$item=="light"), c("count","item")]
head$item <- as.factor(as.character(head$item))
headt <- table(head)
barplot(t(headt), beside=TRUE, xlab="Number", col=c("black","grey", "white"), main=paste("Helmets, lights and backup lights.", Sys.Date()), horiz=TRUE, names=colnames(headt), las=1, xlim=c(0,10))
#harness & SRT kits
srt <- inv[which(inv$item=="srt_kit" | inv$item=="harness"| inv$item=="foot_loops"), c("count","item")]
srt <- aggregate(srt[1], srt[2], sum)
rownames(srt) <- srt$item
srt$item <- NULL
srtt <- as.table(t(srt))
barplot(t(srtt), beside=TRUE, xlab="Number", col=c("black","grey", "white"), main=paste("SRT kits, harnesses and footloops.", Sys.Date()), horiz=TRUE, names=colnames(srtt), las=1, xlim=c(0,10))
#statistics for all
all <- aggregate(inv$count, inv[1], sum)
rownames(all) <- all$item
all$item <- NULL
names(all) <- "count"

all




