import os, json, openpyxl

root = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'

def check_string(s, loc):
    if not isinstance(s, str):
        return
    if '\ufffd' in s:
        print(f"[MOJIBAKE/REPLACEMENT CHAR] in {loc}: {repr(s)}")
    # Check common mojibake patterns
    for bad in ['Ã¡', 'Ã©', 'Ã­', 'Ã³', 'Ãº', 'Ã±', 'Ã‘', 'Ã‰', 'Ã“', 'Ãš', 'Ã']:
        if bad in s:
            print(f"[UTF-8 MOJIBAKE '{bad}'] in {loc}: {repr(s)}")

# 1. Check participantes.json
json_path = os.path.join(root, 'data', 'participantes.json')
with open(json_path, 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()
    if '\ufffd' in text:
        print(f"FOUND \\ufffd in {json_path}")
    data = json.loads(text)
    for i, p in enumerate(data):
        for k, v in p.items():
            check_string(v, f"participantes.json [{p.get('id', i)}] field '{k}'")

# 2. Check registro_certificados_foro_2026.xlsx
excel_path = os.path.join(root, 'registro_certificados_foro_2026.xlsx')
wb = openpyxl.load_workbook(excel_path)
for sname in wb.sheetnames:
    ws = wb[sname]
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
        for col_idx, cell_val in enumerate(row, 1):
            if isinstance(cell_val, str):
                check_string(cell_val, f"Excel sheet '{sname}' R{row_idx}C{col_idx}")

# 3. Check index.html
html_path = os.path.join(root, 'index.html')
with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
    for line_idx, line in enumerate(f, 1):
        if '\ufffd' in line:
            print(f"[REPLACEMENT CHAR] in index.html line {line_idx}: {line.strip()[:100]}")
