# Initializing the embedding model.
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts


documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
model.save("/Users/wyx/Documents/Auto_Standard_Generator/VectorDatabase/embedding_model.model")
