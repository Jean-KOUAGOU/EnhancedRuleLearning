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


Download ```datasets.zip``` from [drive](https://drive.google.com/file/d/1yrHSw4FZTYpkI3Qs8y2ejW1slH51zYJF/view?usp=sharing), extract it into Method/


## Reproducing the reported results

### Link Prediction

*Open a terminal and navigate into Method/* ``` cd EnhancedRuleLearning/Method/```
- Predict new links on DRKG: ``` python predict_new_links ``` with the following options:

``` 
  --model_name MODEL_NAME
                        The embedding model used, e.g. TransE
  --full_embedding_path FULL_EMBEDDING_PATH
                        Full embedding path, expecting a pykeen embedding
                        model saved as a pickle object
  --target_relations TARGET_RELATIONS [TARGET_RELATIONS ...]
                        Relation names to use for link prediction
  --entity_emb_path ENTITY_EMB_PATH
                        Entity embedding path
  --relation_emb_path RELATION_EMB_PATH
                        Relation embedding path
  --max_num_entities MAX_NUM_ENTITIES
                        The maximum number of entities to select
  --min_score MIN_SCORE
                        The minimum score triples should have to be accepted
                        as true triples
  --random_seed RANDOM_SEED
                        Random seed for random entity selection for link
                        prediction
  --path_to_triples PATH_TO_TRIPLES
                        Path to data triples
  --entity_id_map ENTITY_ID_MAP
                        Entity name to id map, same as the one used during
                        training
  --relation_id_map RELATION_ID_MAP
                        Relation name to id map, same as the one used during
                        training
  --store_triples STORE_TRIPLES
                        Whether to store the newly predicted triples
```

*Navigate into Method/anyBURL/* ``` cd Link_Prediction_NCES/Method/anyBURL```

*Configure config-learn.properties and*:

- Learn AnyBURL rules: ```java -Xmx4G -cp anyBURL-RE.jar de.unima.ki.anyburl.LearnReinforced config-learn.properties```
