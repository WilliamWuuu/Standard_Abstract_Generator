import os
import sys
import sqlite3
import faiss
import numpy as np

from Vectorization import Vectorization

class VectorDatabase:
    def __init__(self, db_path, dimension, **kwargs):
        """
        Initialize the database (with the given directory) and create required tables.
        
        Args:
            dp_path (str): Path to the database actually storing the data.
            embedding_model (gensim.models.doc2vec): The model used for embedding.
            dimension (int): The dimension of the stored vector.
        """
        self.db_path = db_path
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT,
                vector BLOB
            )
        ''')
        self.conn.commit()
        
        if kwargs: 
            if 'dir_path' in kwargs.keys() == False:
                sys.exit("IOError: You seem to type in invalid arguments. Please try again.")
                
            dir_path = kwargs['dir_path']
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                self.add(file_path)

    def add_vector(self, file_path):
        """
        Add a new vector to the database.
        
        Args:
            filepath (str): Path to the file waiting to be converted into vector and added to the database.
        """
        # Convert numpy array to binary data for SQLite storage
        vector = np.array(Vectorization(file_path), dtype=np.float32)
        vector_blob = vector.tobytes()
        self.cursor.execute('INSERT INTO vectors (filepath, vector) VALUES (?, ?)', (file_path, vector_blob))
        self.conn.commit()

    def _get_all_vectors(self):
        """
        Fetch all vectors from the database.
        """
        self.cursor.execute("SELECT id, vector FROM vectors")
        rows = self.cursor.fetchall()
        vectors = [(row[0], np.frombuffer(row[1], dtype=np.float32)) for row in rows]
        return vectors

    def load_faiss_index(self):
        """
        Load vectors from the database into the FAISS index.
        """
        vectors = self._get_all_vectors()
        if len(vectors) == 0:
            print("No vectors to load into FAISS.")
            return

        # Add vectors to the FAISS index
        ids, vecs = zip(*vectors)
        vecs_np = np.array(vecs, dtype=np.float32)
        self.index.add(vecs_np)

    def search_vector(self, query_vector, k=5):
        """
        Search for the k-nearest neighbors using FAISS.
        
        Args:
            query_vector (NDArray[floating[_32Bit]]): The searching target.
            k (int): The number of the nearest neighbor returned. 
        """
        if self.index.ntotal == 0:
            self.load_faiss_index()

        query_vector = np.array(query_vector, dtype=np.float32).reshape(1, -1)

        # Search using FAISS
        distances, indices = self.index.search(query_vector, k)
        
        # Retrieve the corresponding texts from the database using indices
        results = []
        for idx in indices[0]:
            if idx == -1:  
                continue
            self.cursor.execute('SELECT id, text FROM vectors WHERE id = ?', (idx + 1,))
            row = self.cursor.fetchone()
            if row:
                results.append({"id": row[0], "file_path": row[1], "distance": distances[0][idx]})

        return results

    def remove_vector_by_id(self, vector_id):
        """
        Remove a vector from the database by its ID.
        
        Args:
            vector_id (int): The id of the target vector.
        """
        self.cursor.execute('DELETE FROM vectors WHERE id = ?', (vector_id,))
        self.conn.commit()

    def get_vector_by_id(self, vector_id):
        """
        Fetch a vector and its corresponding text from the database by ID.
        
        Args:
            vector_id (int): The id of the target vector.
        """
        self.cursor.execute('SELECT id, text, vector FROM vectors WHERE id = ?', (vector_id,))
        row = self.cursor.fetchone()
        if row:
            vector = np.frombuffer(row[2], dtype=np.float32)
            return {"id": row[0], "text": row[1], "vector": vector}
        return None

    def list_vectors(self):
        """
        List all vectors currently stored in the database.
        """
        self.cursor.execute('SELECT id, text FROM vectors')
        return self.cursor.fetchall()

    def __del__(self):
        """
        Close the database connection on deletion of the object.
        """
        self.conn.close()