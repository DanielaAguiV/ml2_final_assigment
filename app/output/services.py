import torch
from tweets import Tweet
from output.models import Model, Embedding, Tokenizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression


model = Model()
embedding = Embedding()
tokenizer = Tokenizer() 

class OutputService:
    
    """Clase que lleva a cabo los embeddings, escalamiento y reducción de dimensionalidad del tweet, para posteriormente
    realizar la predicción de tipo análisis de sentimiento"""
    
    @staticmethod
    def embed_tweet(tweet: Tweet):
        # Tokeniza el texto
      
        input_ids = torch.tensor([tokenizer.tokenizer.encode(tweet.value, add_special_tokens=True,max_length=250,truncation=True)])
        
        # Genera los embeddings
        with torch.no_grad():
            output = embedding.model_t(input_ids)
            embeddings = output[0][:, 0, :].numpy()
        return embeddings
    
    @staticmethod
    def scaler_function(tweet: Tweet):
        
        scaler = MinMaxScaler(feature_range=model.feature_range)
        scaler.data_min_ = model.data_min
        scaler.data_max_ = model.data_max
        scaler.data_range_ = model.data_range
        scaler.scale_ = model.scale
        scaler.min_ = model.min
        embed_tweet = OutputService.embed_tweet(tweet)
        
        return scaler.transform(embed_tweet)
    
    @staticmethod
    def dimensionality_reduction(tweet:Tweet):
        
        pca = PCA()
        pca.components_ = model.pca_components
        pca.mean_ = model.pca_mean
        embed_scaler_tweet = OutputService.scaler_function(tweet)
        
        return pca.transform(embed_scaler_tweet)
    
    @staticmethod
    def sentiment_prediction(tweet:Tweet):
        
        regression = LogisticRegression()
        regression.coef_ = model.logistic_weights
        regression.intercept_ = model.logistic_intercept
        regression.classes_ = model.clases
        
        final_tweet = OutputService.dimensionality_reduction(tweet)
        prediction = regression.predict(final_tweet)
        
        if prediction == 0:
            return 'negativo'
        elif prediction == 1:
            return 'neutro'
        elif prediction == 2:
            return 'positivo'

    
