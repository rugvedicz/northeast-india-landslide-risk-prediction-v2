# Northeast India Landslide Risk Prediction 🌧️

A Big Data and Machine Learning project that estimates landslide risk across Northeast India using historical landslide records, geographical information, weather conditions, and seasonal patterns.

The project combines historical data analysis, live weather collection, a Random Forest classification model, and a Streamlit dashboard to display weather conditions and estimated landslide risk for eight locations in Northeast India.

> **Disclaimer:** This is an educational and experimental project, not an official landslide early-warning system. Model outputs should not be used as the sole basis for safety or emergency decisions.

## 📌 Project Objectives

- Analyze historical landslide records and weather-related features.
- Collect current weather information for eight locations in Northeast India.
- Process rainfall, temperature, humidity, and geographical data.
- Train and evaluate Machine Learning classification models.
- Compare Logistic Regression and Random Forest.
- Display weather information and model predictions through an interactive Streamlit dashboard.
- Demonstrate how Big Data processing and Machine Learning can be combined for environmental risk analysis.

## 🗺️ Locations Covered

The project monitors the following eight state capitals:

- Itanagar — Arunachal Pradesh
- Dispur — Assam
- Agartala — Tripura
- Aizawl — Mizoram
- Gangtok — Sikkim
- Imphal — Manipur
- Kohima — Nagaland
- Shillong — Meghalaya

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning and model evaluation |
| Random Forest | Main classification model |
| Logistic Regression | Comparison model |
| PySpark | Big Data processing workflow |
| Open-Meteo API | Live weather data collection |
| Streamlit | Interactive dashboard |
| Joblib | Saving and loading trained model artifacts |
| Git and GitHub | Version control and project hosting |

## 📊 Features Used by the Model

The Random Forest model uses eight input features.

| No. | Feature | Description |
|---:|---|---|
| 1 | `latitude` | Latitude of the geographical location |
| 2 | `longitude` | Longitude of the geographical location |
| 3 | `rainfall_event_day_mm` | Rainfall associated with the event day, in millimetres |
| 4 | `rainfall_3day_mm` | Rainfall total over the preceding three days |
| 5 | `rainfall_7day_mm` | Rainfall total over the preceding seven days |
| 6 | `temperature_c` | Temperature in degrees Celsius |
| 7 | `humidity_percent` | Relative humidity as a percentage |
| 8 | `month` | Month of the year, representing seasonal patterns |

These features help the model learn relationships between geographical conditions, weather variables, seasonal patterns, and the records in the training dataset.

## 🧠 Dataset and Target Variable

The experimental dataset contains **502 records**:

- 251 historically recorded landslide-event records.
- 251 candidate comparison-date records.

The target variable is `landslide_risk`.

| Label | Meaning |
|---:|---|
| `1` | Recorded landslide event |
| `0` | Candidate comparison date |

### What is a candidate comparison date?

A candidate comparison date is selected for comparison with recorded landslide events when no event is listed for that date in the dataset.

It is important to understand that these dates are **not verified landslide-free observations**. An event may have occurred but not been included in the source catalogue. This limitation can affect model evaluation and the reliability of predictions.

## ⚙️ Machine Learning Approach

The project follows these steps:

1. **Data collection:** Obtain historical landslide records and weather information.
2. **Data preparation:** Clean the dataset and prepare the required features.
3. **Feature selection:** Use the eight geographical, rainfall, temperature, humidity, and seasonal features.
4. **Model training:** Train Logistic Regression and Random Forest classifiers.
5. **Model evaluation:** Compare the models using classification metrics and ROC-AUC.
6. **Model saving:** Save the trained Random Forest model and feature list.
7. **Live weather collection:** Retrieve current weather and recent rainfall information for the selected locations.
8. **Prediction:** Pass the latest available weather features to the trained model.
9. **Visualization:** Display the results through the Streamlit dashboard.

## 📊 Model Evaluation

We compared Logistic Regression and Random Forest using 101 test records.

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 69.3% | **72.3%** |
| Precision (Class 1) | 67.3% | 67.2% |
| Recall (Class 1) | 74% | **86%** |
| F1-Score (Class 1) | 70.5% | **75.4%** |
| ROC-AUC | 0.776 | **0.809** |

