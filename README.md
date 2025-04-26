# 🗳️📰 U.S. Elections & Mental Health: Automated News Pipeline & Analytics

## Project Overview

This project builds and orchestrates a **fully automated, scalable data pipeline** to analyze the impact of U.S. political news—**before and during elections**—on mental well-being.  
Leveraging the latest in cloud data engineering and NLP, it extracts, processes, enriches, and visualizes news data for actionable insights.

---

## 💡 Why This Use Case?

Political news is not just about facts; it also carries emotional weight that can influence public mental health—especially around major events like elections.  
However, collecting, structuring, and analyzing large volumes of news content is a technical challenge.  
**This project solves it by combining Apache Airflow, NLP, Snowflake, BigQuery, DBT, and Tableau into a single automated workflow.**

---

## 🔁 Project Workflow

1. **Automated Data Ingestion**
   - **Apache Airflow** runs in Docker, orchestrating daily extraction of news articles (titles, descriptions, content) from external APIs.

2. **NLP Enrichment**
   - Applies advanced **Natural Language Processing**:
     - **Part-of-speech tagging**
     - **Emotion detection**
     - **Offensive language detection**
     - **Hate speech classification**

3. **Staging & Data Warehousing**
   - Stores processed data in **SQLite** as a staging layer.
   - Loads into **Snowflake** with a star schema:
     - **1 fact table:** Article core details
     - **4 dimension tables:** Metadata, NLP features, categorization, timestamps

4. **Analytics at Scale**
   - Data flows to **Google BigQuery** for high-performance analytics.
   - **DBT** transforms, aggregates, and optimizes data, applying business logic for clean, analysis-ready datasets.

5. **Grade Level & Readability Assessment**
   - Applies statistical tests to news titles to evaluate their complexity and readability grade level, comparing changes pre- and during elections.

6. **Visualization & Insight Generation**
   - Uses **Tableau** (with TabPy) for interactive dashboards.
   - Visualizes trends in sentiment, hate speech, complexity, and emotional tone—**comparing pre- and during-election periods.**

---

## 🔬 Key Findings & Features

- **Real-time sentiment & emotion mapping** of political news
- **Detection of offensive/hateful language trends** during critical periods
- **Readability analysis** to assess changes in news complexity
- **Fully automated, modular pipeline**—easy to scale or extend to new sources/analyses

---

## ⚙️ Technologies Used

- **Apache Airflow** (workflow orchestration, Dockerized)
- **Python & SQL** (data processing, NLP, DBT models)
- **Natural Language Processing (NLP)** with Hugging Face Transformers
- **Snowflake & Google BigQuery** (cloud data warehousing & analytics)
- **DBT** (Data Build Tool for transformations)
- **Tableau + TabPy** (data visualization)
- **SQLite** (staging)
- **Docker** (containerized automation)
- **Google Cloud Platform (GCP)**

---

## 📂 Repository Structure

```
/src          # Data extraction, NLP & ETL scripts
/models              # DBT models and transformations
/tableau          # Dashboards & TabPy scripts
/README.md        # Project documentation (this file)
```

---

## 🏆 Impact

This project enables **seamless, end-to-end analytics** on the relationship between political news and mental health—removing manual steps and technical bottlenecks.  
It provides a blueprint for building **modular, cloud-native data pipelines** ready for real-time or large-scale analysis in any domain.

---


**Skills:**  
Data Build Tool (DBT) · Python · SQL · Apache Airflow · Google BigQuery · GCP · SQLite · Docker · Data Science · NLP · Tableau · TabPy · Cloud Engineering
