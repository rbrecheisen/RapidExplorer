from fastapi import FastAPI


app = FastAPI()
"""
GET     /api/tasks/             Returns list of task instances
POST    /api/tasks/             Create new task instance
GET     /api/tasks/{taskId}     Returns task status
PATCH   /api/tasks/{taskId}     Updates task status
DELETE  /api/tasks/{taskId}     Deletes task
"""


@app.get('/api/tasks/')
async def getTasks():
    return {'tasks': []}
