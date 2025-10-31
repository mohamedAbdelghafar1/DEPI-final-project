# E-commerce Recommendation System — ETL Phase

## Overview
This README covers the **ETL phase** completed for the team project.  
The pipeline takes raw product data, cleans it, and loads it into **Azure SQL** for AI and web use.

**Flow:**
Raw Data → Azure Data Lake → Data Cleaning → Azure SQL → AI / Web


---

## What Was Done
1. **Data Ingestion**
   - Uploaded `raw-data.csv` to Azure Data Lake (`raw-data` container).
   - Script: `src/data_ingestion.py`

2. **Data Cleaning**
   - Kept only relevant columns for AI and SQL.
   - Renamed columns to match the SQL table.
   - Removed duplicates.
   - Filled numeric missing values with 0.
   - `description` field may contain missing values — this is fine.
   - Saved cleaned data as `dataset/cleaned_data.csv`.
   - Script: `src/data_cleaning.py`

3. **Data Warehousing**
   - Loaded cleaned data into Azure SQL `Products` table using `pyodbc`.
   - Script: `src/data_warehousing.py`

---

## How to Run (for teammates)
1. **Install dependencies**:
pip install pandas, pyodbc, azure-storage-blob

2. **Upload raw data** (optional if CSV already in Data Lake):
python src/data_ingestion.py

3. **Clean Data**:
python src/data_cleaning.py

4. **Load into Azure SQL**:
python src/data_warehousing.py

**⚠️ Teammates will need access to Azure resources**:
1. Storage account connection string (Data Lake)
2. SQL server credentials and firewall access (add your IP in Azure SQL if needed)

---

## Next Steps for Team

1. **AI team**: train recommendation models using Products table.

2. **Web team**: query Products and Recommendations tables for product display.

3. Optionally automate ETL using Airflow or Azure Data Factory for future updates.