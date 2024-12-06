import polars as pl
from sqlalchemy import create_engine
import time
rows = [(f'Name {i}', f'email{i}@example.com') for i in range(50001)]
df=pl.DataFrame(rows,orient='row',schema=['name','email'])
print(df)

# Convertir le DataFrame Polars en DataFrame Pandas
pandas_df = df.to_pandas()

start = time.time()

# Configurer la connexion à SQL Server avec SQLAlchemy
connection_string = 'mssql+pymssql://user_bouchara_int:Resolved-Attendant4-Unsteady@130.180.215.217:5433/BOUCHARA_INT'
engine = create_engine(connection_string)

# Insérer les données dans SQL Server
pandas_df.to_sql('your_table', con=engine, if_exists='append', index=False)

# Fermer la connexion
engine.dispose()
print(time.time()-start)