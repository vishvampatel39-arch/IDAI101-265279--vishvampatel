# 💧 WaterBuddy – Your Daily Hydration Companion

A Streamlit hydration tracker built for the school Python FA-2 assessment.
Educational project only – not a medical device. Data lives in the browser
session and resets when the tab closes.

## Project layout

| File | What it does |
|------|--------------|
| `app.py` | The screens (10 pages) and styling |
| `logic.py` | Hydration maths, milestones, achievements (no Streamlit code) |
| `data.py` | Age groups, foods, infusions, tips |
| `test_app.py` | Automated tests |
| `requirements.txt` | Packages the deployed app needs |
| `requirements-dev.txt` | Same + pytest, for running tests locally |
| `.streamlit/config.toml` | Forces the light theme |

## Run locally (Windows)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -v
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo (the `.venv` folder is ignored by `.gitignore`).
2. Go to share.streamlit.io, choose the repo and set the main file to `app.py`.
3. Click **Deploy**.

## Data sources

Food water-content values are based on USDA FoodData Central
(https://fdc.nal.usda.gov/). Infusion facts cite the sources listed on each card.

streamlit link:**https://idai101-265279--vishvampatel-7ywjrcnj2jmwlnp6dmaual.streamlit.app/**
