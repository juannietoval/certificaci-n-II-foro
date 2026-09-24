# -*- coding: utf-8 -*-
import json
import re

FEMALE_NAMES = {
    'erika', 'maria', 'maría', 'nohelia', 'zahira', 'yesenia', 'katherine',
    'elena', 'ana', 'lady', 'veronica', 'verónica', 'carolina', 'julia',
    'liseth', 'melissa', 'ester', 'dahiana', 'lina', 'celina', 'cinthya',
    'fátima', 'fatima', 'jorgelina', 'dorelys', 'doris', 'fabiola', 'mayra',
    'belkis', 'katty', 'eva', 'diana', 'andrea', 'bertha', 'giovana',
    'montserrat', 'antonia', 'myriam', 'laura', 'cristina', 'araceli',
    'marcelina', 'thailing', 'alba', 'elisa', 'angie', 'emma', 'mariana',
    'isela', 'ligia', 'mariela', 'cassandra', 'karina', 'wendolyne', 'rocio',
    'rocío', 'consuelo', 'gloria', 'patricia', 'sandra', 'claudia', 'monica',
    'mónica', 'paola', 'martha', 'marta', 'luz', 'carmen', 'pilar', 'mercedes',
    'guadalupe', 'rosario', 'concepcion', 'concepción', 'beatriz', 'raquel',
    'ines', 'inés', 'astrid', 'vanessa', 'vanesa', 'tatiana', 'stephanie',
    'stefany', 'natalya', 'natalia', 'ximena', 'sheyla', 'nancy', 'margarita',
    'leidy', 'analia', 'analía', 'camila', 'moncerrath'
}

MALE_NAMES = {
    'juan', 'carlos', 'pablo', 'eduardo', 'francisco', 'rubén', 'ruben',
    'alexandre', 'rafael', 'camilo', 'enrique', 'leandro', 'edgar', 'julian',
    'julián', 'rodolfo', 'alán', 'alan', 'frank', 'ricardo', 'josé', 'jose',
    'pascual', 'erick', 'martín', 'martin', 'marco', 'bayron', 'wesley',
    'héctor', 'hector', 'daniel', 'napoleón', 'napoleon', 'miguel', 'javier',
    'fabian', 'fabián', 'jorge', 'reisner', 'benjamín', 'benjamin', 'cristian',
    'darlington', 'darlingthon'
}

def get_tratamiento(nombre):
    if not nombre:
        return "Estimado(a)"
    
    nm = nombre.strip()
    nm_lower = nm.lower()
    
    # Check prefixes
    if nm_lower.startswith("dra.") or nm_lower.startswith("doctora"):
        return "Estimada"
    if nm_lower.startswith("dr.") or nm_lower.startswith("doctor"):
        return "Estimado"
        
    # Extract first name
    # Remove titles
    clean_n = re.sub(r'^(dr\.|dra\.|ing\.|lic\.|prof\.|profesor|profesora)\s+', '', nm_lower)
    parts = clean_n.split()
    first = parts[0] if parts else ""
    
    # Special cases like "María del Rosario" -> female
    if first in FEMALE_NAMES:
        return "Estimada"
    if first in MALE_NAMES:
        return "Estimado"
        
    # Second name check (e.g., "José Luis", "Dora Inés", "Ana María")
    if len(parts) > 1 and parts[1] in FEMALE_NAMES:
        return "Estimada"
    if len(parts) > 1 and parts[1] in MALE_NAMES:
        return "Estimado"
        
    # Ending rule
    if first.endswith('a'):
        return "Estimada"
    return "Estimado"

# Test across all 114 participants
with open(r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados\data\participantes.json', 'r', encoding='utf-8') as f:
    participantes = json.load(f)

print(f"Testing treatment on {len(participantes)} participants:")
results = []
for p in participantes:
    t = get_tratamiento(p['nombre'])
    results.append(f"{t} {p['nombre']}")

for r in results[:15]:
    print(" ", r)

print("...")
for r in results[50:60]:
    print(" ", r)
