import chromadb
import pandas as pd


# Define the path where the database will be stored
DB_PATH = "RAG/chroma_db_doctors"

# Initialize the persistent client with the specified path
client = chromadb.PersistentClient(path=DB_PATH)

# Create a new collection (or get it if it already exists)
collection = client.get_or_create_collection(name="Doctors_Database")

df = pd.read_csv(r'RAG\doctors_data.csv')
df['combined'] = df.apply(lambda row: ' '.join(row.astype(str)), axis=1)
list_of_dicts = df.to_dict(orient='records')


ids = []
metadatas = []
documents = []

for idx, dta in enumerate(list_of_dicts):
    documents.append(dta['combined'])
    ids.append(str(idx))
    metadatas.append({'Metadata': str(dta)})


collection.add(
    ids = ids,
    documents = documents,
    metadatas = metadatas
)