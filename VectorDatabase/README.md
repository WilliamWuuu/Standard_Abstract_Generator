# Vector Database Designed For LLM

This directory contains the code for our **Vector Database** specially designed for storing the knowledge of large language models.

Thanks **facebookresearch** for providing the excellent algorithms that search in sets of vectors. 
- 🔗link: <https://github.com/facebookresearch/faiss>

Thanks **HIT-SCIR** for providing the nice NLP tools.
- 🔗link: <https://github.com/HIT-SCIR/ltp>

## Update Log
- [x] [2024.9.24] Upload the first draft of the database, narrowly realising functions like initialize, add_vector, search_vector, etc. 
- [x] [2024.10.2] Upload the *EmbeddingModel.py* to initialize the *gensim.Doc2Vec* model.
- [x] [2024.11.29] Optimize the *Vectorization* class and make it more descent in calling the *ltp.small* model. 
- [x] [2024.12.4] Upload the *requirements.txt*.

## How to use
Build the environment with the dependencies first.

``` Bash
cd VectorDatabase
pip install -r requirements.txt
```

If the installation process works out fine, let's jump into the actual practice.

Let's say if the object *message* stores the summary of the standard text that user wants to generate. You can run the following code to search the relevant knowledge in the database.

``` Python
import VectorDatabase

# load the database
database = VectorDatabase('./vectorDB.db', 64)

# search the relevant knowledge in the database
search_result = database.search_vector(message, k=5)

# Judge the closest result by its distance to the query.
# If it is closest enough, use the standard text corresponding file_path
for result in search_result:
    valid = False
    if result["distance"] < 1e-5:
        file_path = result["file_path"]
        
        if file_path.endswith(".txt"):
            valid = True

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            break

if valid == True:
    # Just return text
else:
    # Deliver the user message to large language model and you know what to do.
```

After that, you may want to store the summary returned by the llm. Assume it is stored in the object *result*

``` Python
import VectorDatabase

# load the database
database = VectorDatabase('./vectorDB.db', 64)

# add the model response to the database
database.add_vector(text=result)

```

If you want to know more of the functions of the database, check them out in the class file. ^_^