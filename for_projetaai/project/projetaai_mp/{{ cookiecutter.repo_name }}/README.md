# ProjetaAi_mp Starter

## Disclaimer

The core objective of this starter is to make the user comfortable with the multipipeline functionality provided by the `kedro-partitioned` package. This starter was based on [pandas-iris](https://kedro.readthedocs.io/en/stable/get_started/new_project.html). 

It is possible to use this starter in two different ways:

* As a reference guide to the multipipeline function, by running `kedro new --starter projetaai_mp` while having `kedro-projetaai` installed on the environment.

* As a step-by-step best practice guide to using multipipeline.

The output by running the command `kedro viz` is the following:

![kedro-viz](https://i.imgur.com/aBizh9i.jpg "pipeline image")

---


# Step-by-step

## Motivation

Imagine we find ourselves in the same [Iris](https://archive.ics.uci.edu/ml/datasets/iris) situation, however, this time there is information about the same flowers for three different countries, Brazil, the USA, and Canada. As each country has its particularity, it is necessary to create a specific model for each data, and so, 3 different models.  This way, using [kedro-partitioned](https://github.com/ProjetaAi/kedro-partitioned)'s `multipipeline` it is easier to proccess all this new information in a parallel manner. 


The step by step of data validation, data transformation, and model training is very similar for all data. Instead of manually repeating all the steps, we can use [kedro-partitioned](https://github.com/ProjetaAi/kedro-partitioned)'s multipipeline, which facilitates this process by dynamically repeating a group of processes based on some aggregation rules, in this case, country.

## Preparation

In order to start this project from scratch, it is necessary to have a [`pandas-iris`](https://kedro.readthedocs.io/en/stable/get_started/new_project.html) starter finished and ready to use. It is expected that you are familiarized with kedro's functionalities, and how to alter and run it. In case you're not comfortable with using kedro, refer to this tutorial:  [Kedro Spaceflights](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html).



In order to run this starter, it is necessary to install an additional package, avaiable throught `pip`, it being `kedro-partitioned` (used to create multipipelines, making it easier to work with partitioned datasets). In order to install it, add the package to the `requirements.txt` file and run the following command:

```
pip install -r src/requirements.txt
```

> **Note**:
> It is possible to download the fully functional template for this project by simply running `kedro new --starter projetaai_mp`. It is then possible to run it and visualize it with the usual `kedro run` and `kedro viz` commands.


## Changes

Initially, copy the `iris.csv` file paste it into the same folder, and rename, it so the data/01_raw path contains `iris 1.csv`, `iris 2.csv` and `iris 3.csv`, each one of those, will represent information collected in different countries. It is then necessary to change the `catalog.yml` file, to recognize the new files. 

The multipipeline functionality is unable to work with partitioned data in memory, therefore, it is necessary to specify all nodes outputs in the catalog.yaml.
All those modifications can be found below:

```yml
iris_data_multi:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/01_raw
  filename_suffix: .csv

iris_data_multi_with_country:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/03_primary
  filename_suffix: .csv

X_test:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/04_feature
  filename_suffix: xtest.csv
X_train:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/04_feature
  filename_suffix: xtrain.csv
y_train:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/04_feature
  filename_suffix: ytrain.csv
y_test:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/04_feature
  filename_suffix: ytest.csv

y_pred:
  type: PartitionedDataSet
  dataset: pandas.CSVDataSet
  path: data/04_feature
  filename_suffix: ypred.csv

accuracy:
  type: PartitionedDataSet
  dataset: text.TextDataSet
  path: data/07_model_output
  filename_suffix: accuracy.txt

```


Next, it is necessary to change the parameters in a way that connects each country to a different dataset, this change makes sure the datasets iris 1, iris 2, and iris 3 each receive a new column that specifies which country it belongs to. 

It is important to note that this change will be unnecessary in most cases when dealing with partitioned datasets, it is only necessary because we are emulating a real partitioned dataset on this starter. These changes can be seen on the `parameter.yml`:

```yml
parameters:
  train_fraction: 0.8
  random_state: 3
  target_column: species

config:
  template:
    pattern: 'iris {country}'

  configurators:
    -
      target:
        - '1'
      data: 'brasil'
    -
      target:
        - '2'
      data: 'eua'
    -
      target:
        - '3'
      data: 'canada'

```



Finally, we need to change the `pipeline.py` and `node.py`(only the `report_accuracy` function), which should be:

>```pipeline.py```
```python
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import make_predictions, report_accuracy, split_data

from kedro_partitioned.pipeline import multipipeline

def add_country(df,conf):
    return df.assign(country = conf)

def create_pipeline(**kwargs) -> Pipeline:
    return multipipeline(
        pipe = pipeline([
            node(
                func = add_country,
                inputs = ['iris_data_multi','params:config'],
                outputs = 'iris_data_multi_with_country',
                name = 'add_country'
            ),
            node(
                func=split_data,
                inputs=["iris_data_multi_with_country", "params:para"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split",
            ),
            node(
                func=make_predictions,
                inputs=["X_train", "X_test", "y_train"],
                outputs="y_pred",
                name="make_predictions",
            ),
            node(
                func=report_accuracy,
                inputs=["y_pred", "y_test"],
                outputs='accuracy',
                name="report_accuracy",
            ),
        ]),
        partitioned_input = 'iris_data_multi',
        name = 'multipipe1',
        configurator = 'params:config'
    )

```
The multipipeline can be configured in a whole array of different parameters, the most important ones being:


| parameter         | functionality                                                                                                                   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------|
| pipe              | the pipeline which will be used in the partitioned dataset.                                                                      |
| partitioned input | The variable named in the file `catalog.yml` that corresponds to the partitioned dataset.                                       |
| configurator      | The configurator which assimilates a particular information to the partitioned dataset.                                          |
| n_slices          | Determines the maximum number of slices the pipeline will be cut into. By default it is equal to the number of cores in the CPU. |


It is possible to change these configurations inside of this starter to obtain different pipelines, for example, altering the number of slices to be 3 or altering the configurator.

>```node.py```

```python
def report_accuracy(y_pred: pd.Series, y_test: pd.Series):
    """Calculates and logs the accuracy.

    Args:
        y_pred: Predicted target.
        y_test: True target.
    """
    accuracy = (y_pred == y_test).sum() / len(y_test)
    return("Model has accuracy of" + str(accuracy) +  " on test data.")

```





After all those modifications to the pandas-iris starter, running kedro run, 3 files will be generated. Each one containing the accuracy of the model trained for a specific country. 

Remembering that, for this starter, it is presumed that differences in the country's climate, soil condition, or environment can cause an accurate model in one country to be inaccurate in another. Because of that, it is necessary to create a different model for each country.

To replicate the effect of using the multipipeline that we have in this starter, would be necessary to create a pipeline for each country, or create a modular pipeline and manually specify its inputs and outputs and specify all this information on a `datacatalog.yml` file. 

When there aren't that many partitions in the dataset, using Kedro’s default functionalities is feasible. However, as the number of partitions in the dataset grows (if the dataset is partitioned by country, products categories, etc.) it becomes infeasible to manually input this information into the data catalog file or create that many pipelines.