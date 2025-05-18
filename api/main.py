import os
import openai
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

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
    except openai.error.OpenAIError as e:
        error_message = f"OpenAI API error in submit_code: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"Error in submit_code: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        # 파일 크기 검증 (예: 5MB 이하)
        max_file_size = 5 * 1024 * 1024  # 5MB
        if len(contents) > max_file_size:
            raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit")

        # 파일 형식 검증
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

        # Read Excel file
        df = pd.read_excel(contents)
        # Extract trade times from Excel
        if 'Trade Time' in df.columns:
            trade_times = df['Trade Time'].tolist()
        else:
            raise Exception("'Trade Time' column not found in Excel file")
        return {"filename": file.filename, "content_type": file.content_type, "trade_times": trade_times}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel file: {str(e)}")

# Mock function to get real-time coin data
def get_real_time_coin_data():
    try:
        api_key = os.getenv("COINBASE_API_KEY")
        api_secret = os.getenv("COINBASE_API_SECRET")
        headers = {
            'CB-ACCESS-KEY': api_key,
            'CB-ACCESS-SIGN': api_secret,
            'CB-ACCESS-TIMESTAMP': str(int(time.time())),
            'Content-Type': 'application/json'
        }
        response = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD', headers=headers)
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError as e:
            error_message = f"Invalid JSON response: {str(e)}"
            print(error_message)  # 콘솔에 에러 메시지 출력
            raise Exception(error_message)
        return data
    except requests.exceptions.RequestException as e:
        error_message = f"Request error in get_real_time_coin_data: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise Exception(error_message)
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP error in get_real_time_coin_data: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise Exception(error_message)
    except Exception as e:
        error_message = f"Error in get_real_time_coin_data: {str(e)}"
        print(error_message)  # 콘솔에 에러 메시지 출력
        raise Exception(error_message)

# Mock function to analyze trade history
def analyze_trade_history():
    try:
        # 실제 거래 내역 분석 로직을 여기에 추가
        # 예시: 거래 내역을 데이터베이스에서 가져와 분석
        trade_data = []  # 데이터베이스에서 가져온 거래 내역
        # 거래 내역 분석 로직
        analysis_result = "Analyzed trade history result"
        return analysis_result
    except Exception as e:
        raise Exception(f"Error in analyze_trade_history: {str(e)}")

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