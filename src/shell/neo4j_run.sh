#!/bin/bash


mkdir -p .data/neo4j/data &&
mkdir -p .data/plugins &&


if [ -f "/home/pvf/projects/github/kg-oss4climate/.data/neo4j/plugins/apoc-4.4.0.37-all.jar" ]; then
    echo "APOC plugin file exists - skipping download"
else
    echo "File does not exist - downloading."
    pushd /home/pvf/projects/github/kg-oss4climate/.data/neo4j/plugins &&
    wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.37/apoc-4.4.0.37-all.jar &&
    popd
fi


docker run --rm -e NEO4J_AUTH=neo4j/your_password -p 7474:7474 -v .data/neo4j/plugins:/plugins -p 7687:7687 \
    -e NEO4J_PLUGINS='["apoc"]' \
    -e NEO4J_dbms_security_procedures_unrestricted=apoc.* \
    -e NEO4J_dbms_security_procedures_allowlist=apoc.* \
    -v .data/neo4j:/data \
    neo4j:4.4 &&

echo "DONE"