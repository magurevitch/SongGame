from fastapi import FastAPI

import routers.DataViewer
import routers.ListAdder
import routers.Voter
import routers.Scorer

app = FastAPI()
app.include_router(routers.DataViewer.router)
app.include_router(routers.ListAdder.router)
app.include_router(routers.Voter.router)
app.include_router(routers.Scorer.router)