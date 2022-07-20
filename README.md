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