**Selected Model:** Random Forest performed better overall, with higher accuracy, recall, F1-score, and ROC-AUC.

**Note:** Results are experimental because candidate comparison dates are not verified landslide-free observations. This project is not an official early-warning system.

## 🌦️ Live Weather Collection

The project uses the Open-Meteo API to collect weather information for all eight locations.

The weather collector records information such as:

- Timestamp
- Location and state
- Latitude and longitude
- Current rainfall
- Event-day rainfall field
- Three-day rainfall total
- Seven-day rainfall total
- Temperature
- Relative humidity
- Month

Records are appended to a JSON Lines file:

`data/live_weather_stream.json`

The collector is designed to run repeatedly and add new weather records at regular intervals.

## 📈 Streamlit Dashboard

The dashboard provides a visual interface for examining the project's outputs. Depending on the available data, it includes:

- A map showing the monitored locations
- Location-wise weather information
- Weather and risk metrics
- Charts for comparing conditions
- A location inspector
- Estimated landslide-risk predictions

The dashboard connects the data-collection and prediction workflow to an interface that is easier to understand than raw data or model output.

## 📁 Project Structure

```text
landslide-risk-prediction/
│
├── data/
│   ├── processed/
│   │   └── landslide_dataset.csv
│   ├── raw/
│   │   ├── Global_Landslide_Catalog_Export_rows.csv
│   │   └── northeast_landslide_events.csv
│   └── live_weather_stream.json
│
├── models/
│   ├── landslide_features.pkl
│   ├── model_metadata.json
│   └── random_forest_landslide.pkl
│
├── notebooks/
│   ├── models/
│   ├── landslide_events_with_weather.csv
│   ├── landslide_ml.ipynb
│   └── northeast_landslide_events_clean.csv
│
├── app.py
├── live_weather_collector.py
├── live_weather_prediction.py
├── README.md
└── .gitignore
```

*This is the intended project structure; adjust the file list to match the files actually included in your GitHub repository. Do not upload virtual environments, API credentials, or unnecessary generated files.*

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd landslide-risk-prediction
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the repository includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Make sure the installed package versions are compatible with the saved model.

### 4. Start the live weather collector

Open a terminal and run:

```bash
python live_weather_collector.py
```

Keep the collector running so that it can continue collecting weather records.

### 5. Start the Streamlit dashboard

Open another terminal in the project directory, activate the same environment, and run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to access the dashboard.

## 🔍 Limitations

- The dataset is experimental and relatively small.
- Candidate comparison dates are not confirmed landslide-free observations.
- Missing historical events can introduce label errors.
- Weather conditions alone cannot capture every factor affecting landslides, such as slope, soil properties, geology, drainage, and land use.
- Model scores are not necessarily calibrated probabilities of a real landslide occurring.
- Live predictions depend on weather API availability, data freshness, and correct feature preparation.
- The model requires additional validation across different locations and time periods.

For these reasons, this application should be treated as an academic demonstration rather than an operational disaster-warning service.

## 🚀 Future Improvements

- Expand the dataset with verified landslide and non-landslide observations.
- Add geological, elevation, slope, and soil-related features.
- Evaluate the model using time-based and location-based validation.
- Improve data quality and monitor missing or outdated weather records.
- Explore distributed data processing for larger datasets.
- Improve prediction calibration and report uncertainty.
- Integrate validated information from reliable geological and disaster-management sources.

## 🎓 Project Significance

This project demonstrates the integration of Big Data concepts, live weather data collection, data preprocessing, Machine Learning, and interactive visualization for an environmental risk-analysis use case.

It provides a foundation for further research into how historical and real-time data can help researchers understand conditions associated with landslide events.

## 👩‍💻 Authors

**Rugvedi Khandekar** ,
**Chandani Yadav** ,
**Shinjinee Biswas**

B.Tech — Artificial Intelligence and Machine Learning

St. John College of Engineering and Management

---

*Developed as an academic Big Data and Machine Learning project.*
