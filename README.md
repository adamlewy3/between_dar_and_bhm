# Between Darlington and Birmingham (by train).

- An End to End ML model for predicting train delays between Darlington and Birmingham. 

### Project Structure
 
between_dar_and_bhm/
├── .gitignore
├── data_collection/
│   ├── data/
│   │   ├── bhm_to_dar.csv
│   │   ├── dar_to_bhm_weather.csv
│   │   ├── dar_to_bhm.csv
│   │   ├── rids_bhm_to_dar.json
│   │   └── rids_dar_to_bhm.json
│   ├── details_pipeline.py
│   ├── metrics_pipeline.py
│   ├── test_utils.py
│   ├── testdata/
│   │   ├── 202510036723824.json
│   │   ├── 202510216723821.json
│   │   ├── empty_response.json
│   │   ├── sample_details_response.json
│   │   └── sample_response.json
│   ├── utils.py
│   └── weather_pipeline.py
└── model/
    ├── cleaned_data/
    │   ├── cancelled_trains_dar_to_bhm.csv
    │   └── not_cancelled_trains_dar_to_bhm.csv
    ├── EDA.ipynb
    ├── plotting_utils.py
    └── predictions.md

### Acknowledgements 

- Many thanks to Network Rail for providing access to the Darwin HSP API, for their useful website, and the Rail Data Marketplace account on github, which is full of helpful code examples.
- This project owes a lot to the [FI-TW](https://open-research-europe.ec.europa.eu/articles/6-324) dataset, and the modelling done there.


