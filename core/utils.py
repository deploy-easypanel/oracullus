import re

from markdown import markdown
from markdownify import markdownify as convert_markdown

# def clean_answer(answer: str) -> str:
#     answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip() # Caso o outra LLm
#     return answer


def md_answer(answer: str) -> str:
    convert_markdown(answer, heading_style="ATX")
    return markdown(answer, extensions=["fenced_code", "tables"])
