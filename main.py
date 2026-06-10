from fastapi import FastAPI
from fastapi import (UploadFile, File)
import shutil
import os


from agents.chatbot import get_chat_response
from agents.bmi_agent import get_bmi_report
from agents.report_analyzer import (analyze_medical_report)

from schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)
from schemas.bmi_schema import (
    BMIRequest,
    BMIResponse
)
from schemas.report_schema import (
    ReportResponse
)

app = FastAPI(title="MedIntel API", version="1.0.0")

@app.get("/")
def home():
    return {"message": "Welcome to MedIntel API"}

@app.post("/chat", response_model = ChatResponse)
def chat(request: ChatRequest):
    response = get_chat_response(
        message = request.message,
        thread_id = request.thread_id
    )

    return ChatResponse(response=response)

@app.post("/bmi", response_model = BMIResponse)
def bmi(request: BMIRequest):
    result = get_bmi_report(
        weight=request.weight,
        height=request.height
    )

    return BMIResponse(
        bmi=result["bmi"],
        category=result["category"],
        advice=result["advice"]
    )

@app.post("/analyze-report", response_model=ReportResponse)
async def analyze_report(file: UploadFile = File(...)):
    os.makedirs(
        "reports",
        exist_ok=True
    )
    file_path = os.path.join(
        "reports",
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = analyze_medical_report(file_path)

    return ReportResponse(
        extracted_text=result["extracted_text"],
        analysis=result["analysis"]
    )