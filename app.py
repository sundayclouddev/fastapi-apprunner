from fastapi import FastAPI, Query, HTTPException
import pandas as pd

app = FastAPI()

# CSV data source
DATA_URL = "https://my-public-bucket-sao321.s3.us-east-1.amazonaws.com/total_data.csv"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/fetch_data")
def fetch_data(
    year: int = Query(None, description="Filter by year"),
    country: str = Query(None, description="Filter by country"),
    market: str = Query(None, description="Filter by market name")
):
    try:
        # Load CSV
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
            raise HTTPException(status_code=404, detail="No data found for given filters")

        # Return JSON
        return df.fillna('').to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
