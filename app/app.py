from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tweets import TweetTransformations as TT
from tweets import Tweet
from output import OutputService as OS
from tweets.exceptions import  NullTweet


class TweetString(BaseModel):
    value: str

app = FastAPI()

#----------------------------------------------------#

@app.post("/predict/")
async def predict(tweet_string: TweetString):
    
    if len(tweet_string.value) == 0:
        raise HTTPException(status_code=400, detail="Tweet Vacío")
    
    value =  Tweet(tweet_string.value)
    print(value)
    transformations = TT()
    output_service = OS()
    lemma_tweet = transformations.transform_tweets(value)
    prediction = output_service.sentiment_prediction(lemma_tweet)
    
    return {"status": 200, "tweet_transformado": lemma_tweet.value, "prediction": prediction}
    
