import os.path
import json
import numpy as np
import pandas as pd
from tqdm import tqdm


def load_graph_data(file_path):
    try:
        graphs = np.load(file_path, allow_pickle=True)['graph_dict'].item()
    except UnicodeError:
        graphs = np.load(file_path, allow_pickle=True, encoding='latin1')['graph_dict'].item()
        graphs = { k.decode() : v for k, v in graphs.items() }
    return graphs


def validate_graph(graph_path, official_graph_path):
    graphs = load_graph_data(graph_path)
    official_graphs = load_graph_data(official_graph_path)

    if len(graphs) != len(official_graphs):
        print('The graph data sizes are different!')
        return 1

    print('Validating graphs...')
    for key in tqdm(official_graphs.keys()):
        if graphs[key] != official_graphs[key]:
            print('A mismatch was found! The validation process stops here.')
            print(key)
            print(graphs[key])
            print(official_graphs[key])
            return 1
    
    print('Your graph data was validated.')
    return 0


def _isclose(a, b):
    return np.isclose(a, b, rtol=1e-15, atol=1e-15, equal_nan=False)


def validate_targets(csv_path, official_csv_path):
    df = pd.read_csv(csv_path, na_filter=False)
    df_official = pd.read_csv(official_csv_path, na_filter=False)

    float_columns = [ 'volume_per_atom', 'volume_deviation' ]

    mismatches = []
    for col in df_official.columns:
        if col in float_columns:
            if not all(_isclose(df[col], df_official[col])):
                print(col)
                mismatches.append(col)
        else:
            if not all(df[col] == df_official[col]):
                print(col)
                mismatches.append(col)

    for col in mismatches:
        official_col = 'official_'+col
        summary = pd.DataFrame({
            'name': df.name,
            'formula': df.formula,
            col: df[col],
            official_col: df_official[col],
        })
        if col in float_columns:
            summary = summary[_isclose(summary[col], summary[official_col])]
        else:
            summary = summary[summary[col] != summary[official_col]]
        print(summary)
        save_path = f'/tmp/{col}.csv'
        summary.to_csv(save_path)
        print(f'Saved to: {save_path}')
    
    if len(mismatches) == 0:
        print('Your targets data was validated.')
    else:
        print('Your targets data has mismatches.')


def validate_config(config_path, official_config_path):
    with open(config_path) as f:
        config = json.load(f)
    
    with open(official_config_path) as f:
        official_config = json.load(f)
    
    if config == official_config:
        print('Your config data was validated.')
    else:
        print('Your config data has mismatches.')


def validate_split(split_path, official_split_path):
    with open(split_path) as f:
        split = json.load(f)
    
    with open(official_split_path) as f:
        official_split = json.load(f)
    
    if split == official_split:
        print('Your split data was validated.')
    else:
        print('Your split data has mismatches.')


def main(dataset_path, official_dataset_path):
    validate_graph(
        graph_path=os.path.join(dataset_path, 'graph_data.npz'),
        official_graph_path=os.path.join(official_dataset_path, 'graph_data.npz')
    )
    
    validate_targets(
        csv_path=os.path.join(dataset_path, 'targets.csv'),
        official_csv_path=os.path.join(official_dataset_path, 'targets.csv')
    )

    validate_config(
        config_path=os.path.join(dataset_path, 'config.json'),
        official_config_path=os.path.join(official_dataset_path, 'config.json')
    )

    validate_split(
        split_path=os.path.join(dataset_path, 'split.json'),
        official_split_path=os.path.join(official_dataset_path, 'split.json')
    )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validator for the OQMD v1.2 dataset.')
    parser.add_argument('--dataset_path', metavar='PATH', type=str, default='.',
                        help='The path to your dataset directory (default: the current directory)')
    parser.add_argument('--official_dataset_path', metavar='PATH', type=str, default='oqmd_dataset',
                        help='The path to an official dataset directory (default: oqmd_dataset)')
    options = vars(parser.parse_args())

    main(**options)
