"""
This is a boilerplate pipeline
generated using Kedro 0.18.2
"""

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
                inputs=["iris_data_multi_with_country", "params:parameters"],
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
        configurator = 'params:config',
    )

    
    

    
