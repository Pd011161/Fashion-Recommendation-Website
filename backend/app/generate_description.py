import pandas as pd
import os, json, time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
import base64, os
import base64

# ===== Load ENV =====
load_dotenv()

AZURE_OPENAI_KEY       = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT  = os.getenv("AZURE_OPENAI_ENDPOINT")  # "https://xxx.openai.azure.com/"
AZURE_DEPLOYMENT_NAME  = os.getenv("AZURE_DEPLOYMENT_NAME")  # เช่น "gpt-4-vision-preview"
AZURE_API_VERSION      = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")

llm = AzureChatOpenAI(
    openai_api_key    = AZURE_OPENAI_KEY,
    azure_endpoint    = AZURE_OPENAI_ENDPOINT,
    api_version       = AZURE_API_VERSION,
    deployment_name   = AZURE_DEPLOYMENT_NAME,
    temperature       = 0.4,
)

json_parser = JsonOutputParser()  # มีใน langchain-core

system_prompt = (
    "You are a fashion and online marketing expert. "
    "Your task is to write a detailed clothing product description in Thai based on an image, "
    "focusing on clear and concise product attributes and details. "
    "The description will be stored in a vector database for similarity search and matching. "
    "Highlight key information such as product type, brand, material, color, fit, pattern/details, and unique features, "
    "as well as suitable occasions for wearing the item. "
    "The description must be factually accurate, complete, and concise—based only on what is visible in the image. "
    "Do not invent or guess information that is not apparent in the image. "
    "The output must be suitable for use in vector-based search and comparison."
)


user_prompt_text = """
Please generate a **Thai product description** (th_description) for a clothing item based on the given image.
The description should include all relevant details for vector database storage and similarity search.

Include the following details if visible in the image:
- Product type (e.g., T-shirt, shirt, polo shirt, blazer, pants, etc.)
- Brand (if visible)
- Material (e.g., cotton, linen, cotton blend, etc.)
- Color (e.g., white, navy blue, beige, etc.)
- Fit (e.g., loose, straight, slim fit)
- Pattern/details (e.g., front pocket, graphic print, stripes, no pattern)
- Key features or unique characteristics (e.g., breathable fabric, soft texture, color-block design, etc.)
- Suitable occasions for wearing (if inferable from the image, e.g., casual, work, everyday)
- Care instructions (if visible on labels in the image)
Please do **not** add information that is not clear from the image or make assumptions.

Example of a desired output (for vector database storage):
{
  "th_description": "เสื้อสเวตเตอร์คอกลมสีเบจจากแบรนด์ CLASSIC COMFORT เสื้อสเวตเตอร์แขนยาวทรงหลวม ผลิตจากผ้าเนื้อนุ่มให้ความอบอุ่นและสบายในทุกการสวมใส่ ดีไซน์สีเบจคลาสสิกตัดกับขอบสีกรมท่า เพิ่มความโดดเด่นให้กับลุคของคุณ เหมาะสำหรับใส่ในวันสบายๆ หรือในวันที่อากาศเย็น วัสดุ: ผ้าฝ้ายผสม – เนื้อนุ่มและอบอุ่น สี: เบจ (ขอบสีกรมท่า) ทรง: ทรงหลวม ปกเสื้อ: คอกลม กระเป๋า: ไม่มี ลายพิมพ์: ไม่มี จุดเด่น: ดีไซน์สีเบจคลาสสิกตัดกับขอบสีกรมท่า เหมาะสำหรับ: ใส่ในวันสบายๆ, วันที่อากาศเย็น คำแนะนำในการดูแล: ซักมือหรือซักเครื่องโหมดถนอมผ้า / หลีกเลี่ยงการอบร้อน / รีดด้วยไฟอ่อนด้านใน"
}

**Output format:**
{
  "th_description": "Insert a suitable, complete Thai product description for vector search"
}
"""



def encode_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_description_base64(image_path):
    image_base64 = encode_image_base64(image_path)
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": user_prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    )
    chain = llm | json_parser
    desc_json = chain.invoke([
        {"role": "system", "content": system_prompt},
        human_message
    ])
    print("Generate:\n", desc_json)
    return desc_json["th_description"]
