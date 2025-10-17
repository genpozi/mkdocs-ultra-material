"""Asset discovery for documentation generation."""

import logging
from pathlib import Path
from typing import Optional

from .models import Asset

logger = logging.getLogger("mkdocs.plugins.ai-assistant.assets")


class AssetDiscovery:
    """Discover assets in project for documentation."""

    def __init__(self, project_root: str):
        """Initialize asset discovery.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.assets: list[Asset] = []

    def discover_all(self) -> list[Asset]:
        """Discover all supported assets.

        Returns:
            List of discovered assets
        """
        self.assets = []
        self.discover_docker_compose()
        self.discover_python_modules()
        self.discover_openapi_specs()
        return self.assets

    def discover_docker_compose(self) -> list[Asset]:
        """Discover Docker Compose files.

        Returns:
            List of Docker Compose assets
        """
        compose_files = []

        # Common Docker Compose file names
        patterns = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
        ]

        for pattern in patterns:
            for compose_file in self.project_root.rglob(pattern):
                if self._should_document(compose_file):
                    asset = Asset(
                        type="docker-compose",
                        path=compose_file,
                        name=compose_file.stem,
                        metadata={"pattern": pattern},
                    )
                    compose_files.append(asset)
                    self.assets.append(asset)
                    logger.debug(f"Discovered Docker Compose: {compose_file}")

        return compose_files

    def discover_python_modules(
        self, source_dir: Optional[str] = None
    ) -> list[Asset]:
        """Discover Python modules for documentation.

        Args:
            source_dir: Optional source directory to search in

        Returns:
            List of Python module assets
        """
        modules = []
        search_dir = Path(source_dir) if source_dir else self.project_root

        for py_file in search_dir.rglob("*.py"):
            if self._should_document(py_file):
                asset = Asset(
                    type="python",
                    path=py_file,
                    name=self._get_module_name(py_file),
                    metadata={"is_package": py_file.name == "__init__.py"},
                )
                modules.append(asset)
                self.assets.append(asset)
                logger.debug(f"Discovered Python module: {py_file}")

        return modules

    def discover_openapi_specs(self) -> list[Asset]:
        """Discover OpenAPI specification files.

        Returns:
            List of OpenAPI spec assets
        """
        specs = []

        # Common OpenAPI file patterns
        patterns = ["openapi.yml", "openapi.yaml", "swagger.yml", "swagger.yaml"]

        for pattern in patterns:
            for spec_file in self.project_root.rglob(pattern):
                if self._should_document(spec_file):
                    asset = Asset(
                        type="openapi",
                        path=spec_file,
                        name=spec_file.stem,
                        metadata={"format": spec_file.suffix[1:]},
                    )
                    specs.append(asset)
                    self.assets.append(asset)
                    logger.debug(f"Discovered OpenAPI spec: {spec_file}")

        return specs

    def _should_document(self, file_path: Path) -> bool:
        """Determine if a file should be documented.

        Args:
            file_path: Path to the file

        Returns:
            True if file should be documented
        """
        # Skip hidden files and directories
        if any(part.startswith(".") for part in file_path.parts):
            return False

        # Skip common excluded directories
        excluded_dirs = {
            "node_modules",
            "__pycache__",
            "venv",
            "env",
            ".venv",
            ".env",
            "build",
            "dist",
            ".git",
            ".tox",
            ".pytest_cache",
        }

        if any(excluded in file_path.parts for excluded in excluded_dirs):
            return False

        # Skip test files for Python
        if file_path.suffix == ".py" and (
            file_path.name.startswith("test_") or file_path.name.endswith("_test.py")
        ):
            return False

        return True

    def _get_module_name(self, py_file: Path) -> str:
        """Get Python module name from file path.

        Args:
            py_file: Path to Python file

        Returns:
            Module name (e.g., 'package.module')
        """
        # Get relative path from project root
        try:
            rel_path = py_file.relative_to(self.project_root)
        except ValueError:
            rel_path = py_file

        # Convert path to module name
        parts = list(rel_path.parts[:-1])  # Exclude filename
        if py_file.name != "__init__.py":
            parts.append(py_file.stem)

        return ".".join(parts) if parts else py_file.stem
