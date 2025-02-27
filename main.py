import os
import requests
import openai
from fastapi import FastAPI
from fpdf import FPDF

app = FastAPI()

# Получаем API-ключи из переменных окружения
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === 1. Поиск информации ===
def google_search(query, num_results=5):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&num={num_results}"
    response = requests.get(url).json()
    return [
        {"title": item["title"], "link": item["link"], "snippet": item.get("snippet", "Нет описания")}
        for item in response.get("items", [])
    ]

# === 2. Анализ текста через GPT ===
def analyze_text_with_gpt(text):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Analyze this information and summarize key insights."},
                  {"role": "user", "content": text}],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"]

# === 3. Генерация отчета в PDF ===
def generate_pdf_report(title, research_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, title, ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    for item in research_data:
        pdf.cell(0, 10, item["title"], ln=True, link=item.get("link", ""))
        pdf.multi_cell(0, 10, item["snippet"])
        pdf.ln(5)

    pdf.output("research_report.pdf")
    return "research_report.pdf"

# === API Маршруты ===
@app.get("/search")
def search(query: str):
    return {"query": query, "results": google_search(query)}

@app.get("/analyze")
def analyze(query: str):
    search_results = google_search(query)
    combined_text = "\n".join([item["snippet"] for item in search_results])
    return {"query": query, "summary": analyze_text_with_gpt(combined_text)}

@app.get("/report")
def report(query: str):
    search_results = google_search(query)
    combined_text = "\n".join([item["snippet"] for item in search_results])
    summary = analyze_text_with_gpt(combined_text)
    report_data = search_results + [{"title": "AI Анализ", "link": "", "snippet": summary}]
    pdf_path = generate_pdf_report(f"Отчет по теме: {query}", report_data)
    return {"message": "Отчет создан", "file": pdf_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
