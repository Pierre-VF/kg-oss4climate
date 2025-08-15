
.PHONY: install
install:
	uv sync --all-groups


.PHONY: local_db_run
local_db_run:
	chmod +x src/shell/neo4j_run_in_docker.sh
	src/shell/neo4j_run_in_docker.sh

.PHONY: cleanup
cleanup:
	uv tool run pre-commit run --all

.PHONY: test
test:
	uv run pytest src/test
