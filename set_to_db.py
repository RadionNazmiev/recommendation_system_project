import pandas as pd



df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

df.to_sql("test", "sqlite:///test.db")