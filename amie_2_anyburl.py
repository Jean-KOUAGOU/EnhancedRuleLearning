#!/usr/bin/env/python
import argparse
import os

map_model_to_folder = {'transe': 'TransAMIE', 'distmult': 'DistAMIE', 'rotate': 'RotAMIE'}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kgs', type=str, nargs='+', default=['wn18rr'], choices=['wn18rr', 'fb15k', 'carcinogenesis', 'mutagenesis', 'openbiolink', 'yago3', 'drkg'],\
                        help="Knowledge graph names")
    parser.add_argument('--models', type = str, nargs='+', default=None, choices=['TransE', 'Distmult', 'Rotate', 'transe', 'distmult', 'rotate'], help="Embedding model(s)")
    args = parser.parse_args()
    for kg in args.kgs:
        if args.models is not None:
            for model in args.models:
                folder = map_model_to_folder[model.lower()]
                in_path = f"data/{folder}/rules_{kg}/rules_top5000.txt"
                out_path = f"data/{folder}/rules_{kg}/anyburl-format"
                os.system(f"python systems/SAFRAN/python/amie_2_anyburl.py --from {in_path} --to {out_path}")
        else:
            folder = "AMIE"
            in_path = f"data/{folder}/rules_{kg}/rules.txt"
            out_path = f"data/{folder}/rules_{kg}/anyburl-format"
            os.system(f"python systems/SAFRAN/python/amie_2_anyburl.py --from {in_path} --to {out_path}")