from pydantic import BaseModel

class BMIRequest(BaseModel):
    weight: float
    height: float

class BMIResponse(BaseModel):
    bmi: float
    category: str
    advice: str