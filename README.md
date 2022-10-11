# EnhancedRuleLearning
We implement an approach for improving rule learning by means of enriching KGs with link prediction


## Installation

Clone this repository:
```
https://github.com/Jean-KOUAGOU/EnhancedRuleLearning.git
```
First install Anaconda3, then all required librairies by running the following:
```
conda env create -f environment.yml
```
A conda environment (secondment) will be created. Next activate the environment:
``` conda activate secondment```

An error may occur during installation of pykeen. In such a case, use ```pip install pykeen``` in the newly created environment "secondment".


Install Java (version 8 or higher) in the environment (secondment): ```conda install -c bioconda java-jdk```


Download ```datasets.zip``` from [drive](https://drive.google.com/file/d/1qu2_c_SCBql6QGFA6hipiIlgw0p4fKRr/view?usp=sharing), extract them into Method/


## Reproduce the reported results on improved rule mining with AMIE+:

- Make sure Jupyter lab is installed. Open the file ` rule_mining.ipynb ` and run all cells.



## New triple inference

*Open a terminal and navigate into Method/* ``` cd EnhancedRuleLearning/Method/```

- Predict new links on DRKG: ``` python predict_new_links ``` with the following options:

``` 
  --model_name MODEL_NAME
                        The embedding model used, e.g. TransE
                        
  --kg KG               The knowledge graph name
  
  --target_relations TARGET_RELATIONS [TARGET_RELATIONS ...]
                        Relation names to use for link prediction
                        
  --max_num_entities MAX_NUM_ENTITIES
                        The maximum number of entities to select
                        
  --min_score MIN_SCORE
                        The minimum score triples should have to be accepted as true triples
                        
  --random_seed RANDOM_SEED
                        Random seed for random entity selection for link prediction
                        
  --store_triples [STORE_TRIPLES]
                        Whether to store the newly predicted triples
```

## Running AMIE+:

Copy ` amie-dev.jar ` into ` Method/AMIE ` and ` Method/TransAMIE `

- Run AMIE+ on original knowledge graphs: ` cd Method/AMIE ` then ` java -jar amie-dev.jar ../datasets/{kb}/train.txt `

- Run AMIE+ on completed knowledge graphs: `cd Method/TransAMIE ` then ` java -jar amie-dev.jar ../datasets/{kb}/train_completed_TransE.txt `

- To save the generated rules in each case, specify an output directory and file name by adding ` >> directory_name/file_name.txt ` in front of the lines above


