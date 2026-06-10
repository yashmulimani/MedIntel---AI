from pydantic import BaseModel

class ReportResponse(BaseModel):
    extracted_text: str
    analysis: str