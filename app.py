from fastapi import FastAPI, Query, HTTPException
import pandas as pd

app = FastAPI()

DATA_URL = "https://my-public-bucket-sao321.s3.us-east-1.amazonaws.com/total_data.csv"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/fetch_data")
def fetch_data(year: int = None, country: str = None, market: str = None):
    try:
        df = pd.read_csv(DATA_URL)

        if year:
            df = df[df['year'] == year]
        if country:
            df = df[df['country'] == country]
        if market:
            df = df[df['mkt_name'] == market]

        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")

        return df.fillna('').to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
