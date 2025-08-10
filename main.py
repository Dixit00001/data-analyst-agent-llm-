from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from pipeline import run_pipeline
import tempfile, shutil

app = FastAPI(title="LLM-Powered Data Analyst Agent")

@app.post("/api/")
async def api_endpoint(
    questions: UploadFile = File(...),
    files: List[UploadFile] = []
):
    try:
        # save uploaded files to temp dir
        workdir = tempfile.mkdtemp()
        q_path = f"{workdir}/{questions.filename}"
        with open(q_path, "wb") as f:
            f.write(await questions.read())

        file_paths = []
        for f in files:
            fpath = f"{workdir}/{f.filename}"
            with open(fpath, "wb") as out:
                out.write(await f.read())
            file_paths.append(fpath)

        # run multi-LLM pipeline
        result = run_pipeline(q_path, file_paths)

        shutil.rmtree(workdir)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
