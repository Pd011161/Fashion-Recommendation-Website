# ============ LangChain ============
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
import numpy as np
# from .faiss_loader import *
from dotenv import load_dotenv

# ============ ENV ============
load_dotenv()
openapi_key = os.getenv("OPENAI_API_KEY")

# ============ EMBEDDER ============
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("intfloat/multilingual-e5-base")

parser = JsonOutputParser()

prompt_template = PromptTemplate.from_template("""
คุณคือระบบช่วยแยกประเภทสินค้าแฟชั่นจากคำอธิบายสินค้า
ให้คุณพิจารณาจาก description ที่ได้รับ แล้วตอบกลับเป็น JSON
โดยเลือก class ได้แค่ 2 แบบ คือ "เสื้อ" หรือ "กางเกง" เท่านั้น
ห้ามอธิบายเพิ่ม

ตัวอย่างที่1 :
Description: เสื้อเชิ้ตผ้าคอตตอนแขนยาว สีขาวคลาสสิก ทรงพอดีตัว เหมาะสำหรับใส่ทำงานหรือใส่ลำลอง
ผลลัพธ์:
{{
"class": "เสื้อ"
}}

ตัวอย่างที่2 :
Description: กางเกงขายาวทรงกระบอก ผลิตจากผ้ายีนส์คุณภาพสูง สีฟ้าอ่อน ดีไซน์เรียบง่าย
ผลลัพธ์:
{{
"class": "กางเกง"
}}

Description: {description}
ผลลัพธ์:
{{
"class": "เสื้อ" หรือ "กางเกง"
}}
""")


llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.0,
    # max_tokens=512,
    openai_api_key=openapi_key
)

chain = prompt_template | llm | parser

def classify_fashion_type(caption):
    result = chain.invoke({"description": caption})
    return result["class"]
