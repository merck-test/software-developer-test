import csv
import io
from collections import defaultdict
from datetime import date
from typing import List, Optional

import pandas as pd
from prophet import Prophet
from pydantic import BaseModel

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="Customer Purchases API")

# In-memory storage
purchases = []


class Purchase(BaseModel):
    customer_name: str
    country: str
    purchase_date: date
    amount: float


@app.post("/purchase/", response_model=Purchase)
async def add_purchase(purchase: Purchase):
    purchases.append(purchase)
    return purchase


@app.post("/purchase/bulk/")
async def add_bulk_purchases(file: UploadFile = File(...)):
    if file.content_type not in ["text/csv"]:
        raise HTTPException(status_code=400, detail="Invalid file format")

    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    expected_headers = {"customer_name", "country", "purchase_date", "amount"}
    new_purchases = []

    for row in reader:
        try:
            purchase = Purchase(
                customer_name=row["customer_name"],
                country=row["country"],
                purchase_date=date.fromisoformat(row["purchase_date"]),
                amount=float(row["amount"]),
            )
            purchases.append(purchase)
            new_purchases.append(purchase)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error processing row: {row} - {e}"
            )
    return JSONResponse(content={"added": len(new_purchases)})


@app.get("/purchases/", response_model=List[Purchase])
def get_purchases(
    country: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    filtered = purchases
    if country:
        filtered = [p for p in filtered if p.country.lower() == country.lower()]
    if start_date:
        filtered = [p for p in filtered if p.purchase_date >= start_date]
    if end_date:
        filtered = [p for p in filtered if p.purchase_date <= end_date]
    return filtered


@app.get("/purchases/kpis/")
def get_kpis(days: int = Query(16, ge=1, description="Days to predict sales for")):
    if not purchases:
        return {"error": "No purchases available"}

    # KPIs calculation
    total_amount = sum(p.amount for p in purchases)
    customers = {p.customer_name for p in purchases}
    avg_purchase_per_client = total_amount / len(customers) if customers else 0

    clients_per_country = defaultdict(set)
    for p in purchases:
        clients_per_country[p.country].add(p.customer_name)

    clients_count_by_country = {k: len(v) for k, v in clients_per_country.items()}

    # Forecast sales integration
    df = pd.DataFrame([p.dict() for p in purchases])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df_agg = df.groupby("purchase_date")["amount"].sum().reset_index()
    df_agg.columns = ["ds", "y"]

    model = Prophet()
    model.fit(df_agg)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    last_date = df_agg["ds"].max()
    forecast_future = forecast[forecast["ds"] > last_date][
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ]

    return {
        "average_purchase_per_client": avg_purchase_per_client,
        "clients_per_country": clients_count_by_country,
        "forecast_sales": forecast_future.to_dict(orient="records"),
    }
