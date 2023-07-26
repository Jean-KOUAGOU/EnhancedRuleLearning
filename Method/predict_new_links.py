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
    parser.add_argument('--models', type=str, nargs='+', default=['transe'], choices=['transe', 'distmult', 'rotate'], help="The embedding model used, e.g. TransE")
    parser.add_argument('--kgs', type=str, nargs='+', default=['drkg'], help="The knowledge graph name")
    parser.add_argument('--target_relations', type=str, nargs='+', default=[], help="Relation names to use for link prediction")
    parser.add_argument('--num_entities', type=int, default=1000, help="The number of entities to select")
    parser.add_argument('--random_seed', type=int, default=142, help="Random seed for random entity selection for link prediction")
    parser.add_argument('--num_relations', type=int, default=10, help="The maximum number of relations to use in case none was given")
    parser.add_argument('--topk_triples', type=int, default=50, help="Top 50 highest scoring triples")
    parser.add_argument('--store_triples', type=str2bool, const=True, default=False, nargs='?', help="Whether to store the newly predicted triples")
    args = parser.parse_args()
    for kg in args.kgs:
        for model in args.models:
            link_predictor = LinkPredictor(kg, model, args).get_suggested_triples().write_out_suggested_triples()