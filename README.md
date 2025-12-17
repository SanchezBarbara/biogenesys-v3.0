# 🔵 **𝗕𝗶𝗼𝗴𝗲𝗻𝗲𝘀𝘆𝘀 𝗖𝗹𝗼𝘂𝗱Ops 𝘃𝟯.𝟬: 𝗔𝗪𝗦 𝗜𝗻𝗳𝗿𝗮𝘀𝘁𝗿𝘂𝗰𝘁𝘂𝗿𝗲 & 𝗦𝘁𝗮𝗿 𝗦𝗰𝗵𝗲𝗺𝗮**

## **Project Overview**
**Biogenesys v3.0** represents the final leap in the data lifecycle: **Cloud Migration**. In this stage, the project transitions from local CSV processing to a robust **Data Warehouse** environment. We implemented a **Star Schema** architecture on **AWS RDS (PostgreSQL)**, enabling scalable analytics and professional database management.

## **🚀 Key Engineering Features**
* **Cloud Database Implementation:** Deployment of a relational database on **Amazon Web Services (RDS)** using PostgreSQL.
* **Star Schema Architecture:** Transformation of a flat dataset into a structured model with a central **Fact table** and multiple **Dimension tables** for optimized query performance.
* **Automated Cloud Ingestion:** A specialized Python loader that orchestrates the data flow from local outputs to the cloud, utilizing `SQLAlchemy` and `Psycopg2`.
* **Security & Decoupling:** Implementation of a **Modular Configuration Pattern**. Sensitive connection strings (Host, User, Password) are decoupled into a separate `credentials_bio.py` script to prevent exposure and ensure infrastructure integrity.

## **📂 Project Structure**
```text
├── biogenesys_v3.0/
│   ├── sql/
│   │   └── create_star_schema.sql    # DDL for Fact and Dimension tables
│   ├── scripts/
│   │   ├── cloud_loader.py           # The Ingestion Engine
│   │   └── credentials_template.py   # Secure blueprint for DB access
│   └── README.md                     # Technical documentation
```

## 🛠️ Tech Stack
Cloud Provider: Amazon Web Services (AWS RDS)

Database Engine: PostgreSQL

Language: Python 3.x

Tools: DBeaver (SQL Client), Pandas, SQLAlchemy



## ⚙️ How to Run & Deploy

* Prepare AWS RDS: Set up a PostgreSQL instance and ensure your IP is whitelisted in the Security Groups.

* Setup Credentials: Rename credentials_template.py to credentials_bio.py and fill in your AWS Host, User, and Password.

* Deploy Schema: Use DBeaver to execute the scripts located in `/sql/create_star_schema.sql`.


Execute Ingestion in `biogenesys_v3.0/scripts/` :

```text
 Bash
 python cloud_loader.py
```

## 🛡️ Security Note
The file `credentials_bio.py` is excluded from this repository for security reasons. A `credentials_template.py` is provided as a reference. This approach simulates a real-world enterprise environment where sensitive access keys are never hardcoded into the main source code.

## 📈 Impact
This version transforms the project into a Production-Ready solution. By moving to a Star Schema in the cloud, the data is now structured for high-performance BI reporting. This architecture allows for seamless integration with tools like Power BI, providing faster refresh rates and a single source of truth for decision-making.
