
# 🌍 Global Voices on COP 29: A Cross-Country Twitter Analysis

**Conference:** 5th World Conference on Climate Change and Global Warming  
**Venue:** Vienna, Austria | **Date:** 7–9 March 2025  
**Lead Author:** Oluwole Fagbohun  
**Collaborators:** Ifeoluwa Wuraola, Sadeeq Akintola, Nelson Ogbeide, Ilemona Abutu, Temitope Kadri, Joshua Obodai, Anuoluwapo Gabriel, Bisola Kayode, Okiki-Jesu Timothy Olumide, Peter Adetola Adetunji, Mgbame Michael  

---

## 📘 Project Description

This project performs a comprehensive, multilingual Twitter analysis of public discourse surrounding COP 29. Using NLP, machine learning, and time series techniques, the study explores:

- **Aspect-Based Sentiment Analysis (ABSA)**
- **Engagement Metrics & Influencer Insights**
- **Temporal & Geographic Trends**
- **Topic Clustering and Content Themes**

The dataset includes **182,347 tweets** collected between **11 October 2024 and 10 December 2024** via Twitter API.

---

## 📊 Key Features & Insights

### 🔍 Sentiment Analysis
- Positive: 40.1%, Neutral: 32.0%, Negative: 27.9%
- Most optimistic themes: *Technology & Innovation, Youth Activism*
- Most critical themes: *Climate Finance, Equity, Policy Inaction*

### 🔎 Aspect-Based Analysis
- 15 dominant aspects identified (e.g., Climate Action, Biodiversity, Public Health)
- Aspect × Sentiment heatmap highlights public perception by topic

### 📈 Temporal Patterns
- Peak activity: 21 November 2024 (14,981 tweets)
- Sentiment trends aligned with COP speeches, announcements, and press events

### 🧠 Topic Clustering
- Optimal number of clusters: 9 (KMeans + TF-IDF + PCA)
- Largest cluster (62.6%) focused on *green energy and sustainability*
- Cluster sentiment distribution provided for each topic group

### 🔥 Engagement Metrics
- Composite engagement score from retweets, likes, replies, views
- Viral content more likely to carry emotional or polarising sentiment
- Most liked tweet: Zoo conservation (216,915 likes)
- Most viewed tweet: Greenland melt crisis (9.96M views)

### 🌐 Geographic & User Insights
- Location-based sentiment patterns (when available)
- Bias analysis of top 20 most active users
- User clusters with 100% positive/negative bias identified

---

## 🧰 Technologies Used

- Python 3.10  
- Pandas, NumPy, Seaborn, Matplotlib  
- Scikit-learn (KMeans, PCA, TF-IDF)  
- Statsmodels (seasonal decomposition)  
- NLTK (tokenisation, stopword filtering)  
- WordCloud, Heatmaps, KDE, Time Series Plots  

---

## 📁 Project Structure

```bash
├── README.md
├── global_voices.pdf             # Project Report & Full Visuals
├── analysis_results_with_sentiments-3.csv  # Cleaned and annotated dataset
├── visuals/                      # Exported figures (optional)
└── src/
    ├── absa_analysis.py         # Aspect-Based Sentiment Analysis
    ├── engagement_analysis.py   # Engagement Metrics Analysis
    ├── time_series_trends.py    # Temporal Analysis
    ├── clustering_model.py      # Topic Clustering
    ├── wordclouds_ngrams.py     # Text Visualization
    ├── twitter_scraper.py       # Twitter Data Collection
    ├── twitter_main.py          # Main Entry Point
    ├── data_extract.py          # Data Extraction Utilities
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py          # Configuration Settings
    │   └── keywords.py          # Search Keywords
    └── utils/
        ├── __init__.py
        ├── logger.py            # Logging Configuration
        └── data_processor.py    # Data Processing Utilities

---

## 🧪 How to Reproduce

1. Clone this repository  
2. Install dependencies from `requirements.txt`  
3. Run analysis notebook or Python script segments
4. View outputs in the `visuals/` folder or generate plots inline

---

## 📌 Suggested Visualisations for Poster

- **Bar Chart:** Sentiment by Aspect  
- **Heatmap:** Aspect × Sentiment (%)  
- **PCA Scatter Plot:** Topic Clusters by Sentiment  
- **Line Chart:** Sentiment Over Time (Stacked + Normalised)  
- **Heatmap:** Sentiment by Day of Week  
- **Word Clouds:** Overall + Sentiment-Specific  
- **Box Plot:** Engagement Scores by Sentiment  
- **User Heatmap:** Bias of Top 15 Active Users

---

## 📚 References

Refer to the full list in the bottom section of the poster or report PDF.

---

## 🤝 Acknowledgements

Thanks to collaborators from Carbonnote, Readrly, Pavolera Tech, Hankali Intel, and various UK/EU universities for contributions and feedback.

---

## 📬 Contact

- Oluwole Fagbohun — `wole@readrly.io`  
- LinkedIn: [linkedin.com/in/wolehat](https://www.linkedin.com/in/wolehat/)

---
