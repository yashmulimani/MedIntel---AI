from pydantic import BaseModel, Field
from typing import List, Literal


class HealthcareResponse(BaseModel):

    summary: str = Field(
    description="""
        Provide a detailed explanation (3–5 sentences)
        about the user's symptoms, possible implications,
        and general healthcare guidance without diagnosing.
    """
    )   

    possible_causes: List[str] = Field(
    description="""
        List 3–5 possible causes of the symptoms without making a diagnosis.
    """
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "emergency"
    ] = Field(description="""
        Determine the severity level:

        low → mild symptoms,
        medium → persistent symptoms,
        high → significant symptoms requiring prompt medical attention,
        emergency → symptoms requiring immediate medical care.
        """
    )

    recommendations: List[str] = Field(
    description="""
        Provide 4–6 practical healthcare recommendations
        focused on self-care and seeking professional advice.
        Do not recommend medications.
    """
    )

    warning_signs: List[str] = Field(
    description="""
        List warning signs that indicate urgent medical evaluation is needed.
    """
    )

    emergency: bool = Field(
    description="""
        Return ONLY a JSON boolean.

        Use:
        true → emergency medical attention required.

        false → emergency medical attention not immediately required.

        Never return this field as a string.
    """
    )   

    disclaimer: str