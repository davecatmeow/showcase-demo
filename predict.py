import argparse
import sys
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Save the output predictions to file.",
                    nargs="?", type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument("modelfile", help="the model file for predictions, in csv format",
                    nargs="?", type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument(
    "csvfile", help="the input data file, in csv format", type=argparse.FileType('r'))

args = parser.parse_args()

df_centers = pd.read_csv(args.modelfile) # modelfile, the centers of clusters
df_data = pd.read_csv(args.csvfile) # datafile

if "labels" in df_centers.columns:
    df_centers["label"] = df_centers["labels"]
    df_centers = df_centers.drop(columns="labels")
df_centers["label"] = df_centers["label"].str.replace("center", "").str.strip()
df_centers.sort_values(by="label", inplace=True)
centers = df_centers.drop(columns="label").to_numpy()
label_index = df_centers["label"]

k, m = centers.shape
data = df_data.to_numpy()
n = data.shape[0]
distance = np.zeros([n, k])

# calculate distance and assign labels
for j, c in enumerate(centers):
    distance[:, j] = np.linalg.norm(data - c, axis=1)
new_labels = np.argmin(distance, axis=1)
df_labels = pd.Series(data=new_labels).map(label_index.to_dict()) # map labels from 0,...,k-1 to the provided label string

df_data["label"] = df_labels

origin_out = sys.stdout
# redirect the output
sys.stdout = args.output

print(df_data.to_csv(index = False))
