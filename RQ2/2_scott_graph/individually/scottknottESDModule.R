library(reshape2)
library(ScottKnottESD)
library(ggplot2)

# —————————————————————————— input —————————————————————————— #
# 设置Y轴标题
ytitle <- "AV's Recall"

# 设置文件路径
file_path <- "./Recall.csv"  # 替换为您的文件路径

# 设置输出路径
output_path <- "./Recall.pdf"
# —————————————————————————— input end —————————————————————————— #

# 读取 CSV 文件
result <- read.csv(file_path)



sk <- sk_esd(result, version="np")  #rank存放在sk$groups中


#ggplot画图需要把各方法的性能值以行的形式放在一起
PC = data.frame(value=result$PC,technique="PC")
# PC_ = data.frame(value=result$PC.,technique="PC+")
PI = data.frame(value=result$PI,technique="PI")
# PI_ = data.frame(value=result$PI.,technique="PI+")
PM = data.frame(value=result$PM,technique="PM")
# PM_ = data.frame(value=result$PM.,technique="PM+")

Simple = data.frame(value=result$Simple,technique="Simple")

SZZ_B = data.frame(value=result$SZZ_B,technique="SZZ_B")
SZZ_B_ = data.frame(value=result$SZZ_B.,technique="SZZ_B+")
SZZ_RA = data.frame(value=result$SZZ_RA,technique="SZZ_RA")
SZZ_RA_ = data.frame(value=result$SZZ_RA.,technique="SZZ_RA+")
SZZ_U = data.frame(value=result$SZZ_U,technique="SZZ_U")
SZZ_U_ = data.frame(value=result$SZZ_U.,technique="SZZ_U+")


# all = rbind(PC, PC_, PI,PI_,PM,PM_,Simple,SZZ_B,SZZ_B_,SZZ_RA,SZZ_RA_,SZZ_U,SZZ_U_)
all = rbind(PC,PI,PM,Simple,SZZ_B,SZZ_B_,SZZ_RA,SZZ_RA_,SZZ_U,SZZ_U_)
# all = rbind(PC,PI,PM,Simple,SZZ_B,,SZZ_RA,,SZZ_U,)
#给all中的各方法添加sk esd test下的rank信息
all$rank = 0
all[all$technique=="PC", ]$rank = sk$groups[["PC"]]
# all[all$technique=="PC+", ]$rank = sk$groups[["PC."]]
all[all$technique=="PI", ]$rank = sk$groups[["PI"]]
# all[all$technique=="PI+", ]$rank = sk$groups[["PI."]]
all[all$technique=="PM", ]$rank = sk$groups[["PM"]]
# all[all$technique=="PM+", ]$rank = sk$groups[["PM."]]
all[all$technique=="Simple", ]$rank = sk$groups[["Simple"]]

# AVf1
all[all$technique=="SZZ_B", ]$rank = sk$groups[["SZZ_B"]]
all[all$technique=="SZZ_B+", ]$rank = sk$groups[["SZZ_B."]]
all[all$technique=="SZZ_RA", ]$rank = sk$groups[["SZZ_RA"]]
all[all$technique=="SZZ_RA+", ]$rank = sk$groups[["SZZ_RA."]]

all[all$technique=="SZZ_U", ]$rank = sk$groups[["SZZ_U"]]
all[all$technique=="SZZ_U+", ]$rank = sk$groups[["SZZ_U."]]

# 画图
ggplot(all, aes(x=reorder(technique, -value, FUN=median), y=value)) + geom_boxplot() + facet_grid(~rank, drop=TRUE, scales = "free", space = "free") + ylab(ytitle) + xlab("") + theme(axis.text.x=element_text(angle = -60, hjust = 0))

# 存在给定目录下的pdf文件中
ggsave(paste0("./", output_path),width=5,height=2.5)
