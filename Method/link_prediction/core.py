import pandas as pd, numpy as np
import torch
#import pykeen.nn.representation
import random
import warnings
import json
import os

base_path = os.path.dirname(os.path.realpath(__file__)).split('link_prediction')[0]

from tqdm import tqdm

class LinkPredictor:
    """Python class implementing link prediction from pretrained embeddings"""
    
    def __init__(self, kg, model, kwargs):
        self.model_name = model.lower()
        self.kg = kg.lower()
        self.target_relations = kwargs.target_relations
        self.full_embedding_path = base_path+'embeddings/'+self.kg+'_'+self.model_name+'/trained_model.pkl'
        
        self.num_entities = kwargs.num_entities
        self.num_relations = kwargs.num_relations
        self.topk_triples = kwargs.topk_triples
        
        self.path_to_triples = base_path+f'datasets/{self.kg}/train.txt'
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        
        self.entity_id_map = base_path+'embeddings/'+self.kg+'_'+self.model_name+'/entity_to_ids.json'
        self.relation_id_map = base_path+'embeddings/'+self.kg+'_'+self.model_name+'/relation_to_ids.json'
        with open(self.path_to_triples, 'r') as file:
            triples = file.readlines()
        self.triples = {tp: i for i,tp in enumerate(triples)} # use a dictionary for fast lookup
        self.seed = kwargs.random_seed
        self.store_triples = kwargs.store_triples
        
        
    def load_embeddings(self):
        self.model = torch.load(self.full_embedding_path, map_location=self.device)
        self.model.eval()
        with open(self.entity_id_map) as file:
            self.entity_id_map = json.load(file)
        with open(self.relation_id_map) as file:
            self.relation_id_map = json.load(file)
    
    def get_new_triples(self):
        
        print('\n############################## Finding new triples ##############################\n')
        self.load_embeddings()
        
        random.seed(self.seed)
        triples = []
        if self.target_relations == []:
            if self.kg == 'drkg':
                rels = ['DGIDB::INHIBITOR::Gene:Compound', 'DRUGBANK::treats::Compound:Disease', 'GNBR::C::Compound:Disease',
                        'GNBR::Pa::Compound:Disease', 'GNBR::Pr::Compound:Disease', 'GNBR::T::Compound:Disease',
                        'Hetionet::CpD::Compound:Disease', 'Hetionet::CtD::Compound:Disease']
            else:
                rels = list(self.relation_id_map.keys())
                rels = random.sample(rels, min(len(rels),self.num_relations))
            print(f"Using the following relations: {rels}")
        else:
            rels = list(self.relation_id_map.keys())
            rels = [r for r in rels if any([t.lower() in r.lower() for t in self.target_relations])]
            print("Target relations: {}".format(rels))
        ents = list(self.entity_id_map)
        
        random.shuffle(ents)
        
        max_num_ent = min(self.num_entities, len(ents)//2)
        group1 = ents[:max_num_ent]
        group2 = ents[max_num_ent : 2*max_num_ent]
        
        for rel in tqdm(rels, desc='Outer loop (on relations)'):
            for e1 in group1:
                for e2 in group2:
                    if not e1+'\t'+rel+'\t'+e2+'\n' in self.triples:
                        triples.append([e1, rel, e2])
                    #if not e2+'\t'+rel+'\t'+e1+'\n' in self.triples:
                    #    triples.append([e2, rel, e1])
        print('\n*********************** Number of initial candidate triples: {} ***********************\n'.format(len(triples)))
        return triples
    
    def get_suggested_triples(self):
        new_triples = self.get_new_triples()
        new_triples = np.array(new_triples)
        self.suggested_triples = []
        
        print('\n############################## Getting highest scoring triples from Pykeen {} embeddings ##############################\n'\
             .format(self.model_name))
        #try:
        e1_s = torch.tensor(list(map(self.entity_id_map.get, new_triples[:, 0]))).unsqueeze(1)
        r_s = torch.tensor(list(map(self.relation_id_map.get, new_triples[:, 1]))).unsqueeze(1)
        e2_s = torch.tensor(list(map(self.entity_id_map.get, new_triples[:, 2]))).unsqueeze(1)
        h_r_t = torch.cat([e1_s,r_s,e2_s], dim=1)
        scores = self.model.score_hrt(h_r_t)
        sorted_vals, indices = torch.sort(scores.detach().squeeze(), descending=True) # sort scores and rank triples
        valid_indices = indices.tolist()[:self.topk_triples]
        self.suggested_triples = new_triples[valid_indices]
        return self
    
    def write_out_suggested_triples(self):
        if self.store_triples is True:
            print('\n'+'*'*20)
            print('\n*********************** Storing top {} suggested triples ***********************\n'.format(len(self.suggested_triples)))
            print('*'*20)
            write_out_path1 = self.path_to_triples.split('train')[0]+f'train_completed_{self.model_name}_top{self.topk_triples}.txt'
            write_out_path2 = self.path_to_triples.split('train')[0]+f'new_triples_{self.model_name}_top{self.topk_triples}.txt'
            with open(write_out_path1, 'w') as file1:
                file1.writelines(list(self.triples.keys()))
                file1.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))
            with open(write_out_path2, 'w') as file2:
                file2.writelines(list(map(lambda x: x[0]+'\t'+x[1]+'\t'+x[2]+'\n', self.suggested_triples)))
        print('Done !')