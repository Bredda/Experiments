"""Runs endpoints.


"""

import json
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.models.base import ApiResponse
from api.models.run import Run

_cwd = Path.cwd()
_root = _cwd.parent
_output_dir = "runs"
_TARGET_DIR = _root / _output_dir
RUNS_DIR = Path(
    os.environ.get("EXPERIMENTS_RUNS_DIR", "runs")
).resolve()

router = APIRouter(prefix="/runs")

def _read_jsonl(path: Path):
    with (path).open(
            "r",
            encoding="utf-8",
        ) as file:
            data: list[dict] = [json.loads(line) for line in file]
            return data

def _read_json(path: Path):
    with (path).open(
            "r",
            encoding="utf-8",
        ) as file:
            data: dict = json.loads(file.read())
            return data

def list_runs():
    config_files =  _TARGET_DIR.glob("*/config.json")
    return [_read_json(f) for f in config_files]

@router.get("", response_model=ApiResponse[list[Run]])
async def get_runs() :
    print(list_runs())
    return {"data": list_runs()}

@router.get("/{run_id}", response_model=ApiResponse[Run])
async def get_run(run_id: str):
    run_path = _TARGET_DIR / run_id
    if not run_path.exists():
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    config_raw = _read_json(_TARGET_DIR / run_id / "config.json")
    run = Run.model_validate(config_raw)
    response = ApiResponse(data=run)
  
    return response
    

@router.get("/{run_id}/events")
async def get_run_events(run_id: str):
    run_path = _TARGET_DIR / run_id
    print(run_path)
    if not run_path.exists():
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    events = _read_jsonl(_TARGET_DIR / run_id /"events.jsonl")
    return {"data": events}

         