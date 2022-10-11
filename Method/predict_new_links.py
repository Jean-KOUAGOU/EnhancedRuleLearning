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
    parser.add_argument('--model', type=str, default='TransE', help="The embedding model used, e.g. TransE")
    parser.add_argument('--kg', type=str, default='drkg', help="The knowledge graph name")
    parser.add_argument('--target_relations', nargs='+', default=[], help="Relation names to use for link prediction")
    parser.add_argument('--max_num_entities', type=int, default=100, help="The maximum number of entities to select")
    parser.add_argument('--min_score', type=float, default=0.8, help="The minimum score triples should have to be accepted as true triples")
    parser.add_argument('--random_seed', type=int, default=142, help="Random seed for random entity selection for link prediction")
    parser.add_argument('--max_num_relations', type=int, default=10, help="The maximum number of relations to use in case none was given")
    parser.add_argument('--store_triples', type=str2bool, const=True, default=True, nargs='?', help="Whether to store the newly predicted triples")
    args = parser.parse_args()
    link_predictor = LinkPredictor(args).get_suggested_triples().write_out_suggested_triples()