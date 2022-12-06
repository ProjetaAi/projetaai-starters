# ProjetaAí Starter

## Disclaimer
Este starter foi feito com base no “[kedro starter Iris](https://kedro.readthedocs.io/en/stable/get_started/new_project.html)”, para começar este projeto, tenha um starter do Iris terminado e funcional. Para a realização deste tutorial, é esperado que você esteja familiarizado com a usabilidade normal do Kedro, como iniciar um projeto e o fazer rodar. Caso não esteja familiarizado com o Kedro, realizar o tutorial [Kedro Spaceflights](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html)

## Motivação

Imagine que nos encontremos na mesma situação do Iris porém desta vez, temos as informações das mesmas 3 flores em países diferentes, sendo eles Brasil, Canada e EUA, usaremos o multipipeline para processar diretamente essa informação

## Preparação

Para realização deste tutorial, é necessária a instalação de três pacotes adicionais, todos disponíveis por meio do pip, sendo eles kedro-partitioned(serve para criação da classe multipipeline, possibilitando trabalhar de maneira mais nítida com datasets particionados), azure-cli e adlfs.. Para instalar todos os pacotes necessários, execute o comando:

```
pip install -r src/requirements.txt
```

> Nota: É possível baixar o template que contém todas as informações prontas e que pode ser testado utilizando apenas dois comandos, az login e kedro run. 


## Alterações

Inicialmente, são realizadas mudanças no catálogo para possibilitar o acesso ao azure, nele são especificados os arquivos que serão utilizados e é utilizada uma variável definida no arquivo credentials.yml, ao qual especifica o endereço do azure que se encontra a pasta especificada da variável.

Em seguida, iremos copiar o csv do Iris, de maneira que tenhamos 3 cópias, “íris 1.csv”, “íris 2.csv” e “íris 3.csv”. É realizada então uma mudança no arquivo de catálogo adicionando variáveis, nota-se que o multipipeline não consegue trabalhar com variáveis particionadas em memória, portanto é necessário especificar os outputs dos nodes no arquivo ```catalog.yml ```: 

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

Após esta especificação, é necessário configurar novamente os parâmetros de forma a assimilar o país de cada um dos datasets de acordo com sua numeração, neste caso o “Iris 1.csv” receberá Brasil como uma coluna nova de forma a especificar o seu país de origem, a mudança no arquivo é alterar os parâmetros já existentes para um novo agrupamento, altere o arquivo ``` parameters.yml ``` para ficar da seguinte maneira:

```yml
para:
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

Por fim, é realizada uma alteração no arquivo ```pipeline.py``` e ```node.py``` (apenas na função ```report_accuracy``` ), com resultado final:
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

Com isto, ao se executar o comando ```kedro run```, serão gerados 3 arquivos com a acuracia de cada um dos três modelos.

A execução do comando ```kedro viz``` também se encontra a seguir