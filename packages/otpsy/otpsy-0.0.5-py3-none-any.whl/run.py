import otpsy as ot
import pandas as pd

df = pd.read_csv("C:\Users\alexl\Documents\ETUDE\2024\M2Thesis\experience\data\df_global_pilote.csv", sep = ";")

a = ot.Sample(df, 
              columns_to_test=["PSE"],
              participant_column="index_participant")
a.visualise()
outliers = a.methodMAD(distance=2, threshold_included=True)
print(outliers)