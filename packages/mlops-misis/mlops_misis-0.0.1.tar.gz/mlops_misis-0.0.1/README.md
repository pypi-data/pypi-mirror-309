# mlops_misis

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

roman-shinkarenko-17 MLOps MISIS Course 

## Запуск airflow

Перед первым запуском
```shell
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```
make airflow_up
```
или 

```shell
docker compose up airflow-init
docker compose up --build -d
```
Web доступен на 8080 порте

Логин: airflow \
Пароль:airflow


## Даги

### Генерация датасета
![img.png](images/generate_dataset_dag.png)

### Обучение модели

![img.png](images/img.png)
### Сенсор предикт по файлу с удалением

![img_1.png](images/img_1.png)

## pylint

![pylint results](images/pylint.png)

## tests coverage and results 

![pytest](images/pytest.png)

## Запуск

- установка зависимостей 

```
pip install -r requirements.txt
```

- конфигурация config.yaml

```
ml_model_params:
  ml_model_type: RandomForestClassifier # LogisticRegression | DecisionTreeClassifier
  max_depth: 10 # обязательный параметр для моделях на деревьях
  n_estimators: 100 # обязательный параметр для RandomForestClassifier
  C: 1.0 # обязательный параметр для LogisticRegression
  run_name: run_1 # название запуска
  validate_model: True # проводить валидацию модели или нет

data_params:
  n_features: 123 # число признаков
  n_samples: 1000 # количество объектов
  dataset_name: dataset_1 # название датасета
  train_size: 0.75 # часть выборки для обучения
```

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
│                         mlops_misis and configuration for tools like black
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
└── mlops_misis   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes mlops_misis a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

