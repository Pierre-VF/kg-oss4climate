

mkdir -p .data/neo4j/data &&
mkdir -p .data/plugins &&

docker run \
    -p 7474:7474 -p 7687:7687 \
    -v .data/neo4j/data:/data -v .data/neo4j/plugins:/plugins \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_PLUGINS='["apoc", "apoc-extended"]' \
    -e NEO4J_AUTH=neo4j/your_password \
    neo4j:5.26.10
