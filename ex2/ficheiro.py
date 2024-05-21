from rdflib import Graph, URIRef, Namespace

# Carregar o grafo RDF
g = Graph()
g.parse("updated_medical.ttl", format="ttl")

namespace = Namespace("http://www.example.org/disease-ontology#")

# Consulta SPARQL CONSTRUCT para diagnosticar doenças
construct_query = """
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?patient :hasDisease ?disease .
}
WHERE {
  ?patient rdf:type :Patient ;
           :exhibitsSymptom ?symptom .
  ?disease rdf:type :Disease ;
           :hasSymptom ?symptom .
}
"""

# Executar a consulta CONSTRUCT
diagnosis_graph = g.query(construct_query)

# Adicionar os triplos resultantes ao grafo original
for triple in diagnosis_graph:
    g.add(triple)

# Salvar o grafo atualizado em um novo arquivo Turtle
with open("diagnosed_medical.ttl", "w") as f:
    f.write(g.serialize(format="ttl"))

print("Diagnóstico adicionado e arquivo salvo como diagnosed_medical.ttl")
