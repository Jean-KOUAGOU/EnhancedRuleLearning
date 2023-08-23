import os
map_model_to_folder = {'transe': 'TransAMIE', 'distmult': 'DistAMIE', 'rotate': 'RotAMIE'}
for kg in ['wn18rr', 'fb15k', 'carcinogenesis', 'mutagenesis', 'drkg', 'openbiolink', 'yago3']:
    print("Dataset: ", kg.upper())
    config_apply_path = f'data/AMIE/config-apply-{kg}.properties'
    config_eval_path = f'data/AMIE/config-eval-{kg}.properties'
    if not os.path.exists(f'data/AMIE/predictions_{kg}'):
        os.mkdir(f'data/AMIE/predictions_{kg}')
    with open(config_apply_path, 'w') as apply_file:
        apply_file.writelines([f'PATH_TRAINING  = data/datasets/{kg}/train.txt\n',
                               f'PATH_TEST      = data/datasets/{kg}/test.txt\n',
                               f'PATH_VALID     = data/datasets/{kg}/valid.txt\n',
                               f'PATH_RULES     = data/AMIE/rules_{kg}/anyburl-format\n',
                               f'PATH_OUTPUT    = data/AMIE/predictions_{kg}/predictions.txt\n',
                               'UNSEEN_NEGATIVE_EXAMPLES = 5\n',
                               'TOP_K_OUTPUT = 10\n',
                               'WORKER_THREADS = 7'])
    with open(config_eval_path, 'w') as eval_file:
        eval_file.writelines([f'PATH_TRAINING  = data/datasets/{kg}/train.txt\n',
                               f'PATH_TEST      = data/datasets/{kg}/test.txt\n',
                               f'PATH_VALID     = data/datasets/{kg}/valid.txt\n',
                               f'PATH_PREDICTIONS   = data/AMIE/predictions_{kg}/predictions.txt',
                               ])
    for model in ['transe', 'distmult', 'rotate']:
        folder = map_model_to_folder[model]
        if not os.path.exists(f'data/{folder}/predictions_{kg}'):
            os.mkdir(f'data/{folder}/predictions_{kg}')
        config_apply_path = f'data/{folder}/config-apply-{kg}.properties'
        config_eval_path = f'data/{folder}/config-eval-{kg}.properties'
        with open(config_apply_path, 'w') as apply_file:
            apply_file.writelines([f'PATH_TRAINING  = data/datasets/{kg}/train_completed_{model}_top5000.txt\n',
                                   f'PATH_TEST      = data/datasets/{kg}/test.txt\n',
                                   f'PATH_VALID     = data/datasets/{kg}/valid.txt\n',
                                   f'PATH_RULES     = data/{folder}/rules_{kg}/anyburl-format\n',
                                   f'PATH_OUTPUT    = data/{folder}/predictions_{kg}/predictions.txt\n',
                                   'UNSEEN_NEGATIVE_EXAMPLES = 5\n',
                                   'TOP_K_OUTPUT = 10\n',
                                   'WORKER_THREADS = 7'])
        with open(config_eval_path, 'w') as eval_file:
            eval_file.writelines([f'PATH_TRAINING  = data/datasets/{kg}/train_completed_{model}_top5000.txt\n',
                                   f'PATH_TEST      = data/datasets/{kg}/test.txt\n',
                                   f'PATH_VALID     = data/datasets/{kg}/valid.txt\n',
                                   f'PATH_PREDICTIONS   = data/{folder}/predictions_{kg}/predictions.txt',
                                   ])