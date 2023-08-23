# EnhancedRuleLearning
We implement an approach for improving rule learning via embedding-based KG enrichement


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

An error may occur during installation of pykeen. In such a case, we recommend using ```pip install pykeen``` in the newly created environment "enhancerl".


Install Java (version 8 or higher) in the environment (enhancerl): ```conda install -c bioconda java-jdk```


Download datasets and pretrained models by running `./download_data`


## Reproduce the reported results

1. Statistics of the generated rules using our approach:
 Make sure a jupyter kernel with the required libraries in `enhancerl` is installed. Open the notebook (analyzing mined rules)[analyzing_mined_rules.ipynb], activate the previously kernel and run all cells

2. Performance of the generated rules on link prediction on test sets:
 Open a terminal and run `python evaluate-rules-hits.py` with the following parameter options:
 
`
--kgs {wn18rr,fb15k,carcinogenesis,mutagenesis,openbiolink,yago3,drkg} [{wn18rr,fb15k,carcinogenesis,mutagenesis,openbiolink,yago3,drkg} ...]
                        Knowledge graph names, defaulting to wn18rr
--system {amie,AMIE,anyburl,AnyBURL}
                        System to execute, defaulting to amie
--models {TransE,Distmult,Rotate,transe,distmult,rotate} [{TransE,Distmult,Rotate,transe,distmult,rotate} ...]
                        Embedding model(s), defaulting to None
`

## Running rule mining systems 

1. Learning rules:
Open a terminal and run `python execute-system.py`. Parameter setting is the same as above

2. Configuration files:
Check whether configuration files are already present under `data/{System-Folder}`. Otherwise, run `python create-config.py`, where `{System-Folder}` is one of `AMIE`, `DistAMIE`, `RotAMIE`, `AnyBURL`

3. Applying mined rules:
Open a terminal and run `python apply-rules.py`. Parameter setting is also the same as above (i.e., same as in Reproduce the reported results)


## Training embeddings

Open a terminal in `EnhancedRuleLearning` and run `python src/embed_kgs_pykeen.py`. Use `python src/embed_kgs_pykeen.py -h` to view all available options


## Inferring new triples for KG completion

*Open a terminal in the main repository*

- Predict new links: ```python src/predict_new_links.py``` with the following options:

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

## Peliminary results

Link prediction performance using the mined rules

|                               | Hits@1  |  Hits@3 | MRR   |
|------------------------------------------------------------
|                                           :--AMIE+--:                   
| WN18RR                        | 0.390   | 0.395   | 0.398 |
| CARCINOGENESIS                | 0.216   | 0.245   | 0.248 |
| MUTAGENESIS                   | 0.217   | 0.244   | 0.244 |
| FB15K-237                     | 0.180   | 0.284   | 0.389 |
| YAGO3-10                      | 0.244   | 0.333   | 0.408 |
| DRKG                          | 0.147   | 0.172   | 0.215 |
| OPENBIOLINK                   | 0.038   | 0.081   | 0.158 |
|                                   :--Ours (with RotatE)--: 
| WN18RR                        | 0.384   | 0.390   | 0.392 |
| CARCINOGENESIS                | 0.220   | 0.248   | 0.252 |
| MUTAGENESIS                   | 0.182   | 0.215   | 0.227 |
| FB15K-237                     | 0.177   | 0.280   | 0.385 |
| YAGO3-10                      | 0.243   | 0.331   | 0.405 |
| DRKG                          | 0.147   | 0.172   | 0.215 |
| OPENBIOLINK                   | 0.059   | 0.129   | 0.258 |
|                                           :--AnyBURL--:       
| WN18RR                        | 0.469   | 0.527   | 0.594 |
| CARCINOGENESIS                | 0.483   | 0.533   | 0.630 |
| MUTAGENESIS                   | 0.477   | 0.547   | 0.639 |
| FB15K-237                     | 0.278   | 0.424   | 0.569 |
| YAGO3-10                      | 0.372   | 0.457   | 0.531 |
| DRKG                          | 0.064   | 0.075   | 0.090 |
| OPENBIOLINK                   | 0.009   | 0.016   | 0.026 |
