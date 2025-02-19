import pandas as pd
import requests
import streamlit as st

st.title("Customer Purchases Dashboard")

st.sidebar.header("Upload Data")

# File uploader for CSV files
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    try:
        # Prepare the file for the POST request
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}

        # Send the file to the backend endpoint for bulk purchases
        response = requests.post("http://backend:8000/purchase/bulk/", files=files)

        # Show success or error message based on the response
        if response.status_code == 200:
            st.sidebar.success("Data uploaded")
        else:
            st.sidebar.error(
                f"Error uploading file: {response.json().get('detail', 'Unknown error')}"
            )
    except Exception as e:
        st.sidebar.error(f"Failed to upload file: {str(e)}")

# User inputs for filtering purchases
st.sidebar.header("Filter Data")
country = st.sidebar.text_input("Filter by country")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")


# Button to fetch filtered purchases from the backend
if st.sidebar.button("Get Purchases"):
    params = {"country": country, "start_date": start_date, "end_date": end_date}
    response = requests.get("http://backend:8000/purchases/", params=params)
    st.write(response.json())

# Button to fetch KPIs from the backend
if st.sidebar.button("Get KPIs"):
    response = requests.get("http://backend:8000/purchases/kpis/")
    st.write(response.json())


# Sección para predecir compras futuras
st.sidebar.header("Predict Future Purchases")
days = st.sidebar.number_input("Days to predict", min_value=1, value=30, step=1)

if st.sidebar.button("Predict"):
    response = requests.get("http://backend:8000/predict/", params={"days": days})
    if response.status_code == 200:
        predictions = response.json()
        st.write("Predictions:", predictions)
        # Opcional: Graficar la predicción
        df_pred = pd.DataFrame(predictions)
        df_pred["ds"] = pd.to_datetime(df_pred["ds"])
        df_pred = df_pred.set_index("ds")
        st.line_chart(df_pred["yhat"])
    else:
        st.error("Error fetching predictions")
