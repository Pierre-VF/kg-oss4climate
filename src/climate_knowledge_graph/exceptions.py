class MissingDependencyInstall(ImportError):
    def __init__(self, dependency: str):
        super().__init__(
            f"{dependency} not installed (make sure to install all dependency groups (uv sync --all-groups) )"
        )
