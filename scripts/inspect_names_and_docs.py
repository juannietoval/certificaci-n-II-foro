# -*- coding: utf-8 -*-
import json

with open(r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados\data\asistentes_raw.json', 'r', encoding='utf-8') as f:
    attendees = json.load(f)

print(f"Total: {len(attendees)}")

all_caps = []
has_digits = []
short_names = []
odd_docs = []

for i, a in enumerate(attendees):
    nm = a['nombre']
    doc = a['doc']
    tdoc = a['tipo_doc']
    
    if nm.isupper():
        all_caps.append((i+1, nm))
    if any(c.isdigit() for c in nm):
        has_digits.append((i+1, nm))
    if len(nm.split()) < 2:
        short_names.append((i+1, nm))
    if not doc or doc == 'None' or len(doc) < 4:
        odd_docs.append((i+1, nm, tdoc, doc))

print("\n--- ALL CAPS NAMES ---")
for idx, nm in all_caps:
    print(f"  {idx:3d}. {nm}")

print("\n--- NAMES WITH DIGITS ---")
for idx, nm in has_digits:
    print(f"  {idx:3d}. {nm}")

print("\n--- SHORT NAMES (< 2 words) ---")
for idx, nm in short_names:
    print(f"  {idx:3d}. {nm}")

print("\n--- ODD OR EMPTY DOCS ---")
for idx, nm, tdoc, doc in odd_docs:
    print(f"  {idx:3d}. {nm} | {tdoc} | '{doc}'")
