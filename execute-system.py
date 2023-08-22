import argparse
map_model_to_folder = {'transe': 'TransAMIE', 'distmult': 'DistAMIE', 'rotate': 'RotAMIE'}
    
def execute(kgs, models, system):
    import os
    if system.lower() == 'amie':
        if models is not None:
            for model in models:
                folder = map_model_to_folder[model.lower()]
                path = f"data/{folder}/"
                for topk in [50, 500, 5000]:
                    print(f"\n### Running AMIE with top{topk} added triples... ###\n")
                    for kg in kgs:
                        if not os.path.exists(path+f'rules_{kg}'):
                            os.mkdir(path+f'rules_{kg}')
                        print("Dataset: ", kg.upper())
                        train_path = f"data/datasets/{kg}/train_completed_{model.lower()}_top{topk}.txt"
                        out_path = path+f'rules_{kg}/rules_top{topk}.txt'
                        if os.path.isfile(out_path):
                            os.system(f'rm -f {out_path}')
                        os.system(f'java -jar systems/amie-dev.jar {train_path} >> {out_path}')
        else:
            path = f"data/AMIE/"
            print(f"\n### Running AMIE on original KGs ###\n")
            for kg in kgs:
                if not os.path.exists(path+f'rules_{kg}'):
                    os.mkdir(path+f'rules_{kg}')
                print("Dataset: ", kg.upper())
                train_path = f"data/datasets/{kg}/train.txt"
                out_path = path+f'rules_{kg}/rules.txt'
                if os.path.isfile(out_path):
                    os.system(f'rm -f {out_path}')
                os.system(f'java -jar systems/amie-dev.jar {train_path} >> {out_path}')
    else:
        path = f"data/AnyBURL/"
        print(f"\n### Running AnyBURL on original KGs ###\n")
        for kg in kgs:
            if not os.path.exists(path+f'rules_{kg}'):
                os.mkdir(path+f'rules_{kg}')
            print("Dataset: ", kg.upper())
            
            config = f"data/AnyBURL/config-learn-{kg}.properties"
            os.system(f'java -Xmx12G -cp systems/AnyBURL-RE.jar de.unima.ki.anyburl.LearnReinforced {config}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kgs', type=str, nargs='+', default=['wn18rr'], choices=['wn18rr', 'fb15k', 'carcinogenesis', 'mutagenesis', 'openbiolink', 'yago3', 'drkg'],\
                        help="Knowledge graph names")
    parser.add_argument('--system', type=str, default='amie', choices=['amie', 'AMIE', 'anyburl', 'AnyBURL'], help="System to execute")
    parser.add_argument('--models', type = str, nargs='+', default=None, choices=['TransE', 'Distmult', 'Rotate', 'transe', 'distmult', 'rotate'], help="Embedding model(s)")
    
    args = parser.parse_args()
    
    execute(args.kgs, args.models, args.system)
    
    
