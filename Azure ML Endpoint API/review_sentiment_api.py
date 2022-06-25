from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from consume_hashingonly import get_review_sentiment

app = FastAPI()

class Reviews(BaseModel):
    reviews_list: list[str]

@app.post("/sentiment")
async def get_sentiments(reviews: Reviews):
    sentiments = []
    for review in reviews.reviews_list:
        sentiments.append(get_review_sentiment(review))
    return sentiments

if __name__ == '__main__':
    uvicorn.run("review_sentiment_api:app", port=8000, reload=False)