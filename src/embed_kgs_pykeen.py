import json, argparse
from pykeen.pipeline import pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kgs', type=str, nargs='+', default=['drkg'], help="Knowledge graph names, should be in [drkg, wn18rr, carcinogenesis, ... (see folder datasets)]")
    parser.add_argument('--models', type = str, nargs='+', default=['TransE', 'Distmult', 'Rotate'], help="Embedding model(s)")
    parser.add_argument('--loss', type=str, default='mse', help="Loss to be used during training")
    parser.add_argument('--epochs', type=int, default=50, help="Number of training epochs")
    parser.add_argument('--random_seed', type=int, default=142, help="Random seed for model initialization")
    parser.add_argument('--dataset_kwargs', type=dict, default={'create_inverse_triples': False}, help="Dataset key arguments")
    args = parser.parse_args()
    for kg in args.kgs:
        print()
        print("#"*50)
        print("Embedding "+kg.upper()+" KG")
        print("#"*50)
        for model in args.models:
            print()
            print('*'*50)
            print(f'Training with {model}...')
            print('*'*50)
            result = pipeline(
                training="./data/datasets/"+kg+"/train.txt",
                testing="./data/datasets/"+kg+"/test.txt",
                model=model,
                optimizer='Adam',
                loss=args.loss,
                #epochs=args.epochs,
                training_kwargs=dict(num_epochs=args.epochs, batch_size=1024),
                random_seed=args.random_seed,
                dataset_kwargs=args.dataset_kwargs
            )
            storage_path = './data/embeddings/'+kg+'_'+model
            result.save_to_directory(storage_path)

            with open(storage_path+"/entity_to_ids.json", "w") as file:
                json.dump(result.training.entity_to_id, file, indent=3, ensure_ascii=False)
            with open(storage_path+"/relation_to_ids.json", "w") as file:
                json.dump(result.training.relation_to_id, file, indent=3, ensure_ascii=False)