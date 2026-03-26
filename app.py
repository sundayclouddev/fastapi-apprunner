from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

DATA_URL = "https://my-public-bucket-sao321.s3.us-east-1.amazonaws.com/total_data.csv"

def fetch_data(year: int = None, country: str = None, market: str = None):
    try:
        # Load CSV from S3
        df = pd.read_csv(DATA_URL)

        # Apply filters
        if year is not None:
            df = df[df['year'] == year]
        if country is not None:
            df = df[df['country'] == country]
        if market is not None:
            df = df[df['mkt_name'] == market]

        # Handle empty results
        if df.empty:
            return {"message": "No data found for given filters"}

        return df.fillna('').to_dict(orient='records')

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/fetch_data")
async def fetch_data_api(
    year: int = Query(None),
    country: str = Query(None),
    market: str = Query(None)
):
    return fetch_data(year, country, market)
