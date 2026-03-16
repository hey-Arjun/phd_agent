from utils.llm import get_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm()

prompt = PromptTemplate(
    template="""
You are an expert research assistant.

Extract information about a PhD program from the webpage text.

Return ONLY valid JSON with these fields:

university
country
phd_program
funding
tuition_fees
requirements
application_deadline
application_link

Rules:
- If data is missing return "Not found"
- Do not explain anything
- Do not add text before or after JSON

Only extract university name if the university hosting the PhD program is clearly mentioned.
Do not infer country from scholarship names.

TEXT:
{text}

JSON:
""",
    input_variables=["text"],
)

parser = JsonOutputParser()


def extract_phd_info(text):

    chain = prompt | llm | parser

    result = chain.invoke({
        "text": text[:12000]   # limit text to avoid token overflow
    })

    return result
