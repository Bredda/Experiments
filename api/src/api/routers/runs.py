"""Runs endpoints.


"""

from pathlib import Path
from fastapi import APIRouter
import json
import os
from os import listdir
from os.path import isfile, join
from fastapi import HTTPException

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

def _list_folders(path: Path):
    return [f for f in listdir(path) if not isfile(join(path, f))]


@router.get("")
async def get_runs() :
    runs = _list_folders(_TARGET_DIR)
    return {"runs": runs}

@router.get("/{run_id}")
async def get_run(run_id: str):
    run_path = _TARGET_DIR / run_id
    if run_path.exists:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    config = _read_json(_TARGET_DIR / run_id / "config.json")
    return {**config}
    

@router.get("/{run_id}/events")
async def get_run_events(run_id: str):
    run_path = _TARGET_DIR / run_id
    if run_path.exists:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    events = _read_jsonl(_TARGET_DIR / run_id /"events.jsonl")
    return {"run_id": run_id, "events": events}

         