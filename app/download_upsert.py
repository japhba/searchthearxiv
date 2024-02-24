# %%

from pathlib import Path
import requests
import urllib
import os

from helpers import SRC_ROOT

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

savepath = Path(SRC_ROOT) / "data"
savepath.mkdir(exist_ok=True)

print(data)

file_urls = data['files'][:1]

# %%
# Download the first part of the dataset
from tqdm import tqdm
for i, url in enumerate(tqdm(file_urls)):
    # Download the file
    pass
    # urllib.request.urlretrieve(url, savepath / f"part_{i}.gz")





# example_data_generator = map(lambda i: (f'id-{i}', [random.random() for _ in range(vector_dim)]), range(vector_count))

# %%
import gzip
import json
from pathlib import Path
from itertools import chain


def data_generator(i):
    file_path = savepath / f"part_{i}.gz"
    with gzip.open(file_path, 'rt') as file:  # 'rt' mode for text mode reading
        for line in file:
            yield process_line(line)

def process_line(line):
    entry_dict = json.loads(line)
    id = str(entry_dict['corpusid'])
    vector = json.loads(entry_dict['vector'])
    elem = (id, vector)
    return elem

# Create a list of individual file generators
generators = [data_generator(i) for i in range(10)]

# Use itertools.chain to create a single stream from all generators
total_generator = chain(*generators)

# Test data generator
try:
    print(next(total_generator))
except StopIteration:
    print("No more data.")


# %% 
import random
import itertools
from pinecone import Pinecone, ServerlessSpec
import os

vector_dim = 768
vector_count = 10000

# Initialize the client with pool_threads=30 (limits to 30 simultaneous requests)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"], pool_threads=30)
pc.create_index(
    name="specter-2",
    dimension=vector_dim,
    metric="cosine",
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-west-2'
    ) 
) 

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))




# Upsert data with 100 vectors per upsert request asynchronously
# - Pass async_req=True to index.upsert()
with pc.Index('specter-2', pool_threads=30) as index:
    # Send requests in parallel
    async_results = [
        index.upsert(vectors=ids_vectors_chunk, async_req=True)
        for ids_vectors_chunk in chunks(total_generator, batch_size=100)
    ]
    # Wait for and retrieve responses (this raises in case of error)
    [async_result.get() for async_result in async_results]
# %%
