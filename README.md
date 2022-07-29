## Dataset Intro

This data set was introduced by Dou et al. in [Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters](https://paperswithcode.com/paper/enhancing-graph-neural-network-based-fraud).

The data and paper's code could be found [here](https://github.com/YingtongDou/CARE-GNN), and here I cheated during the processing of data by leveraging [dgl](https://github.com/dmlc/dgl/tree/master/examples/pytorch/caregnn) to convert ajacency matrix to edgelist, and nodes with features & label.

Schema of the data:

- vertices: Yelp Reviews, with label(is_fruad) as a property and 32 normalized features as properties.
- edges: Relationship between reviews without property.
    - R-U-R: shares_user_with
    - R-S-R: shares_restaurant_rating_with
    - R-T-R: shares_restaurant_in_one_month_with

## Download and convert data into CSV

```bash
python3 -m pip install -r requirements.txt
python3 data_download.py
ls -l data/*.csv
```
Generated files:

```bash
$ ls data/*.csv
$

net_rsr.csv  net_rtr.csv  net_rur.csv  vertices.csv
```

## Import data into NebulaGraph

> Assuming that we boostrap a NebulaGraph with [Nebula-UP](https://github.com/wey-gu/nebula-up/).

```bash
docker run --rm -ti \
    --network=nebula-net \
    -v ${PWD}/yelp_nebulagraph_importer.yaml:/root/importer.yaml \
    -v ${PWD}/data:/root \
    vesoft/nebula-importer:v3.1.0 \
    --config /root/importer.yaml
```

After it's imported, we could query the stats of the graph:

```bash
~/.nebula-up/console.sh -e "USE yelp; SHOW STATS"
```
It should be like this:

```bash
(root@nebula) [(none)]> USE yelp; SHOW STATS
+---------+---------------------------------------+---------+
| Type    | Name                                  | Count   |
+---------+---------------------------------------+---------+
| "Tag"   | "review"                              | 45954   |
| "Edge"  | "shares_restaurant_in_one_month_with" | 1147232 |
| "Edge"  | "shares_restaurant_rating_with"       | 6805486 |
| "Edge"  | "shares_user_with"                    | 98630   |
| "Space" | "vertices"                            | 45954   |
| "Space" | "edges"                               | 8051348 |
+---------+---------------------------------------+---------+
Got 6 rows (time spent 1911/4488 us)
```

## NebulaGraph DGL Integration

> I know I don't have to do this as we have it in DGL dataset already, this is just a demo of how to use NebulaGraph with DGL.

```python
In [1]:
from nebula_dgl import NebulaLoader

nebula_config = {
    "graph_hosts": [
                ('graphd', 9669),
                ('graphd1', 9669),
                ('graphd2', 9669)
            ],
    "user": "root",
    "password": "nebula",
}

with open('nebulagraph_yelp_dgl_mapper.yaml', 'r') as f:
    feature_mapper = yaml.safe_load(f)

nebula_loader = NebulaLoader(nebula_config, feature_mapper)

g = nebula_loader.load()

# This will take a while

In [2]: g
Out[2]:
Graph(num_nodes={'review': 45954},
      num_edges={('review', 'shares_restaurant_in_one_month_with', 'review'): 1147232, ('review', 'shares_restaurant_rating_with', 'review'): 6805486, ('review', 'shares_user_with', 'review'): 98630},
      metagraph=[('review', 'review', 'shares_restaurant_in_one_month_with'), ('review', 'review', 'shares_restaurant_rating_with'), ('review', 'review', 'shares_user_with')])

In [3]: g.canonical_etypes
Out[3]:
[('review', 'shares_restaurant_in_one_month_with', 'review'),
 ('review', 'shares_restaurant_rating_with', 'review'),
 ('review', 'shares_user_with', 'review')]
```