from pathlib import Path
import requests
import urllib
import os

# Get info about the latest release
latest_release = requests.get("http://api.semanticscholar.org/datasets/v1/release/latest").json()
print(latest_release['README'])
print(latest_release['release_id'])

# Get info about past releases
dataset_ids = requests.get("http://api.semanticscholar.org/datasets/v1/release").json()
earliest_release = requests.get(f"http://api.semanticscholar.org/datasets/v1/release/{dataset_ids[0]}").json()

# Print names of datasets in the release
print("\n".join(d['name'] for d in latest_release['datasets']))

# Print README for one of the datasets
print(latest_release['datasets'][2]['README'])

# Get info about the papers dataset
data = requests.get("http://api.semanticscholar.org/datasets/v1/release/latest/dataset/embeddings-specter_v2",
                      headers={'X-API-KEY':os.getenv("S2_API_KEY")}).json()

# Download the first part of the dataset
savepath = Path(__file__).parent / "data"
savepath.mkdir(exist_ok=True)
download = False
if download:
    from tqdm import tqdm
    for i, url in enumerate(tqdm(data['files'])):
        # Download the file
        urllib.request.urlretrieve(url, savepath / f"part_{i}.tar.gz")

# Extract the file
extract = False
if extract:
    import tarfile
    for i in range(1):
        with tarfile.open(f"part_{i}.tar.gz") as tar:
            tar.extractall(f"part_{i}")