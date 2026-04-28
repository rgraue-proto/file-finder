from pinecone import ServerlessSpec, Pinecone

pc = Pinecone(
    api_key="pclocal", 
    host="http://localhost:5081",
    ssl_verify=False
)

DENSE_INDEX = 'dense-index'

def describe_index(index_name=DENSE_INDEX):
    if not pc.has_index(DENSE_INDEX):
        pc.create_index(
            name=DENSE_INDEX,
            dimension=3072,
            metric='cosine',
            vector_type='dense',
            spec=ServerlessSpec(cloud='aws', region='us-west-2'),
            deletion_protection='disabled',
            tags={'env': 'dev'}
        )
    return pc.describe_index(name=index_name).host

def get_index_or_make(index_name=DENSE_INDEX):
    host = describe_index(index_name)

    return pc.Index(host=f'http://{host}', name=index_name)


index = get_index_or_make()
def upsert_embeding(id, value, meta):
    index.upsert(
        vectors=[
            {
                'id': id,
                'values': value,
                'metadata': meta
            }
        ],
        namespace='files'
    )

def query_index(vector):
    response = index.query(
        namespace="files",
        vector=vector,
        top_k=10,
        include_values=False,
        include_metadata=True
    )

    return response

