Плешаков Иван БИВТ-21-16

## HW5

python-publish
![image](https://github.com/user-attachments/assets/ed54b37c-f5ef-4f24-8400-4a1318f084d9)

docker-publish
![image](https://github.com/user-attachments/assets/de6b26b9-9644-4188-967c-fd8dfc2530d4)


## HW4
![image](https://github.com/user-attachments/assets/488db4ea-fb77-4a05-af6c-c53b47471974)
![image](https://github.com/user-attachments/assets/07a6560d-0c84-4f1a-923d-91ffeee078d9)


## HW3
- dvc dag   
+--------------+   
| make_dataset |  
+--------------+  
        *  
        *  
        *  
+-------------+  
| train_model |  
+-------------+  

- dvc repro
- dvc metrics  
Path                      Accuracy  
reports\metrics_dvc.json  0.92  

## HW2
.../pleshakov-ivan-16> pylint mlops (9/10)  
.../pleshakov-ivan-16> pytest --cov=mlops tests/ (96%)

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         mlops and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
│
├── tests   <- Test code.
│   │
│   ├── __init__.py             <- Makes tests a Python module
│   │
│   ├── conftest.py
│   │
│   ├── test_dataset.py 
│   │
│   ├── test_model.py
│   │
│   └── test_global_params.yaml 
│
│
└── mlops   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes mlops a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── params                  <- Configs for all parameters.               
    │   ├── global_params.yaml
    │   ├── models_params.yaml
    │   ├── read_global_params.py
    │   └── read_models_params.py
    │
    └── modeling                
        ├── __init__.py 
        └── train.py            <- Code to train models
```

