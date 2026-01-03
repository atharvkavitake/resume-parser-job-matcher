"""
File handling utilities
Extracts text from PDF and DOCX files
"""

import os
import PyPDF2
from docx import Document
from config import config

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        str: Extracted text
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path):
    """
    Extract text from DOCX file
    
    Args:
        file_path (str): Path to DOCX file
        
    Returns:
        str: Extracted text
    """
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_text(file_path):
    """
    Extract text from file (PDF or DOCX)
    Automatically detects file type
    
    Args:
        file_path (str): Path to file
        
    Returns:
        str: Extracted text
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = file_path.rsplit('.', 1)[1].lower()
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext in ['docx', 'doc']:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

