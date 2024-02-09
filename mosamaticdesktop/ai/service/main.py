from fastapi import FastAPI

app = FastAPI()

@app.get('/items/{itemId}')
async def getItem(itemId: int):
    return {'itemId': itemId}
