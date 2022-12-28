# ProjetaAi_mp Starter

## Disclaimer

The core objective of this starter is to make the user comfortable with the multipipeline functionality provided by the `kedro-partitioned` package. This starter was based on [pandas-iris](https://kedro.readthedocs.io/en/stable/get_started/new_project.html). 

It is possible to use this starter in two different ways:

As a reference guide to the multipipeline function, by running `kedro new --starter projetaai_mp` while having `kedro-projetaai` installed on the environment.

As a step-by-step best practice guide to using multipipeline.


# Step-by-step

In order to start this project from scratch, it is necessary to have a `pandas-iris` finished and ready to use. It is expected that you are familiarized with kedro's functionalities, and how to alter it and run it. In case you're not comfortable with using kedro, refer to this tutorial:  [Kedro Spaceflights](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html).



## Motivation

Imagine we find ourselves in the same Iris situation however, this time, there is information for the three species of flower for three different countries, Brazil, USA and Canada. This way, using [kedro-partitioned](https://github.com/ProjetaAi/kedro-partitioned)'s `multipipeline` to directly process this new information. 

## Preparation



In order to run this starter, it is necessary to install an additional packages, all avaiable throught `pip`, them being `kedro-partitioned`(used to create multipipelines, making it easier to work with partitioned datasets). In order to install it, execute the following, add the package to the `requirements.txt` file and run the following command:

```
pip install -r src/requirements.txt
```

> **Note**:
> It is possible to download the fully functional template for this project by simply running `kedro new --starter projetaai_mp`. It is then possible to run it and visualize it with the usual `kedro run` and `kedro viz` commands.


## Changes

Initially, copy the `iris.csv` file so the `data/01_raw` path contains `iris 1.csv` `iris 2.csv` and `iris 3.csv`, each one of those, representing a different country. It is then necessary to change the `catalog.yaml` file, adding the new variables. It is important to note that the multipipeline is unable to work with partitioned variables in memory, therefore, it is necessary to specify the node's outputs at `catalog.yaml`:

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


Next, it is necessary to change the parameters in a way that connects each country to a different dataset, this change makes sure the dataset receives a new column which specifies which country it belongs to. These changes can be seen on the `parameter.yml` which follows:

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

>```node.py```

```python
def report_accuracy(y_pred: pd.Series, y_test: pd.Series):
    """Calculates and logs the accuracy.

    Args:
        y_pred: Predicted target.
        y_test: True target.
    """
    accuracy = (y_pred == y_test).sum() / len(y_test)
    #logger = logging.getLogger(__name__)
    #logger.info("Model has accuracy of %.3f on test data.", accuracy)
    return("Model has accuracy of" + str(accuracy) +  " on test data.")

```


With this, by running `kedro run`, 3 files will be generated, each with the accuracy of each model.

