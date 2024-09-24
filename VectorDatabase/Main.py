from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile, common_texts

from VectorDatabase import VectorDatabase

# 创建 Doc2Vec 模型
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

# 保存模型到临时文件并加载
fname = get_tmpfile("my_doc2vec_model")
model.save(fname)
model = Doc2Vec.load(fname)

myVectorDatabase = VectorDatabase("vector_database.db", model, 64)