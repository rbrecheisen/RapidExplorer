from fastapi import FastAPI


app = FastAPI()


@app.get('/api/items/{itemId}')
async def getItem(itemId: str):
    return {'itemId': itemId}
