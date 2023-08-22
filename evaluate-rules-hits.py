import argparse
map_model_to_folder = {'transe': 'TransAMIE', 'distmult': 'DistAMIE', 'rotate': 'RotAMIE'}

def execute(kgs, models, system):
    import os
    if system.lower() == 'amie':
        if models is not None:
            for model in models:
                folder = map_model_to_folder[model.lower()]
                path = f"data/{folder}/"
                print(f"Evaluating our system on link prediction from learned rules, KGE model: {model}")
                for kg in kgs:
                    if not os.path.exists(path+f'results_{kg}'):
                        os.mkdir(path+f'results_{kg}')
                    print("Dataset: ", kg.upper())
                    predictions_path = f"{path}predictions_{kg}/predictions.txt"
                    out_path = path+f'results_{kg}/results.txt'
                    config = f"{path}config-eval-{kg}.properties"
                    if os.path.isfile(out_path):
                        os.system(f'rm -f {out_path}')
                    os.system(f'java -Xmx12G -cp systems/AnyBURL-RE.jar de.unima.ki.anyburl.Eval {config} >> {out_path}')
                    with open(out_path) as file:
                        print(file.read())
        else:
            path = f"data/AMIE/"
            print(f"\n### Evaluating AMIE on original KGs ###\n")
            for kg in kgs:
                if not os.path.exists(path+f'results_{kg}'):
                    os.mkdir(path+f'results_{kg}')
                print("Dataset: ", kg.upper())
                predictions_path = f"{path}predictions_{kg}/predictions.txt"
                out_path = path+f'results_{kg}/results.txt'
                config = f"{path}config-eval-{kg}.properties"
                if os.path.isfile(out_path):
                    os.system(f'rm -f {out_path}')
                os.system(f'java -Xmx12G -cp systems/AnyBURL-RE.jar de.unima.ki.anyburl.Eval {config} >> {out_path}')
                with open(out_path) as file:
                    print(file.read())
    elif system == 'anyburl':
        path = f"data/AnyBURL/"
        print(f"\n### Evaluating AnyBURL on original KGs ###\n")
        for kg in kgs:
            if not os.path.exists(path+f'results_{kg}'):
                os.mkdir(path+f'results_{kg}')
            print("Dataset: ", kg.upper())
            predictions_path = f"{path}predictions_{kg}/predictions.txt"
            out_path = path+f'results_{kg}/results.txt'
            config = f"{path}config-eval-{kg}.properties"
            if os.path.isfile(out_path):
                os.system(f'rm -f {out_path}')
            os.system(f'java -Xmx12G -cp systems/AnyBURL-RE.jar de.unima.ki.anyburl.Eval {config} >> {out_path}')
            with open(out_path) as file:
                print(file.read())
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kgs', type=str, nargs='+', default=['wn18rr'], choices=['wn18rr', 'fb15k', 'carcinogenesis', 'mutagenesis', 'openbiolink', 'yago3', 'drkg'],\
                        help="Knowledge graph names")
    parser.add_argument('--system', type=str, default='amie', choices=['amie', 'AMIE', 'anyburl', 'AnyBURL', 'safran', 'SAFRAN'], help="System to execute")
    parser.add_argument('--models', type = str, nargs='+', default=None, choices=['TransE', 'Distmult', 'Rotate', 'transe', 'distmult', 'rotate'], help="Embedding model(s)")
    
    args = parser.parse_args()
    
    execute(args.kgs, args.models, args.system)
    