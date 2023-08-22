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
A conda environment (enhancerl) will be created. Next activate the environment:
``` conda activate enhancerl```

An error may occur during installation of pykeen. In such a case, use ```pip install pykeen``` in the newly created environment "enhancerl".


Install Java (version 8 or higher) in the environment (enhancerl): ```conda install -c bioconda java-jdk```


Download datasets and pretrained models by running `./download_data`


## Reproduce the reported results

1. Statistics of the generated rules using our approach:
 Open the notebook (analyzing mined rules)[Method/analyzing_mined_rules.ipynb] and run all cells

2. Performance of the generated rules on link prediction on test sets:
 Ope a terminal and run `python SAFRAN/python/eval.py SAFRANBinaries/results_{kg_name}/predictions.txt datasets/{kg_name}/test.txt`



## Inferring new triples for KG completion

*Open a terminal and navigate into Method/* ``` cd EnhancedRuleLearning/Method/```

- Predict new links on DRKG: ``` python predict_new_links ``` with the following options:

``` 
  --models {transe,distmult,rotate} [{transe,distmult,rotate} ...]
                        The embedding model used, e.g. TransE
  --kgs KGS [KGS ...]   The knowledge graph name
  --target_relations TARGET_RELATIONS [TARGET_RELATIONS ...]
                        Relation names to use for link prediction
  --num_entities NUM_ENTITIES
                        The number of entities to select
  --random_seed RANDOM_SEED
                        Random seed for random entity selection for link prediction
  --num_relations NUM_RELATIONS
                        The maximum number of relations to use in case none was given
  --topk_triples TOPK_TRIPLES
                        Top 50 highest scoring triples
  --store_triples [STORE_TRIPLES]
                        Whether to store the newly predicted triples
```

## Running AMIE+:

Copy ` amie-dev.jar ` into ` Method/AMIE ` and ` Method/TransAMIE `

- Run AMIE+ on original knowledge graphs: ` cd Method/AMIE ` then ` java -jar amie-dev.jar ../datasets/{kb}/train.txt `

- Run AMIE+ on completed knowledge graphs: `cd Method/TransAMIE ` then ` java -jar amie-dev.jar ../datasets/{kb}/train_completed_TransE.txt `

- To save the generated rules in each case, specify an output directory and file name by adding ` >> directory_name/file_name.txt ` at the end of the lines above


