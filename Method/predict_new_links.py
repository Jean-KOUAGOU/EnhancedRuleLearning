from link_prediction.core import LinkPredictor
import argparse

if __name__ == "__main__":
    def str2bool(v):
        if isinstance(v, bool):
            return v
        elif v.lower() in ['t', 'true', 'y', 'yes', '1']:
            return True
        elif v.lower() in ['f', 'false', 'n', 'no', '0']:
            return False
        else:
            raise ValueError('Ivalid boolean value.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='TransE', help="The embedding model used, e.g. TransE")
    parser.add_argument('--full_embedding_path', type=str, default='./embeddings/drkg_TransE/trained_model.pkl', help="Full embedding path, expecting a pykeen embedding model saved as a pickle object")
    parser.add_argument('--target_relations', nargs='+', default=[], help="Relation names to use for link prediction")
    parser.add_argument('--entity_emb_path', type=str, default='./datasets/drkg/TransE_entity_embeddings.csv', help="Entity embedding path")
    parser.add_argument('--relation_emb_path', type=str, default='./datasets/drkg/TransE_relation_embeddings.csv', help="Relation embedding path")
    parser.add_argument('--max_num_entities', type=int, default=100, help="The maximum number of entities to select")
    parser.add_argument('--min_score', type=int, default=0.8, help="The minimum score triples should have to be accepted as true triples")
    parser.add_argument('--random_seed', type=int, default=142, help="Random seed for random entity selection for link prediction")
    parser.add_argument('--path_to_triples', type=str, default='./datasets/drkg/train.txt', help="Path to data triples")
    parser.add_argument('--entity_id_map', type=str, default='./embeddings/drkg_TransE/entity_to_ids.json', help="Entity name to id map, same as the one used during training")
    parser.add_argument('--relation_id_map', type=str, default='./embeddings/drkg_TransE/relation_to_ids.json', help="Relation name to id map, same as the one used during training")
    parser.add_argument('--store_triples', type=str2bool, const=True, default=True, nargs='?', help="Whether to store the newly predicted triples")
    args = parser.parse_args()
    link_predictor = LinkPredictor(args).get_suggested_triples().write_out_suggested_triples()