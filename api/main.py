import os
import openai
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class TradingCode(BaseModel):
    code: str

@app.post("/submit-code/")
async def submit_code(trading_code: TradingCode):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze and optimize the following trading code: {trading_code.code}",
        max_tokens=150
    )
    return {"message": "Code received", "optimized_code": response.choices[0].text.strip()}

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # 엑셀 파일 처리 로직 추가
    return {"filename": file.filename, "content_type": file.content_type} 