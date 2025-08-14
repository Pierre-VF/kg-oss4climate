
.PHONY: install
install:
	uv sync


.PHONY: local_db_run
local_db_run:
	chmod +x src/shell/neo4j_run.sh
	src/shell/neo4j_run.sh


.PHONY: avoid
avoid:
	mkdir -p .data/neo4j/data
	mkdir -p .data/plugins

	pushd /home/pvf/projects/github/kg-oss4climate/.data/neo4j/plugins
	wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/2025.06.0/apoc-2025.06.0-all.jar
	wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.37/apoc-4.4.0.37-all.jar
	popd

	docker run \
		--publish=7474:7474 \
		--publish=7687:7687 \
		--volume=.data/neo4j/data:/data \
		--env NEO4J_AUTH=neo4j/your_password \
		neo4j:5.26.10
	
