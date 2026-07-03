import os
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

if os.path.exists("config.development.yaml"):
    with open("config.development.yaml") as f:
        data = yaml.safe_load(f) or {}
        config.update(data)

mapping = {
    "APP_PORT": "port",
    "NUM_WORKERS": "workers",
    "APP_DEBUG": "debug",
    "APP_LOG_LEVEL": "log_level",
    "APP_API_KEY": "api_key",
}

def to_bool(v):
    return str(v).lower() in ("true","1","yes","on")

for env, key in mapping.items():
    val = os.getenv(env)
    if val is None:
        continue
    if key in ("port","workers"):
        config[key] = int(val)
    elif key == "debug":
        config[key] = to_bool(val)
    else:
        config[key] = val

@app.get("/")
def home():
    return {"status":"ok"}

@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    result = config.copy()

    for item in set:
        if "=" in item:
            k,v = item.split("=",1)
            if k in ("port","workers"):
                result[k] = int(v)
            elif k=="debug":
                result[k] = to_bool(v)
            else:
                result[k]=v

    result["api_key"]="****"
    return result
