# Anomalie detection in screw driving data (ProData)

## Overview

This project contains data and code from the research project "ProData": 

**Cross-process chain detection of material and process anomalies with Imbalanced Data for technical plastic assemblies**

The repository provides both means to extract and utilize the data as well as to understand and follow the code that was used during the analysis. The project is continously being updated. 

## Installation

Clone the repository to your local machine:


    git clone https://github.com/nikolaiwest/2023-prodata-sd-data-anomalies.git

Then go to the new repository:

    cd 2023-prodata-sd-data-anomalies


And install the required dependencies:

    pip install -r requirements.txt

## Usage

Currently, the data of this project is not made available publicly. However, this will follow at a later stage of this project. Then, data from a screw driving scenario can be loaded using either one of two data loaders. 

From path:

    data = DataFromPath([path_01, path_02])

or by scenario:

    data = DataFromScenario([1, 2])

Both, loading from path and loading by scenario, refers to the currently employed data structure (see [/data](/https://github.com/nikolaiwest/2023-prodata-sd-data-anomalies/tree/main/data) in this repository).

## Acknowledgement

The work on this repository is supported by supported by the **German Ministry of Education and Research (BMBF)** as part of program “Strengthening the data skills of the next generation of scientists” as well as by the program “NextGenerationEU” of the **European Union**.

## Contributing

Contributions are welcome. If you find a bug or have an enhancement in mind, please open an issue or submit a pull request.

![Funding BMBF](images/Förderhinweis_BMBF.jpg){: width="400px"}
![Funding EU](images/to/Förderhinweis_EU.jpg){: width="400px"}

## License
The project is currently licensed under the [MIT License](https://github.com/nikolaiwest/2023-prodata-sd-data-anomalies/blob/main/license).