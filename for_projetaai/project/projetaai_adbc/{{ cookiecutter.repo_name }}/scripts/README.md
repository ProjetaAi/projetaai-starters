# Model Scripts

This directory contains scripts for model inference from http requests.

## Script definition

Any deploy script must contain three functions:

- `init`: This function is called once when the server starts. It is used to load the model and other resources.
- `prepare`: This function is called for each request. It is used to prepare the data for the model.
- `predict`: This function is called for each request. It receives the prepared data and the model as parameter and returns the response body.

### A minimal example

```python
from kedro.io import DataCatalog
from sklearn.linear_model import LinearRegression
from kedro_projetaai.framework.model import ScriptException, assert_script
import numpy as np


def init(catalog: DataCatalog) -> LinearRegression:
    # Load the model
    return catalog.load("regressor")


def prepare(data: list) -> np.ndarray:
    # Prepare data for model
    try:
        data = np.array([data])
        assert_script(np.issubdtype(data.dtype, np.number), "Invalid type")
        assert_script(len(data.shape) == 2, "Invalid shape")
        return data
    except Exception as e:
        # this will be returned as a 400 error
        raise ScriptException(f"Invalid data due to {str(e)}") from e


def predict(model: LinearRegression,
            prepared_data: np.ndarray) -> dict:
    # Predicts the request data
    return {'inference': model.predict(prepared_data).tolist()}
```
