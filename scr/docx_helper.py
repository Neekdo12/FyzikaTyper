from docx.document import Document
import json


"""
def export(data, document: Document, prefix):
    for para in document.paragraphs:
        for i in data:
            if f"{prefix}-{i}" == para.text:
                para.add_run("\n")
                para.style = "upper"
                for index, line in enumerate(data[i]):
                    for letter in line:
                        match letter[1]:
                            case "n":
                                para.add_run(letter[0])
                            case "d":
                                para.add_run(letter[0]).font.subscript = True
                            case "u":
                                para.add_run(letter[0]).font.superscript = True
                    
                    if index != len(data[i]) - 1:
                        para.add_run("\n")
                        
    document.save("test.docx")
"""

def export(data, document: Document, settings):
    print("Started exporintg")

    for paragraph in document.paragraphs:
        print(f"Trying to export: {paragraph.text.split(sep="\n")[0]}")

        for window in data:
            if paragraph.text.split(sep="\n")[0] == f"{settings("prefix", "zt")}-{window}":
                print(f"Exporting {window}")

                paragraph.text = f"{settings("prefix", "zt")}-{window}\n"
                if settings("export_style", "internal") == "internal":
                    paragraph.style = "upper"
                
                elif settings("export_style", "internal") == "custom":
                    paragraph.style = settings("custom_sytel", "upper")
                
                for index, line in enumerate(data[window]):
                    for letter in line:
                        match letter[1]:
                            case "n":
                                paragraph.add_run(letter[0])
                            case "d":
                                paragraph.add_run(letter[0]).font.subscript = True
                            case "u":
                                paragraph.add_run(letter[0]).font.superscript = True
                
                    if index != len(data[window]) - 1:
                        paragraph.add_run("\n")
    
    document.save(settings("docx", settings.chose_file(settings.file_types["docx"])))
    print("Export done")