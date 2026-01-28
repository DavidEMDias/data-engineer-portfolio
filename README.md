# 🌦️ Weather Data Engineering Pipeline

**Role:** Data Engineer. <br>
**Tools Used:** Airflow, Docker, PostgreSQL, SQL-based transformation (dbt), Python scripts and DAGs, Apache Superset.

An end-to-end **ELT (Extract, Load, Transform)** data pipeline that ingests live weather data, loads it into PostgreSQL, transforms and enriches it using dbt, and produces analytical visualizations — fully automated and containerized.

---

## 📌 Problem

Weather data is commonly exposed through external APIs in raw and semi-structured formats. While this data is valuable, it is not immediately suitable for analytics, reporting, or decision-making.

Key challenges addressed by this project include:
- Reliable ingestion of live weather data
- Storing raw data for traceability and reprocessing
- Transforming and enriching data for analytical use cases
- Automating pipeline execution
- Making insights accessible through visualizations

---

## 🎯 Objectives

The main objectives of this project are to:

- Ingest live weather data from a public API
- Load raw weather data directly into PostgreSQL
- Transform and enrich data using dbt
- Orchestrate and automate the ELT pipeline
- Create visualizations for data exploration and insight generation
- Provide a reproducible, containerized setup

---

## 🛠️ Solution Approach

This project implements a modern **ELT (Extract, Load, Transform)** architecture using industry-standard data engineering tools.

### Architecture Overview

<img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/35bd92d4-1223-4738-89ce-fae9a98000af" />

### Pipeline Components

1. **Extract**
   - Live weather data is pulled from an external Weather API using Python.
   - Data is ingested in its raw form without upfront transformations.

2. **Load**
   - Raw weather data is first loaded into a PostgreSQL database.
   - This preserves source data for auditing, backfills, and reprocessing.
   - **Idempotency is guaranteed** via a unique constraint on `(city, time)` and `INSERT ... ON CONFLICT DO NOTHING`, ensuring reruns do not create duplicate entries.

3. **Transform (dbt)**
   - dbt is used to transform raw data directly inside PostgreSQL.
   - Transformations include:
     - Data cleaning and normalization
     - Unit conversions (e.g., temperature, wind speed)
     - Timestamp standardization
     - Creation of analytics-ready models

4. **Orchestration & Automation**
   - Apache Airflow orchestrates the entire ELT workflow.
   - dbt runs are triggered as downstream tasks after data loading.

5. **Reporting & Visualization**
   - Transformed dbt models are used to power dashboards and charts.
   - Enables trend analysis and data-driven insights, in our case leveraging Apache Superset.

6. **Containerization**
   - Docker is used to containerize all components of the pipeline.
   - Ensures consistent environments across development and deployment.

---

## 📊 Key Results

- ✅ Fully automated ELT weather data pipeline  
- ✅ Raw data preserved in PostgreSQL for traceability  
- ✅ Scalable, SQL-based transformations powered by dbt  
- ✅ Orchestrated and monitored using Apache Airflow  
- ✅ Analytics-ready datasets and meaningful visualizations using Apache Superset  
- ✅ Reproducible and portable deployment using Docker

<br>
### Figures

#### Figure 1: Main Workflow Orchestration
![Main Workflow Orchestration](https://github.com/user-attachments/assets/643e1cd8-7790-478e-88a6-853a5d230f96)

#### Figure 2: Airflow DAG in Execution
![Airflow DAG in Execution](https://github.com/user-attachments/assets/59a55830-1580-4a58-b29f-a851d3ef182d)

#### Figure 3: Airflow DAG Idempotency in Execution
![Airflow DAG Idempotency](https://github.com/user-attachments/assets/e2b77edb-8968-4bed-8c65-63f03a7f50c2)

#### Figure 4: Superset Visualizations
![Superset Visualizations](https://github.com/user-attachments/assets/cc23aecb-413c-4bdb-8263-d94a0aa50db7)

---

This repository demonstrates a **production-style ELT pipeline** for real-time weather analytics, leveraging PostgreSQL and dbt for scalable and maintainable data transformations.
