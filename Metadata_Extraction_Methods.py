import zipfile
import json
import csv
import docx
from PyPDF2 import PdfReader
import openpyxl
import sqlite3
from PIL import Image

def excel_metadata(downloaded_files):
    metadata = {}
    try:
        workbook = openpyxl.load_workbook(downloaded_files, read_only=True)
        properties = workbook.properties
        metadata["Title"] = properties.title
        metadata["Author"] = properties.creator
    except Exception as e:
        metadata["Error"] = f"Error Excel: {e}"
    return metadata

def pdf_metadata(downloaded_files):
    metadata = {}
    try:
        reader = PdfReader(downloaded_files)
        info = reader.metadata
        metadata["Title"] = info.get("/Title", "N/A")
        metadata["Author"] = info.get("/Author", "N/A")
        metadata["Creator"] = info.get("/Creator", "N/A")
        metadata["Producer"] = info.get("/Producer", "N/A")
        metadata["CreationDate"] = info.get("/CreationDate", "N/A")
    except Exception as e:
        metadata["Error"] = f"Error PDF: {e}"
    return metadata

def word_metadata(downloaded_files):
    metadata = {}
    try:
        doc = docx.Document(downloaded_files)
        core_props = doc.core_properties
        metadata["Title"] = core_props.title
        metadata["Author"] = core_props.author
        metadata["Created"] = core_props.created.strftime("%Y-%m-%d %H:%M:%S")
        metadata["Modified"] = core_props.modified.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        metadata["Error"] = f"Error Word: {e}"
    return metadata

def csv_metadata(downloaded_files):
    metadata = {}
    try:
        with open(downloaded_files, "r") as f:
            reader = csv.reader(f)
            header = next(reader, None)
        metadata["Header"] = header if header else "No header found"
    except Exception as e:
        metadata["Error"] = f"Error CSV: {e}"
    return metadata

def json_metadata(downloaded_files):
    metadata = {}
    try:
        with open(downloaded_files, "r") as f:
            json_data = json.load(f)
        metadata["Keys Count"] = len(json_data) if isinstance(json_data, dict) else "N/A"
    except Exception as e:
        metadata["Error"] = f"Error JSON: {e}"
    return metadata

def database_metadata(downloaded_files):
    metadata = {}
    try:
        conn = sqlite3.connect(downloaded_files)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        metadata["Tables"] = [table[0] for table in tables]
    except Exception as e:
        metadata["Error"] = f"Error Database: {e}"
    return metadata

def zip_metadata(downloaded_files):
    metadata = {}
    try:
        with zipfile.ZipFile(downloaded_files, "r") as zip_ref:
            metadata["Contained Files"] = zip_ref.namelist()
    except Exception as e:
        metadata["Error"] = f"Error Zip: {e}"
    return metadata

def img_metadata(downloaded_files):
    metadata = {}
    try:
        image = Image.open(downloaded_files)
        metadata["Dimensions"] = image.size
    except Exception as e:
        metadata["Error"] = f"Error Image: {e}"
    return metadata