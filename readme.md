# E-Commerce Recommender System 🚀🛍️
A cloud-ready, end-to-end data engineering pipeline and recommender-system blueprint for modern e-commerce platforms. The project demonstrates how data ingestion, cleaning, transformation, storage, and ML preparation fit together into a scalable workflow.

---

## 🔍 Project Overview
This project builds a complete data engineering pipeline that powers product recommendation systems. It processes raw user–product interactions, cleans and models the data in a star schema, and prepares the matrices required for recommendation algorithms such as collaborative filtering and content-based models.

Project Objectives:
- Build an ETL pipeline suitable for large-scale e-commerce data
- Store cleaned data in Azure SQL Data Warehouse
- Engineer features for recommendation models
- Visualize KPIs and insights using Apache Superset

---

## ⭐ Features
- Automated ETL using Python + Azure Data Factory
- Azure Data Lake (Raw → Processed zones)
- PySpark + Pandas data transformations
- Star schema with fact & dimension tables
- Feature engineering for user and product behavior
- User-item matrix preparation for ML models
- Dashboards generated using Superset

---

## 🧭 Architecture
1. Data Sources – Kaggle + synthetic generator
2. Ingestion – Python ETL / Azure Data Factory → Data Lake (raw zone)
3. Processing – Cleaning, normalization, feature engineering
4. Storage – Azure SQL Data Warehouse (Synapse)
5. Visualization – Apache Superset dashboards
6. Model Prep – Interaction matrix for collaborative filtering

---

## 🛠️ Tech Stack
- Python (Pandas, NumPy, Scikit-learn)
- PySpark for distributed transformations
- Azure Data Lake Storage
- Azure Synapse Analytics
- Azure Data Factory orchestration
- Apache Superset dashboards
- Matplotlib / Seaborn for EDA

---

## 📁 Repository Structure
    .
    ├── etl/                 # Ingest, transform, load scripts
    ├── data/                # Sample data + synthetic datasets
    ├── sql/                 # Schema creation and SQL scripts
    ├── notebooks/           # EDA + model prep notebooks
    ├── superset/            # Dashboard exports
    ├── docs/                # Full project report (PDF)
    └── README.md

---

## 🚀 Quick Start (Local Mode)

### 1. Clone the repo
    git clone <repo-url>
    cd ecomm-recommender

### 2. Create a virtual environment
    python -m venv .venv
    source .venv/bin/activate       # macOS / Linux
    .venv\Scripts\activate          # Windows

### 3. Install dependencies
    pip install -r requirements.txt

### 4. Run ETL steps
    python etl/ingest_kaggle.py --input data/kaggle_sample.csv --out data/raw/
    python etl/transform.py --in data/raw/ --out data/processed/

### 5. Create a development database
    python sql/load_to_sqlite.py --in data/processed/ --db dev.db

### 6. Open EDA notebook
    notebooks/EDA.ipynb

---

## 🧪 Model Preparation
- Generate user-item interaction matrices in notebooks/model_prep.ipynb
- Includes baseline collaborative filtering examples
- Metrics used: RMSE, Precision@K, Recall@K

---

## ⚠️ Limitations
- Pipeline currently operates in batch mode
- Some data is synthetic for demonstration purposes
- Production model serving not included

---

## 🔮 Future Enhancements
- Real-time streaming (Kafka / Event Hubs)
- Deep-learning hybrid recommendation models
- Automated model retraining
- A/B testing framework

---

## 👥 Team
Team 165:
- Mohamed Ahmed Abdelkader
- Badr Islam
- Malek Anas
- Alaa Mahmoud
- Mazen Maysara Shawqi
- Yousef Mohamed Elsayed

Supervisor: Eng. Mohamed Hamed

---

## 📄 License
This project is licensed under the MIT License.

---

## 🙌 Final Note
This project offers a scalable foundation for any e-commerce platform wanting smarter, data-driven product recommendations. Extend it, stress-test it, or plug in your own ML models — the pipeline is ready.
