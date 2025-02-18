# 🛍️ Customer Purchases Dashboard

## 📌 Overview

This project consists of two main components:

### 🖥️ **Backend (FastAPI)**

- Manages customer purchase data in-memory.
- Provides the following endpoints:
  - Add a single purchase (`POST /purchase/`).
  - Bulk upload purchases from a CSV file (`POST /purchase/bulk/`).
  - Retrieve purchases filtered by date and country (`GET /purchases/`).
  - Compute KPIs such as:
    - Average purchase per customer.
    - Number of customers per country.
    - (Optional) Sales forecasting.

| Método | Endpoint           | Descripción                      |
| ------ | ------------------ | -------------------------------- |
| `POST` | `/purchase/`       | Add a single purchase            |
| `POST` | `/purchase/bulk/`  | Upload purchases from a CSV file |
| `GET`  | `/purchases/`      | Retrieve all purchases           |
| `GET`  | `/purchases/kpis/` | Get purchase KPIs                |

### 🎨 **Frontend (Streamlit)**

- Provides an interactive UI for users.
- Features:
  - **Upload Section**: Allows users to manually input a single purchase or upload a CSV file.
  - **Analysis Section**: Enables filtering by date and country and displays key KPIs retrieved from the backend.

### 🐳 **Dockerization**

- Both the FastAPI backend and Streamlit frontend are containerized.
- A `docker-compose.yml` file orchestrates both services.

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/ChengjiePL/software-developer-test-1
cd software-developer-test-1
```

### 2️⃣ **Run with Docker**

```bash
docker-compose up --build
```

This will start both the backend (FastAPI) and frontend (Streamlit) services. `http://localhost:8501/`

## 🧪 Testing

To run unit tests for the backend, navigate to the `backend/tests` folder and execute:

```bash
python3 -m pytest test_main.py
```

## 📦 Project Structure

```
/
│── backend/      # FastAPI backend
│   ├── fastapi
│   │   ├── main.py   # Main API logic
│   ├── tests
│   │   ├── test_main.py # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
│
│
│── frontend/     # Streamlit frontend
│   ├── app.py    # Streamlit application
│   ├── Dockerfile
│   └── requirements.txt
│
│── docker-compose.yml  # Orchestrates backend & frontend
│── sample_purchase.csv # Sample CSV for testing
│── README.md           # Documentation
```
