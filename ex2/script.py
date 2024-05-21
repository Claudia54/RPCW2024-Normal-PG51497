from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, OWL
import json
import csv

ids = 0

# Initialize Graph and Namespace
g = Graph()
g.parse("medical.ttl", format="turtle")
namespace = Namespace("http://www.example.org/disease-ontology#")
g.bind("ex", namespace)

def create_uri(name):
    return URIRef(namespace[name.strip().replace(" ", "_").replace(",", "").replace("'", "").replace("__", "_")])

# Process Disease_Symptoms.csv
with open("Disease_Syntoms.csv") as f:
    csv_reader = csv.DictReader(f)
    symptoms = set()

    for row in csv_reader:
        disease_name = row["Disease"].strip().replace(' ', '_')
        disease_uri = create_uri(disease_name)
        
        g.add((disease_uri, RDF.type, namespace.Disease))
        disease_instance_uri = URIRef(f"{namespace}{disease_name}_{ids}")
        ids += 1
        g.add((disease_instance_uri, RDF.type, disease_uri))
        
        for i in range(1, 18):
            symptom = row[f"Symptom_{i}"]
            if symptom:
                symptom_name = symptom.strip().replace(' ', '_')
                symptom_uri = create_uri(symptom_name)
                if symptom_name not in symptoms:
                    symptoms.add(symptom_name)
                    g.add((symptom_uri, RDF.type, namespace.Symptom))
                g.add((disease_instance_uri, namespace.hasSymptom, symptom_uri))

# Process Disease_Description.csv
with open("Disease_Description.csv") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        disease_name = row["Disease"].strip().replace(' ', '_')
        description = row["Description"]
        
        disease_uri = create_uri(disease_name)
        g.add((disease_uri, URIRef(f"{namespace}description"), Literal(description)))

# Serialize and save to file
with open("med_doencas.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode("utf-8"))

# Process Disease_Treatment.csv
treatments = set()

with open("Disease_Treatment.csv") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        disease_name = row["Disease"].strip().replace(' ', '_')
        disease_uri = create_uri(disease_name)
        
        for i in range(1, 5):
            treatment = row[f"Precaution_{i}"]
            if treatment:
                treatment_name = treatment.strip().replace(' ', '_')
                treatment_uri = create_uri(treatment_name)
                if treatment_name not in treatments:
                    treatments.add(treatment_name)
                    g.add((treatment_uri, RDF.type, namespace.Treatment))
                g.add((disease_uri, namespace.hasTreatment, treatment_uri))

# Serialize and save to file
with open("med_tratamentos.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode("utf-8"))

# Process patients from pg51497.json
ids = 0
with open("pg51497.json") as f:
    data = json.load(f)
    for person in data:
        person_uri = URIRef(f"{namespace}PERSON{ids}")
        ids += 1
        
        g.add((person_uri, RDF.type, namespace.Patient))
        g.add((person_uri, namespace.name, Literal(person['nome'])))
        
        symptoms = map(lambda x: x.strip().replace(' ', '_'), person['sintomas'])
        for symptom in symptoms:
            symptom_uri = create_uri(symptom)
            g.add((person_uri, namespace.exhibitsSymptom, symptom_uri))

# Serialize and save to file
with open("med_doentes22.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode("utf-8"))

print("Ontologies saved successfully.")
