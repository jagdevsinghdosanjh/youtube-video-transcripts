from deep_translator import GoogleTranslator as gt
from fpdf import FPDF

def get_supported_languages():
    return gt.get_supported_languages() # pyright: ignore[reportCallIssue]
# GoogleTranslator.get_supported_languages()

def translate_text(text, target_lang):
    return gt(source="auto", target=target_lang).translate(text) # pyright: ignore[reportUndefinedVariable, reportCallIssue]
#GoogleTranslator(source="auto", target=target_lang).translate(text)

def save_translated_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
