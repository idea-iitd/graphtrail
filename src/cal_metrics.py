from pickle import load
from sklearn.metrics import classification_report
import torch
from torch_geometric import datasets

DATASETS = ["BAMultiShapesDataset", "MUTAG", "Mutagenicity", "NCI1"]
ARCHS = ["GAT", "GCN", "GIN"]
POOLS = ["add", "max", "mean"]
SIZES = [0.05, 0.25, 0.5, 0.75, 1.0]

DATASETS = ["MUTAG"]
ARCHS = ["GAT"]
POOLS = ["add"]
SIZES = [1.0]
sample = 1.0 # Use ctrees and shapley values from this split of the training set.

for name in DATASETS:
    if name in ["MUTAG", "Mutagenicity", "NCI1"]:
        dataset = datasets.TUDataset(root=f"../data/", name=name)
    elif name == "BAMultiShapesDataset":
        dataset = datasets.BAMultiShapesDataset(root=f"../data/{name}")
    else:
        print("Invalid dataset")
        exit(1)
    ground_truth = dataset.y
    for arch in ARCHS:
        for pool in POOLS:
            for size in SIZES:
                if name == "NCI1":
                    SEEDS = [45, 1225, 1983]
                else:
                    SEEDS = [45, 357, 796]
                for seed in SEEDS:
                    folder = f"../data/{name}/{arch}/{pool}/{size}/{seed}"

                    file_test_indices = f"{folder}/test_indices.pkl"
                    with open(file_test_indices, "rb") as file:
                        test_indices = load(file)

                    try:
                        # gnn_train_pred = torch.load(f"{folder}/gnn_train_pred.pt")
                        # pysr_train_pred = torch.load(f"{folder}/pysr_train_pred_sample{sample}.pt")

                        gnn_test_pred = torch.load(f"{folder}/gnn_test_pred.pt")
                        pysr_test_pred = torch.load(f"{folder}/pysr_test_pred_sample{sample}.pt")
                    except FileNotFoundError:
                        print(">>>", folder)
                        print("FileNotFound")
                        continue

                    print(">>>", folder)

                    # print("--- Train")
                    # print("gnn_train_pred:",  torch.unique(gnn_train_pred,  return_counts=True))
                    # print("pysr_train_pred:", torch.unique(pysr_train_pred, return_counts=True))
                    # print(classification_report(y_true=gnn_train_pred, y_pred=pysr_train_pred))

                    print("--- Test")
                    print("gnn_test_pred:", torch.unique(gnn_test_pred,  return_counts=True))
                    print("gnn_test_pred:", torch.unique(pysr_test_pred, return_counts=True))
                    print(classification_report(y_true=gnn_test_pred,  y_pred=pysr_test_pred))

                    print("--- Ground truth")
                    ground_truth_test = ground_truth[test_indices]
                    print(classification_report(y_true=ground_truth_test,  y_pred=pysr_test_pred))
