import pandas as pd
import os

excel_path = '/home/hugojz/GIT/KZ_proyect/data_privada/Reporte.xlsx'
output_path = '/home/hugojz/GIT/KZ_proyect/data_privada/diccionario_datos.txt'

try:
    # Read the Excel file to get sheet names
    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Diccionario de Datos para {excel_path}\n")
        f.write("="*50 + "\n\n")
        
        for sheet in sheet_names:
            f.write(f"Hoja: {sheet}\n")
            f.write("-" * (len(sheet) + 6) + "\n")
            
            # Read just the header of the sheet
            df = pd.read_excel(excel_path, sheet_name=sheet, nrows=0)
            columns = df.columns.tolist()
            
            for col in columns:
                f.write(f"- {col}\n")
            
            f.write("\n")
            
    print(f"Diccionario generado exitosamente en: {output_path}")

except Exception as e:
    print(f"Error al procesar el archivo: {e}")
