import h5py
import torch

class Model:
    
    """Clase que inyecta a la aplicación el modelo"""
    
    def __init__(self) -> None:
        
        model_path = './models/modelo1.h5'
        
        with h5py.File(model_path, 'r') as hf:
            self.pca_components = hf['pca_components'][:]
            self.pca_mean = hf['pca_mean'][:]
            self.logistic_weights = hf['logistic_weights'][:]
            self.logistic_intercept = hf['logistic_intercept'][:]
            self.clases = hf['classes'][:]
            self.grupo_scaler = hf['scaler']
            # Obtiene los atributos del scaler del grupo
            self.data_min = self.grupo_scaler.attrs['data_min']
            self.data_max = self.grupo_scaler.attrs['data_max']
            self.data_range = self.grupo_scaler.attrs['data_range']
            self.feature_range = self.grupo_scaler.attrs['feature_range']
            self.scale = self.grupo_scaler.attrs['scale']
            self.min = self.grupo_scaler.attrs['min']
        

class Embedding:
    
    """Clase que inyecta a la aplicación los Embeddings"""
    
    def __init__(self) -> None:
        embedding_path = './models/modelo_t.pt'
        self.model_t = torch.load(embedding_path)

class Tokenizer:
    
    """Clase que inyecta a la aplicación el tokenizador de palabras"""
    
    def __init__(self) -> None:
        tokenizer_path = './models/tokenizador.pt'
        self.tokenizer = torch.load(tokenizer_path)
