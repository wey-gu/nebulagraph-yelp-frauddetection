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
python3 download_data.py
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
    -v ./yelp_nebulagraph_importer.yaml:/root/importer.yaml \
    -v ./data/root \
    vesoft/nebula-importer:v3.1.0 \
    --config /root/importer.yaml
```
