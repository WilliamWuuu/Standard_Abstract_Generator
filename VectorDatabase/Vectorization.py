import re
import sys
from ltp import LTP

class Vectorization:
    def __init__(self, filepath, embedding_model):
        self.path = filepath
        self.model = embedding_model
        self.text_pure = str
        self.tokens = []
        self.vector = []
        
    # 去除标点符号    
    def remove_punctuation(self):
        """
        Read and remove the punctuation from the given path.
        
        Args:
            filepath (str): Path to the file waiting to be converted into vector.
        """
        if self.path.endswith(".txt"):
            with open(self.path, 'r', encoding='utf-8') as file:
                text = file.read().strip()
            self.text_pure = re.sub(r'[^\u4e00-\u9fa5\w\s]', '', text)
        else:
            sys.exit("Type Error: Only support <.txt> file to be converted to vector now!")

    # 进行分词
    def segmentation(self):
        """
        Apply segmentation to the pure text using ltp.
        """
        ltp = LTP()
        seg_result = ltp.pipeline([self.text_pure], tasks = ["cws"], return_dict = False)
        self.tokens = seg_result[0][0]

    # embedding
    def embedding(self):
        """
        Embed the tokens into vector using gensim.
        """
        self.vector = self.model.infer_vector(self.tokens)
        
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
        
