import pandas
import os

DATA = pandas.DataFrame()
ALB_DATA = pandas.DataFrame()
BMX_DATA = pandas.DataFrame()
BPX_DATA = pandas.DataFrame()
DEMO_DATA = pandas.DataFrame()
DIQ_DATA = pandas.DataFrame()
GHB_DATA = pandas.DataFrame()

#Read all data in folders containing datasets for each year of the surveys.
for x in os.listdir(path = "NHANES_DATA/Pooled/ALB"):
    ALB_DATASET = pandas.read_sas("NHANES_DATA/Pooled/ALB/" + x)
    ALB_DATA = pandas.concat([ALB_DATA, ALB_DATASET[["SEQN", "URXUMA"]]])
    
for x in os.listdir(path = "NHANES_DATA/Pooled/BMX"):
    BMX_DATASET = pandas.read_sas("NHANES_DATA/Pooled/BMX/" + x)
    BMX_DATA = pandas.concat([BMX_DATA, BMX_DATASET[["SEQN", "BMXBMI"]]])

for x in os.listdir(path = "NHANES_DATA/Pooled/BPX"):
    BPX_DATASET = pandas.read_sas("NHANES_DATA/Pooled/BPX/" + x)
    BPX_DATA = pandas.concat([BPX_DATA, BPX_DATASET[["SEQN", "BPXSY2", "BPXDI2"]]])
    
for x in os.listdir(path = "NHANES_DATA/Pooled/DEMO"):
    DEMO_DATASET = pandas.read_sas("NHANES_DATA/Pooled/DEMO/" + x)
    DEMO_DATA = pandas.concat([DEMO_DATA, DEMO_DATASET[["SEQN", "RIAGENDR", "RIDAGEYR"]]])
        
for x in os.listdir(path = "NHANES_DATA/Pooled/DIQ"):
    DIQ_DATASET = pandas.read_sas("NHANES_DATA/Pooled/DIQ/" + x)
    DIQ_DATA = pandas.concat([DIQ_DATA, DIQ_DATASET[["SEQN", "DIQ010"]]])
    
for x in os.listdir(path = "NHANES_DATA/Pooled/GHB"):
    GHB_DATASET = pandas.read_sas("NHANES_DATA/Pooled/GHB/" + x)
    GHB_DATA = pandas.concat([GHB_DATA, GHB_DATASET[["SEQN", "LBXGH"]]])

#Ensure that only participants featured in all of the datasets are used.
ALB_DATA = ALB_DATA[ALB_DATA["SEQN"].isin(GHB_DATA["SEQN"]) == True]
BMX_DATA = BMX_DATA[BMX_DATA["SEQN"].isin(GHB_DATA["SEQN"]) == True]
BPX_DATA = BPX_DATA[BPX_DATA["SEQN"].isin(GHB_DATA["SEQN"]) == True]
DEMO_DATA = DEMO_DATA[DEMO_DATA["SEQN"].isin(GHB_DATA["SEQN"]) == True]
DIQ_DATA = DIQ_DATA[DIQ_DATA["SEQN"].isin(GHB_DATA["SEQN"]) == True]

ALB_DATA = ALB_DATA.sort_values(by = ["SEQN"])
BMX_DATA = BMX_DATA.sort_values(by = ["SEQN"])
BPX_DATA = BPX_DATA.sort_values(by = ["SEQN"])
DEMO_DATA = DEMO_DATA.sort_values(by = ["SEQN"])
DIQ_DATA = DIQ_DATA.sort_values(by = ["SEQN"])
GHB_DATA = GHB_DATA.sort_values(by = ["SEQN"])

#Reset index of all dataframes, ensuring that concating will work.
ALB_DATA = ALB_DATA.reset_index(drop = True)
BMX_DATA = BMX_DATA.reset_index(drop = True)
BPX_DATA = BPX_DATA.reset_index(drop = True)
DEMO_DATA = DEMO_DATA.reset_index(drop = True)
DIQ_DATA = DIQ_DATA.reset_index(drop = True)
GHB_DATA = GHB_DATA.reset_index(drop = True)

#Concat datasets.
DATA = pandas.concat([GHB_DATA, ALB_DATA["URXUMA"]], axis = 1)
DATA = pandas.concat([DATA, BMX_DATA["BMXBMI"]], axis = 1)
DATA = pandas.concat([DATA, BPX_DATA[["BPXSY2", "BPXDI2"]]], axis = 1)
DATA = pandas.concat([DATA, DEMO_DATA[["RIAGENDR", "RIDAGEYR"]]], axis = 1)
DATA = pandas.concat([DATA, DIQ_DATA["DIQ010"]], axis = 1)

DATA.to_csv("DATA.csv", index = False)