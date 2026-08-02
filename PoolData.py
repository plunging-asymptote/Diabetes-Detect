import pandas
import os

def main ():
    data = pandas.DataFrame()
    ALB_data = pandas.DataFrame()
    BMX_data = pandas.DataFrame()
    BPX_data = pandas.DataFrame()
    DEMO_data = pandas.DataFrame()
    DIQ_data = pandas.DataFrame()
    GHB_data = pandas.DataFrame()
    
    #Read all data in folders containing datasets for each year of the surveys.
    for x in os.listdir(path = "NHANES_data/Pooled/ALB"):
        ALB_dataSET = pandas.read_sas("NHANES_data/Pooled/ALB/" + x)
        ALB_data = pandas.concat([ALB_data, ALB_dataSET[["SEQN", "URXUMA"]]])
        
    for x in os.listdir(path = "NHANES_data/Pooled/BMX"):
        BMX_dataSET = pandas.read_sas("NHANES_data/Pooled/BMX/" + x)
        BMX_data = pandas.concat([BMX_data, BMX_dataSET[["SEQN", "BMXBMI"]]])
    
    for x in os.listdir(path = "NHANES_data/Pooled/BPX"):
        BPX_dataSET = pandas.read_sas("NHANES_data/Pooled/BPX/" + x)
        BPX_data = pandas.concat([BPX_data, BPX_dataSET[["SEQN", "BPXSY2", "BPXDI2"]]])
        
    for x in os.listdir(path = "NHANES_data/Pooled/DEMO"):
        DEMO_dataSET = pandas.read_sas("NHANES_data/Pooled/DEMO/" + x)
        DEMO_data = pandas.concat([DEMO_data, DEMO_dataSET[["SEQN", "RIAGENDR", "RIDAGEYR"]]])
            
    for x in os.listdir(path = "NHANES_data/Pooled/DIQ"):
        DIQ_dataSET = pandas.read_sas("NHANES_data/Pooled/DIQ/" + x)
        DIQ_data = pandas.concat([DIQ_data, DIQ_dataSET[["SEQN", "DIQ010"]]])
        
    for x in os.listdir(path = "NHANES_data/Pooled/GHB"):
        GHB_dataSET = pandas.read_sas("NHANES_data/Pooled/GHB/" + x)
        GHB_data = pandas.concat([GHB_data, GHB_dataSET[["SEQN", "LBXGH"]]])
    
    #Ensure that only participants featured in all of the datasets are used.
    ALB_data = ALB_data[ALB_data["SEQN"].isin(GHB_data["SEQN"]) == True]
    BMX_data = BMX_data[BMX_data["SEQN"].isin(GHB_data["SEQN"]) == True]
    BPX_data = BPX_data[BPX_data["SEQN"].isin(GHB_data["SEQN"]) == True]
    DEMO_data = DEMO_data[DEMO_data["SEQN"].isin(GHB_data["SEQN"]) == True]
    DIQ_data = DIQ_data[DIQ_data["SEQN"].isin(GHB_data["SEQN"]) == True]
    
    ALB_data = ALB_data.sort_values(by = ["SEQN"])
    BMX_data = BMX_data.sort_values(by = ["SEQN"])
    BPX_data = BPX_data.sort_values(by = ["SEQN"])
    DEMO_data = DEMO_data.sort_values(by = ["SEQN"])
    DIQ_data = DIQ_data.sort_values(by = ["SEQN"])
    GHB_data = GHB_data.sort_values(by = ["SEQN"])
    
    #Reset index of all dataframes, ensuring that concating will work.
    ALB_data = ALB_data.reset_index(drop = True)
    BMX_data = BMX_data.reset_index(drop = True)
    BPX_data = BPX_data.reset_index(drop = True)
    DEMO_data = DEMO_data.reset_index(drop = True)
    DIQ_data = DIQ_data.reset_index(drop = True)
    GHB_data = GHB_data.reset_index(drop = True)
    
    #Concat datasets.
    data = pandas.concat([GHB_data, ALB_data["URXUMA"]], axis = 1)
    data = pandas.concat([data, BMX_data["BMXBMI"]], axis = 1)
    data = pandas.concat([data, BPX_data[["BPXSY2", "BPXDI2"]]], axis = 1)
    data = pandas.concat([data, DEMO_data[["RIAGENDR", "RIDAGEYR"]]], axis = 1)
    data = pandas.concat([data, DIQ_data["DIQ010"]], axis = 1)
    
    data.to_csv("data.csv", index = False)

main()
