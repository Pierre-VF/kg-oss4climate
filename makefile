
.PHONY: install
install:
	uv sync


.PHONY: local_db_run
local_db_run:
	chmod +x src/shell/neo4j_run_in_docker.sh
	src/shell/neo4j_run_in_docker.sh

.PHONY: cleanup
cleanup:
	uv tool run pre-commit run --all