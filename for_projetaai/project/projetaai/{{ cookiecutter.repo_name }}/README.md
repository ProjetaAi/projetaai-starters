# {{ cookiecutter.project_name }}

## Description

### Overview

Insert the main idea of this project. What aims it to solve?

### Motivation

Input the reason for the existence of this project. Why has it been developed?

### Dataflow Diagram

Design a simple descriptive dataflow diagram. You can use [Mermaid](https://mermaid-js.github.io/mermaid/#/) and [MermaidCLI](https://github.com/mermaid-js/mermaid-cli#transform-a-markdown-file-with-mermaid-diagrams) and [VSCode Mermaid](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid), [PlantUML](https://plantuml.com/) or a custom markdown image under the `docs/assets` folder.

### Pipelines

Enter a simple description of the `Kedro` pipelines. If possible, use the same tools used in the DataFlow section for explaining it.

_Example:_

* **Data Engineering:** Pre-processes the inputs X, Y, Z using moving averages in order to smooth the prediction results producing A, B, C.

* **Data Science:** Predicts the inputs A, B, C values for the post three months from the execution moment using linear regression producing outputs D, E, F. 

### Inputs/Features

This project requires the following data/artifacts:

_Example:_

* Iris (CSV)
    * Sepal length
    * Sepal width
    * Petal length
    * Petal width
    * Species

### Outputs

This project generates the following data/artifacts:

_Example:_

* Species classifier (Pickle)
* Classifier metrics (JSON)
    * Accuracy
    * Recall

### Algorithm explanation

Explain the main data science process, what algorithm was chosen, why it was chosen, and how it solves the problem.

### Use Cases

Describe some possible scenarios for using this project outputs.

## Usage

### Installation

In order to run this project, execute the following steps:

1. Clone this repo
2. Go to the project folder using terminal
3. Run `pip install -r src/requirements.txt`

### Execution

For executing the pipelines mentioned before, run the following commands:

1. Execute `kedro <projetaai-plugin> init` for creating the missing local files
2. Run `kedro run --pipeline <pipeline_name>`

#### Notes

If required, add any more information the user should know for using this pipeline. For example, login operations.

## Development

There are some other tools required for changing the project source code. Execute the commands below:

1. Install dev deps with `pip install -r src/requirements-dev.txt`
2. Install test deps with `pip install -r src/requirements-test.txt`
3. Install pre-commit with `pre-commit install`
4. If unit tests were created, run `pytest` before committing to ensure no breaking changes were made.

## Authors

Enter the name and email of the authors in this section using a bullet list:

{%- set authors = cookiecutter.author.split(',') -%}
{%- for author in authors -%}
{%- set detail = author.split(';') -%}
* {{-detail[0]-}}; [{{-detail[1]-}}](mailto:{{-detail[1]-}})
{%- endfor -%}

## References

Fill this section with the articles and papers that were relevant to developing this solution.

_Example:_

1. [XOR-Net: An Efficient Computation Pipeline for Binary Neural Network
Inference on Edge Devices](https://cmu-odml.github.io/papers/XOR-Net_An_Efficient_Computation_Pipeline_for_Binary_Neural_Network_Inference_on_Edge_Devices.pdf)
