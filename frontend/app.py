import pandas as pd
import requests
import streamlit as st

st.title("Customer Purchases Dashboard")

# Crear dos pestañas: Upload y Analyse
tabs = st.tabs(["Upload", "Analyse"])
upload_tab, analyse_tab = tabs

with upload_tab:
    st.header("Upload Data")

    # --- Bulk Upload (CSV) ---
    st.subheader("Bulk Upload (CSV)")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], key="bulk_upload")
    if uploaded_file is not None:
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
            response = requests.post("http://backend:8000/purchase/bulk/", files=files)
            if response.status_code == 200:
                st.success("Bulk data uploaded successfully")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error uploading CSV: {str(e)}")

    # --- Single Purchase Form ---
    st.subheader("Add Single Purchase")
    with st.form("single_purchase_form"):
        customer_name = st.text_input("Customer Name")
        country = st.text_input("Country")
        purchase_date = st.date_input("Purchase Date")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Submit Purchase")
        if submitted:
            payload = {
                "customer_name": customer_name,
                "country": country,
                "purchase_date": purchase_date.isoformat(),
                "amount": amount,
            }
            try:
                response = requests.post("http://backend:8000/purchase/", json=payload)
                if response.status_code == 200:
                    st.success("Purchase added successfully")
                else:
                    st.error(
                        f"Error adding purchase: {response.json().get('detail', 'Unknown error')}"
                    )
            except Exception as e:
                st.error(f"Request failed: {str(e)}")

with analyse_tab:
    st.header("Analyse Data")

    # --- Filter Purchases ---
    st.subheader("Filter Purchases")
    filter_country = st.text_input("Filter by Country", key="filter_country")
    start_date = st.date_input("Start Date", key="start_date")
    end_date = st.date_input("End Date", key="end_date")

    if st.button("Get Purchases", key="get_purchases"):
        params = {
            "country": filter_country,
            "start_date": start_date,
            "end_date": end_date,
        }
        try:
            response = requests.get("http://backend:8000/purchases/", params=params)
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error("Error fetching purchases")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

    # --- KPIs ---
    st.subheader("KPIs")
    if st.button("Get KPIs", key="get_kpis"):
        try:
            response = requests.get("http://backend:8000/purchases/kpis/")
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error("Error fetching KPIs")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

    # --- Predict Future Purchases ---
    # st.subheader("Predict Future Purchases")
    # days = st.number_input(
    #     "Days to Predict", min_value=1, value=10, step=1, key="predict_days"
    # )
    # if st.button("Predict", key="predict"):
    #     try:
    #         response = requests.get(
    #             "http://backend:8000/predict/", params={"days": days}
    #         )
    #         if response.status_code == 200:
    #             predictions = response.json()
    #             st.write("Predictions:", predictions)
    #             # Graficar la predicción
    #             df_pred = pd.DataFrame(predictions)
    #             df_pred["ds"] = pd.to_datetime(df_pred["ds"])
    #             df_pred = df_pred.set_index("ds")
    #             st.line_chart(df_pred["yhat"])
    #         else:
    #             st.error("Error fetching predictions")
    #     except Exception as e:
    #         st.error(f"Request failed: {str(e)}")
