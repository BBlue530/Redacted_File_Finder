import os
from datetime import datetime
import mimetypes
from Metadata_Extraction_Methods import excel_metadata, pdf_metadata, word_metadata, csv_metadata, json_metadata, database_metadata, zip_metadata, img_metadata

def get_mime_type(downloaded_files):
    mime_type, _ = mimetypes.guess_type(downloaded_files)
    return mime_type

def extract_metadata(downloaded_files):
    metadata = {}
    file_extension = os.path.splitext(downloaded_files)[1].lower().replace(".", "")

    if file_extension in ["xls", "xlsx"]:
        metadata = excel_metadata(downloaded_files)
    
    #elif file_extension in ["", ""]:
    #    metadata = (downloaded_files)

    #elif file_extension == "":
    #    metadata = (downloaded_files)
    
    elif file_extension == "pdf":
        metadata = pdf_metadata(downloaded_files)

    elif file_extension in ["doc", "docx"]:
        metadata = word_metadata(downloaded_files)

    elif file_extension == "csv":
        metadata = csv_metadata(downloaded_files)

    elif file_extension == "json":
        metadata = json_metadata(downloaded_files)

    elif file_extension in ["sql", "db", "backup"]:
        metadata = database_metadata(downloaded_files)

    elif file_extension == "zip":
        metadata = zip_metadata(downloaded_files)

    elif file_extension == "img":
        metadata = img_metadata(downloaded_files)

    
    else:
        metadata["Error"] = f"Unsupported file extension: {file_extension}"
    
    try:
        metadata["File Size"] = os.path.getsize(downloaded_files)
        metadata["Last Accessed"] = datetime.fromtimestamp(os.path.getatime(downloaded_files)).strftime("%Y-%m-%d %H:%M:%S")
        metadata["Last Modified"] = datetime.fromtimestamp(os.path.getmtime(downloaded_files)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        metadata["Error"] = f"Error File Properties: {e}"

    return metadata


def process_folder(folder, metadata_report="metadata.txt"):
    path_to_folder = os.path.join(os.getcwd(), folder)
    report = []

    if not os.path.exists(path_to_folder):
        print(f"Error: {folder} does not exist.")
        return

    for root, _, files in os.walk(path_to_folder):
        for file_name in files:
            downloaded_files = os.path.join(root, file_name)
            print(f"Processing file: {file_name}")
            file_metadata = extract_metadata(downloaded_files)
            file_metadata["File Name"] = file_name
            file_metadata["File Path"] = downloaded_files
            report.append(file_metadata)

    with open(metadata_report, "w") as f:
        for file_meta in report:
            f.write(f"File: {file_meta.get("File Name", "Unknown")}\n")
            for key, value in file_meta.items():
                if key not in ["File Name", "File Path"]:
                    f.write(f"  {key}: {value}\n")
            f.write("\n")
    print(f"Metadata saved: {metadata_report}")