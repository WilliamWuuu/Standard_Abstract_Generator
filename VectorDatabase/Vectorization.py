from gensim.models.doc2vec import Doc2Vec

import re
import sys
from ltp import LTP

embedding_model = Doc2Vec.load('/Users/wyx/Documents/Auto_Standard_Generator/VectorDatabase/embedding_model.model')

class Vectorization:
    def __init__(self, **kwargs):
        
        self.text_pure = str
        self.tokens = []
        self.vector = []
        
        if kwargs:
            if 'filepath' in kwargs.keys():
                self.path = kwargs['filepath']
                self.flag = 'FILE'
            elif 'text' in kwargs.keys():
                self.text = kwargs['text']
                self.flag = 'TEXT'
            else:
                sys.exit("IOError: You seem to type in invalid arguments. Please try again.")
          
    def remove_punctuation(self):
        """
        Read and remove the punctuation from the given path.
        
        Args:
            filepath (str): Path to the file waiting to be converted into vector.
        """
        if self.flag == 'FILE':
            if self.path.endswith(".txt"):
                with open(self.path, 'r', encoding='utf-8') as file:
                    text = file.read().strip()
                self.text_pure = re.sub(r'[^\u4e00-\u9fa5\w\s]', '', text)
            else:
                sys.exit("Type Error: Only support <.txt> file to be converted to vector now!")
        
        elif self.flag == 'TEXT':
            self.text_pure = re.sub(r'[^\u4e00-\u9fa5\w\s]', '', self.text.strip())
            
        else:
            sys.exit("IOError: You seem to type in invalid arguments. Please try again.")

    def segmentation(self):
        """
        Apply segmentation to the pure text using ltp.
        """
        ltp = LTP()
        seg_result = ltp.pipeline([self.text_pure], tasks = ["cws"], return_dict = False)
        self.tokens = seg_result[0][0]

    def embedding(self):
        """
        Embed the tokens into vector using gensim.
        """
        self.vector = embedding_model.infer_vector(self.tokens)

        
    def vectorization(self):
        """
        Convert the object file into vector

        Returns:
            list: Vector 
        """
        self.remove_punctuation()
        self.segmentation()
        self.embedding()
        
        return self.vector
        
