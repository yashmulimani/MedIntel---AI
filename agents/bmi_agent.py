from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

class BMIState(TypedDict):
    weight: float
    height: float
    bmi: Optional[float]
    category: Optional[str]
    advice: Optional[str]

@tool
def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI."""
    return round(weight / (height ** 2), 2)

def bmi_node(state: BMIState):
    bmi = calculate_bmi.invoke(
        {
            "weight": state["weight"],
            "height": state["height"]
        }
    )

    return {
        "bmi": bmi
    }

def interpretation_node(state: BMIState):
    bmi = state["bmi"]
    prompt = f"""
        You are MedIntel AI.

        A user has a BMI of {bmi}.

        1. Categorize the BMI into:
        - Underweight
        - Healthy
        - Overweight
        - Obese

        2. Give 3–4 general wellness recommendations.

        3. Never prescribe medicines.

        4. Encourage consulting healthcare professionals.

        Format:

        Category: ...
        Advice: ...
    """
    response = llm.invoke(prompt)
    content = response.content
    category = "Unknown"

    for line in content.split("\n"):
        if line.lower().startswith("category:"):
            category = line.replace(
                "Category:",
                ""
            ).strip()

    return {
        "category": category,
        "advice": content
    }

graph = StateGraph(BMIState)

graph.add_node("calculate_bmi", bmi_node)
graph.add_node("interpret_bmi", interpretation_node)

graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "interpret_bmi")
graph.add_edge("interpret_bmi", END)

workflow = graph.compile()


def get_bmi_report(weight: float, height: float):
    result = workflow.invoke(
        {
            "weight": weight,
            "height": height
        }
    )

    return {
        "bmi": result["bmi"],
        "category": result["category"],
        "advice": result["advice"]
    }