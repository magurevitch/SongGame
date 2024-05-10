from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers.DataViewer
import routers.ListAdder
import routers.Voter
import routers.Scorer
import routers.Admin

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://magurevitch.github.io/SongGame"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routers.DataViewer.router)
app.include_router(routers.ListAdder.router)
app.include_router(routers.Voter.router)
app.include_router(routers.Scorer.router)
app.include_router(routers.Admin.router)