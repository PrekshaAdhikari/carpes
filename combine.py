import pandas as pd
df1 = pd.read_csv('capres.csv')
df2 = pd.read_csv('new_capres.csv')
df = df1.merge(df2, on='origurl')
df.to_csv('carpes_Output.csv')