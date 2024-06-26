#!/usr/local/bin/python3.9 
import pandas as pd
  
data = {"id": [1, 2, 3],
        "name": ["karthik", "nikhil", "bhagi"]}
  
df = pd.DataFrame(data)
print(df)