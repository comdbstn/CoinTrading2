import os
import openai
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class TradingCode(BaseModel):
    code: str

@app.post("/submit-code/")
async def submit_code(trading_code: TradingCode):
    try:
        # Compare trade times with current code logic
        comparison_result = "Comparison result between code and trade times"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze and optimize the following trading code: {trading_code.code}. {comparison_result}",
            max_tokens=150
        )
        return {"message": "Code received", "optimized_code": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting code: {str(e)}")

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        # Read Excel file
        df = pd.read_excel(contents)
        # Extract trade times from Excel
        trade_times = df['Trade Time'].tolist()  # Assuming 'Trade Time' is a column in the Excel file
        return {"filename": file.filename, "content_type": file.content_type, "trade_times": trade_times}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Excel file")

# Mock function to get real-time coin data
def get_real_time_coin_data():
    return {"BTC": 50000, "ETH": 4000}  # Example data

# Mock function to analyze trade history
def analyze_trade_history():
    return "Trade history analysis result"

@app.get("/coin-data/")
async def coin_data():
    try:
        data = get_real_time_coin_data()
        return {"data": data}  # JSON 형식으로 반환
    except Exception as e:
        error_message = f"Error fetching coin data: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/trade-history/")
async def trade_history():
    try:
        result = analyze_trade_history()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 