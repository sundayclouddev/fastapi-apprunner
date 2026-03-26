from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

DATA_URL = "https://my-public-bucket-sao321.s3.us-east-1.amazonaws.com/total_data.csv"

@app.get("/")
def root():
return {"message": "API is running"}

@app.get("/fetch_data")
def fetch_data(
year: int = Query(None),
country: str = Query(None),
market: str = Query(None)
):
try:
df = pd.read_csv(DATA_URL)

```
    if year is not None:
        df = df[df['year'] == year]
    if country is not None:
        df = df[df['country'] == country]
    if market is not None:
        df = df[df['mkt_name'] == market]

    if df.empty:
        return {"message": "No data found"}

    return df.fillna('').to_dict(orient='records')

except Exception as e:
    return {"error": str(e)}
```
