# Aadhaar-Last-Mile-Friction-Index
AI-Powered Dashboard to measure Aadhaar Maintenance Friction and Child Exclusion Risk (UIDAI Hackathon 2026).
# 🇮🇳 The Last-Mile Friction Index
### UIDAI Hackathon 2026 Submission

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![ML](https://img.shields.io/badge/AI-KMeans%20Clustering-green)

## 🚀 Project Overview
While Aadhaar enrolment has reached near-saturation, **Identity Access** does not guarantee **Service Delivery**. 
This project introduces the **Friction Index**—a new metric to quantify the "maintenance burden" citizens face (updating biometrics, correcting errors) versus new enrolment.

We use **Unsupervised Machine Learning (K-Means)** to segment Indian districts into risk categories and identify "Scholarship Time Bombs" where children are at risk of service exclusion.

## 🎥 Live Demo
**[Click Here to Watch the Video Demo]**

## 📊 Key Features
1.  **AI-Powered Clustering:** Automatically segments districts into "Healthy Growth," "High Maintenance," and "Critical Friction."
2.  **Geospatial Intelligence:** Zoomable, interactive map of India identifying bureaucratic hotspots.
3.  **Child Risk Predictor:** Tracks Mandatory Biometric Update (MBU) gaps to prevent scholarship failure.
4.  **Action Plan Generator:** One-click export of priority districts for field officers.

## 📂 System Architecture
The project is modularized into four core components:

* **`dashboard_interface.py`**: The Streamlit-based frontend for the Command Center.
* **`risk_segmentation_engine.py`**: The Machine Learning module utilizing K-Means for district clustering.
* **`etl_processor.py`**: The Data Engineering pipeline for standardizing 1,000+ district names.
* **`geospatial_integrator.py`**: The bridging module for merging statistical risk vectors with coordinate data.

## 🚀 Deployment Instructions
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/kresx/Aadhaar-Last-Mile-Friction-Index
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch the Command Center:**
    ```bash
    streamlit run dashboard_interface.py
    ```

## 📄 License
This project was developed for the **UIDAI Data Hackathon 2026**.
