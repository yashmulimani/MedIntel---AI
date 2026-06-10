from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import easyocr

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

reader = easyocr.Reader(['en']) 

class ReportState(TypedDict):
    image_path: str
    extracted_text: str
    analysis: str

def extract_text(state: ReportState):
    result = reader.readtext(
        state["image_path"],
        detail=0
    )
    extracted_text = "\n".join(result)

    return {
        "extracted_text": extracted_text
    }

def analyze_report_node(state: ReportState):

    prompt = f"""
        You are MedIntel AI, an educational healthcare assistant.

        Analyze the following medical report.

        Provide:

        1. Summary
        2. Abnormal Findings
        3. Educational Interpretation
        4. Recommendations
        5. Disclaimer

        Do NOT diagnose diseases.
        Do NOT prescribe medicines.

        Medical Report:
        {state["extracted_text"]}
    """

    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }

graph = StateGraph(ReportState)

graph.add_node("extract_text", extract_text)
graph.add_node("analyze_report", analyze_report_node)

graph.add_edge(START, "extract_text")
graph.add_edge("extract_text", "analyze_report")
graph.add_edge("analyze_report", END)

workflow = graph.compile()

def analyze_medical_report(image_path: str):
    result = workflow.invoke(
        {
            "image_path": image_path
        }
    )

    return {
        "extracted_text": result["extracted_text"],
        "analysis": result["analysis"]
    }