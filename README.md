# Conceptual Models Pattern Mining and Analysis Toolkit

This is an exploratory tool, which, through the combination of frequent subgraph mining algorithm and graph manipulation techniques, can process multiple conceptual models and discover recurrent graph structures according to multiple criteria. The tool is adapted to mine information from two main state-of-the-art conceptual modeling languages, nemely [OntoUML](https://github.com/OntoUML/ontouml-models) and [ArchiMate](https://github.com/me-big-tuwien-ac-at/EAModelSet), and can be easily adapted to other languages by plugging-in new importing and visualization components.

The primary objective is to offer a support facility for language engineers. This can be employed to leverage both good and bad modeling practices, to evolve and maintain the conceptual modeling language, and to promote the reuse of encoded experience in designing better models with the given language.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation
You can install the library using the following pip command:

```bash
git clone https://github.com/unibz-core/CM-Mining
```

- create the following folders, `domain_patterns`, `patterns`, `input`.
- install the dependencies you find in the `requirements.txt` file.
- run the `main.py` file from the root `script` folder. 
- (!) Note that this application requires `Python==3.9`

## Usage

Follow the input from the command line and play. 

## License

This project is licensed under the Apache License 2.0.

## Acknowledgments

You can use this section to credit any individuals, libraries, or resources that inspired or assisted your project.# CM-Mining

# Citing

If this tool is helpful to your research, please consider citing it. 

The article is currently under evaluation for publication at the [International Journal on Software and Systems Modeling (SoSyM)](https://www.sosym.org/), the pre-print version is available [here](https://arxiv.org/abs/2406.07129).