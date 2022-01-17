import pandas as pd, numpy as np
import torch
import random
import warnings
import json

from tqdm import tqdm

class LinkPredictor:
    """Python class implementing link prediction from pretrained embeddings"""
    
    def __init__(self, kwargs):
        self.model = kwargs.model_name
        self.target_relations = kwargs.target_relations
        self.entity_emb_path = kwargs.entity_emb_path
        self.relation_emb_path = kwargs.relation_emb_path
        self.full_embedding_path = kwargs.full_embedding_path
        
        self.max_num_entities = kwargs.max_num_entities
        self.min_score = kwargs.min_score
        
        self.path_to_triples = kwargs.path_to_triples
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        
        self.entity_id_map = kwargs.entity_id_map
        self.relation_id_map = kwargs.relation_id_map
        kg = open(self.path_to_triples, 'r')
        kg = kg.readlines()
        self.kg = {tp: i for i,tp in enumerate(kg)} # dictionary for fast lookup
        self.seed = kwargs.random_seed
        self.store_triples = kwargs.store_triples
        
        
    def load_embeddings(self):
        model = torch.load(self.full_embedding_path, map_location=self.device)
        with open(self.entity_id_map) as file:
            entity_id_map = json.load(file )
        with open(self.relation_id_map) as file:
            relation_id_map = json.load(file)
        ent_emb = pd.DataFrame(model.entity_embeddings._embeddings.weight.data.tolist(), index=list(entity_id_map.keys()))
        rel_emb = pd.DataFrame(model.relation_embeddings._embeddings.weight.data.tolist(), index=list(relation_id_map.keys()))
        self.entity_embs = ent_emb
        self.relation_embs = rel_emb
    
    def get_new_triples(self):
        
        print('\n############################## Finding new triples ##############################\n')
        self.load_embeddings()
        
        triples = []
        if self.target_relations == []:
            rels = list(self.relation_embs.index)
        else:
            rels = list(self.relation_embs.index)
            rels = [r for r in rels if any([p.lower() in r.lower() for p in self.target_relations])]
            print("Target relations: {}".format(rels))
        ents = list(self.entity_embs.index)
        
        random.seed(self.seed)
        random.shuffle(ents)
        
        group1 = ents[:self.max_num_entities]
        group2 = ents[self.max_num_entities : 2*self.max_num_entities]
        
        for rel in tqdm(rels, desc='Outer loop (on relations)'):
            for e1 in group1:
                for e2 in group2:
                    if not e1+'\t'+rel+'\t'+e2+'\n' in self.kg:
                        triples.append([e1, rel, e2])
        print('\n*********************** Number of initial candidate triples: {} ***********************\n'.format(len(triples)))
        return triples
      
    def score(self, emb_e1, emb_r, emb_e2):
        def TransE_pykeen(h, r, t):
            if h.ndim == 1:
                return 2*torch.sigmoid(-torch.norm(h+r-t, p=2))
            return 2*torch.sigmoid(-torch.norm(h+r-t, p=2, dim=-1))
    
        def Distmult_pykeen(h,r,t):
            if h.ndim == 1:
                return 2*torch.sigmoid(-torch.norm((h*r)-t, p=2))
            return 2*torch.sigmoid(-torch.norm((h*r)-t, p=2, dim=-1))
        if self.model == 'TransE':
            return TransE_pykeen(emb_e1, emb_r, emb_e2)
        if self.model == 'Distmult':
            return Distmult_pykeen(emb_e1, emb_r, emb_e2)
        raise ValueError
    
    def get_suggested_triples(self):
        new_triples = self.get_new_triples()
        new_triples = np.array(new_triples)
        suggested_triples = []
        
        print('\n############################## Getting highest scoring triples from Pykeen {} embeddings ##############################\n'\
             .format(self.model))
        try:
            e1_s = torch.tensor(self.entity_embs.loc[new_triples[:, 0].tolist()].values)
            r_s = torch.tensor(self.relation_embs.loc[new_triples[:, 1].tolist()].values)
            e2_s = torch.tensor(self.entity_embs.loc[new_triples[:, 2].tolist()].values)
            scores = self.score(e1_s, r_s, e2_s)
            valid_indices = (scores >= self.min_score).tolist()
            suggested_triples = new_triples[valid_indices].tolist()
            self.suggested_triples = suggested_triples
        except IndexError:
            print("Empty array %s" % suggested_triples)
        print('\n*********************** Number of suggested triples with score >= {}: {} ***********************\n'.format(self.min_score, len(suggested_triples)))
        return self
    
    def write_out_suggested_triples(self):
        if self.store_triples is True:
            print('\n'+'*'*20)
            print('Storing new triples')
            print('*'*20)
            write_out_path1 = self.path_to_triples.split('train')[0]+'train_completed.txt'
            write_out_path2 = self.path_to_triples.split('train')[0]+'new_triples.txt'
            with open(write_out_path1, 'w') as file1:
                file1.writelines(list(self.kg.keys()))
                file1.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))
            with open(write_out_path2, 'w') as file2:
                file2.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))