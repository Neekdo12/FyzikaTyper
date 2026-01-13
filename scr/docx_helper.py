from docx import Document
import json

def export(data, document, prefix):
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
    
