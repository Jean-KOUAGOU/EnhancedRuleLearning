import pandas as pd, numpy as np
import torch
import random
import warnings
import json
import os

base_path = os.path.dirname(os.path.realpath(__file__)).split('link_prediction')[0]

from tqdm import tqdm

class LinkPredictor:
    """Python class implementing link prediction from pretrained embeddings"""
    
    def __init__(self, kwargs):
        self.model = kwargs.model
        self.kg = (kwargs.kg).lower()
        self.target_relations = kwargs.target_relations
        self.full_embedding_path = base_path+'embeddings/'+self.kg+'_'+self.model+'/trained_model.pkl'
        
        self.max_num_entities = kwargs.max_num_entities
        self.max_num_relations = kwargs.max_num_relations
        self.min_score = kwargs.min_score
        
        self.path_to_triples = base_path+f'datasets/{self.kg}/train.txt'
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        
        self.entity_id_map = base_path+'embeddings/'+self.kg+'_'+self.model+'/entity_to_ids.json'
        self.relation_id_map = base_path+'embeddings/'+self.kg+'_'+self.model+'/relation_to_ids.json'
        triples = open(self.path_to_triples, 'r')
        triples = triples.readlines()
        self.triples = {tp: i for i,tp in enumerate(triples)} # dictionary for fast lookup
        self.seed = kwargs.random_seed
        self.store_triples = kwargs.store_triples
        
        
    def load_embeddings(self):
        model = torch.load(self.full_embedding_path, map_location=self.device)
        with open(self.entity_id_map) as file:
            entity_id_map = json.load(file)
        with open(self.relation_id_map) as file:
            relation_id_map = json.load(file)
        ent_emb = pd.DataFrame(model.entity_embeddings._embeddings.weight.data.tolist(), index=list(entity_id_map.keys()))
        rel_emb = pd.DataFrame(model.relation_embeddings._embeddings.weight.data.tolist(), index=list(relation_id_map.keys()))
        self.entity_embs = ent_emb
        self.relation_embs = rel_emb
    
    def get_new_triples(self):
        
        print('\n############################## Finding new triples ##############################\n')
        self.load_embeddings()
        
        random.seed(self.seed)
        triples = []
        if self.target_relations == []:
            rels = list(self.relation_embs.index)
            rels = random.sample(rels, min(len(rels),self.max_num_relations))
            print(f"Using the following relations: {rels}")
        else:
            rels = list(self.relation_embs.index)
            rels = [r for r in rels if any([p.lower() in r.lower() for p in self.target_relations])]
            print("Target relations: {}".format(rels))
        ents = list(self.entity_embs.index)
        
        random.shuffle(ents)
        
        max_num_ent = min(self.max_num_entities, len(ents)//2)
        group1 = ents[:max_num_ent]
        group2 = ents[max_num_ent : 2*max_num_ent]
        
        for rel in tqdm(rels, desc='Outer loop (on relations)'):
            for e1 in group1:
                for e2 in group2:
                    if not e1+'\t'+rel+'\t'+e2+'\n' in self.triples:
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
                return torch.sigmoid(torch.norm((h*r)*t, p=1))
            return torch.sigmoid(torch.norm((h*r)*t, p=1, dim=-1))
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
            print('All scores: ', scores)
            print('Max score: ', max(scores))
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
            write_out_path1 = self.path_to_triples.split('train')[0]+f'train_completed_{self.model}.txt'
            write_out_path2 = self.path_to_triples.split('train')[0]+f'new_triples_{self.model}.txt'
            with open(write_out_path1, 'w') as file1:
                file1.writelines(list(self.triples.keys()))
                file1.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))
            with open(write_out_path2, 'w') as file2:
                file2.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))
            print('Done !')