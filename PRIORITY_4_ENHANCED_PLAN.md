# Priority 4: Asset Processing - Enhanced Plan

**Date**: October 17, 2025  
**Status**: Planning Phase  
**Estimated Effort**: 7-8 hours (enhanced from 5-6 hours)

---

## Overview

Asset Processing converts various project assets (code, Docker Compose, OpenAPI specs) into comprehensive documentation. Enhanced with industry best practices including mkdocstrings integration, Docker support, and diagram generation.

---

## Goals

### Original Goals
1. ✅ Docker Compose → Documentation
2. ✅ Code → API Documentation
3. ✅ Auto-discovery system

### Enhanced Goals (From Research)
4. **mkdocstrings Integration** ⭐⭐⭐
   - Use mkdocstrings for structured API docs
   - Add AI-generated summaries
   - Add AI-generated usage examples
   - Auto-discover Python modules

5. **Docker Integration** ⭐⭐
   - Create Dockerfile for reproducible builds
   - Add Docker Compose for development
   - Support volume mounting for hot-reload

6. **Diagram Generation** ⭐⭐
   - Mermaid diagrams from code structure
   - Architecture diagrams from Docker Compose
   - Dependency graphs

---

## Architecture

### Component Overview

```
Asset Processing System
├── AssetDiscovery
│   ├── Scan project for assets
│   ├── Identify asset types
│   └── Build asset inventory
│
├── AssetProcessors
│   ├── DockerComposeProcessor
│   │   ├── Parse docker-compose.yml
│   │   ├── Generate service docs
│   │   ├── Create architecture diagram (NEW)
│   │   └── Document networking
│   │
│   ├── PythonCodeProcessor (ENHANCED)
│   │   ├── Use mkdocstrings for API reference
│   │   ├── Generate AI summaries
│   │   ├── Create usage examples with AI
│   │   ├── Generate class diagrams (NEW)
│   │   └── Auto-discover modules
│   │
│   ├── OpenAPIProcessor
│   │   ├── Parse OpenAPI/Swagger specs
│   │   ├── Generate endpoint docs
│   │   └── Create request/response examples
│   │
│   └── MermaidProcessor (NEW)
│       ├── Generate class diagrams
│       ├── Generate sequence diagrams
│       └── Generate architecture diagrams
│
└── DocumentationGenerator
    ├── Combine structured + AI content
    ├── Apply templates
    └── Generate final markdown
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (2 hours)

#### 1.1 Asset Discovery

```python
# mkdocs_ai/assets/discovery.py
class AssetDiscovery:
    """Discover assets in project."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.assets = []
    
    def discover_all(self) -> list[Asset]:
        """Discover all supported assets."""
        self.discover_docker_compose()
        self.discover_python_modules()
        self.discover_openapi_specs()
        return self.assets
    
    def discover_python_modules(self) -> list[Asset]:
        """Discover Python modules for documentation."""
        modules = []
        for py_file in self.project_root.rglob("*.py"):
            if self._should_document(py_file):
                modules.append(Asset(
                    type="python",
                    path=py_file,
                    name=self._get_module_name(py_file)
                ))
        return modules
```

#### 1.2 Base Processor

```python
# mkdocs_ai/assets/base.py
class AssetProcessor(ABC):
    """Base class for asset processors."""
    
    def __init__(self, provider: AIProvider, cache: CacheManager):
        self.provider = provider
        self.cache = cache
    
    @abstractmethod
    async def process(self, asset: Asset) -> Documentation:
        """Process asset and generate documentation."""
        pass
    
    @abstractmethod
    def generate_structure(self, asset: Asset) -> dict:
        """Generate structured documentation."""
        pass
    
    async def enhance_with_ai(self, structure: dict) -> str:
        """Enhance structured docs with AI."""
        pass
```

### Phase 2: Docker Compose Processor (1.5 hours)

```python
# mkdocs_ai/assets/docker_compose.py
class DockerComposeProcessor(AssetProcessor):
    """Process Docker Compose files."""
    
    async def process(self, asset: Asset) -> Documentation:
        """Process docker-compose.yml file."""
        # Parse YAML
        compose_data = self._parse_compose(asset.path)
        
        # Generate structure
        structure = self.generate_structure(compose_data)
        
        # Generate Mermaid diagram (NEW)
        diagram = self._generate_architecture_diagram(compose_data)
        
        # Enhance with AI
        enhanced = await self.enhance_with_ai(structure)
        
        return Documentation(
            content=enhanced,
            diagrams=[diagram],
            metadata=structure
        )
    
    def _generate_architecture_diagram(self, compose_data: dict) -> str:
        """Generate Mermaid architecture diagram."""
        services = compose_data.get('services', {})
        
        mermaid = ["graph TD"]
        
        # Add services
        for name, config in services.items():
            mermaid.append(f"    {name}[{name}]")
        
        # Add dependencies
        for name, config in services.items():
            depends_on = config.get('depends_on', [])
            for dep in depends_on:
                mermaid.append(f"    {name} --> {dep}")
        
        # Add networks
        for name, config in services.items():
            networks = config.get('networks', [])
            for network in networks:
                mermaid.append(f"    {name} -.-> net_{network}")
        
        return "\n".join(mermaid)
```

### Phase 3: Python Code Processor with mkdocstrings (2 hours)

```python
# mkdocs_ai/assets/python_code.py
class PythonCodeProcessor(AssetProcessor):
    """Process Python code with mkdocstrings integration."""
    
    def __init__(self, provider: AIProvider, cache: CacheManager):
        super().__init__(provider, cache)
        self.use_mkdocstrings = True
    
    async def process(self, asset: Asset) -> Documentation:
        """Process Python module."""
        # Parse module
        module_info = self._parse_module(asset.path)
        
        # Generate mkdocstrings reference
        api_reference = self._generate_mkdocstrings_ref(module_info)
        
        # Generate AI summary (NEW)
        summary = await self._generate_summary(module_info)
        
        # Generate usage examples (NEW)
        examples = await self._generate_examples(module_info)
        
        # Generate class diagram (NEW)
        diagram = self._generate_class_diagram(module_info)
        
        # Combine into documentation
        content = self._combine_content(
            summary=summary,
            api_reference=api_reference,
            examples=examples
        )
        
        return Documentation(
            content=content,
            diagrams=[diagram],
            metadata=module_info
        )
    
    def _generate_mkdocstrings_ref(self, module_info: dict) -> str:
        """Generate mkdocstrings reference."""
        module_path = module_info['module_path']
        
        return f"""
## API Reference

::: {module_path}
    options:
      show_source: true
      show_root_heading: true
      show_root_full_path: false
      members_order: source
"""
    
    async def _generate_summary(self, module_info: dict) -> str:
        """Generate AI summary of module."""
        prompt = f"""
Generate a concise summary of this Python module:

Module: {module_info['name']}
Classes: {', '.join(module_info['classes'])}
Functions: {', '.join(module_info['functions'])}

Docstring:
{module_info['docstring']}

Provide:
1. What the module does (1-2 sentences)
2. Key features (bullet points)
3. When to use it (1 sentence)
"""
        
        response = await self.provider.generate(prompt)
        return response.content
    
    async def _generate_examples(self, module_info: dict) -> str:
        """Generate usage examples with AI."""
        prompt = f"""
Generate practical usage examples for this Python module:

Module: {module_info['name']}
Classes: {', '.join(module_info['classes'])}
Functions: {', '.join(module_info['functions'])}

Create 2-3 examples showing:
1. Basic usage
2. Common use case
3. Advanced usage (if applicable)

Use realistic code that would actually work.
"""
        
        response = await self.provider.generate(prompt)
        return response.content
    
    def _generate_class_diagram(self, module_info: dict) -> str:
        """Generate Mermaid class diagram."""
        classes = module_info.get('classes', [])
        
        if not classes:
            return ""
        
        mermaid = ["classDiagram"]
        
        for cls in classes:
            # Add class
            mermaid.append(f"    class {cls['name']} {{")
            
            # Add methods
            for method in cls.get('methods', []):
                mermaid.append(f"        +{method}()")
            
            mermaid.append("    }")
            
            # Add inheritance
            if cls.get('bases'):
                for base in cls['bases']:
                    mermaid.append(f"    {base} <|-- {cls['name']}")
        
        return "\n".join(mermaid)
```

### Phase 4: Mermaid Processor (1 hour)

```python
# mkdocs_ai/assets/mermaid.py
class MermaidProcessor:
    """Generate Mermaid diagrams."""
    
    def generate_class_diagram(self, classes: list[dict]) -> str:
        """Generate class diagram from class info."""
        pass
    
    def generate_sequence_diagram(self, interactions: list[dict]) -> str:
        """Generate sequence diagram from interactions."""
        pass
    
    def generate_architecture_diagram(self, components: list[dict]) -> str:
        """Generate architecture diagram from components."""
        pass
    
    def generate_dependency_graph(self, dependencies: dict) -> str:
        """Generate dependency graph."""
        pass
```

### Phase 5: Docker Integration (1.5 hours)

#### 5.1 Dockerfile

```dockerfile
# Dockerfile
FROM squidfunk/mkdocs-material:latest

# Install system dependencies
RUN apk add --no-cache git

# Copy project
COPY . /app
WORKDIR /app

# Install our plugin
RUN pip install -e .

# Install additional plugins
RUN pip install \
    mkdocstrings[python] \
    mkdocs-mermaid2-plugin \
    mkdocs-awesome-pages-plugin

# Expose port
EXPOSE 8000

# Default command
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
```

#### 5.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  mkdocs:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./docs:/app/docs
      - ./mkdocs.yml:/app/mkdocs.yml
      - ./.ai-cache:/app/.ai-cache
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    command: mkdocs serve -a 0.0.0.0:8000
    restart: unless-stopped

  # Optional: Separate service for building
  build:
    build: .
    volumes:
      - ./docs:/app/docs
      - ./mkdocs.yml:/app/mkdocs.yml
      - ./site:/app/site
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    command: mkdocs build
    profiles:
      - build
```

#### 5.3 Documentation

```markdown
# docs/docker-setup.md

## Docker Setup

### Quick Start

```bash
# Build and run
docker-compose up

# Access at http://localhost:8000
```

### Development

```bash
# Run with hot-reload
docker-compose up mkdocs

# Build only
docker-compose --profile build up build
```

### Environment Variables

Create `.env` file:

```
OPENROUTER_API_KEY=your-key
GEMINI_API_KEY=your-key
```
```

---

## Configuration

### mkdocs.yml Updates

```yaml
plugins:
  - search
  
  - ai-assistant:
      assets:
        enabled: true
        sources:
          - type: python
            path: src/
            output_dir: docs/api
            use_mkdocstrings: true
            ai_summaries: true
            ai_examples: true
            generate_diagrams: true
          
          - type: docker-compose
            path: docker-compose.yml
            output_dir: docs/infrastructure
            generate_diagrams: true
          
          - type: openapi
            path: openapi.yaml
            output_dir: docs/api-reference
  
  # mkdocstrings for API documentation
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            members_order: source
            docstring_style: google
  
  # Mermaid for diagrams
  - mermaid2:
      version: 10.6.1

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

---

## CLI Commands

### Asset Discovery

```bash
# Discover all assets
mkdocs-ai assets discover

# Discover specific type
mkdocs-ai assets discover --type python

# Show asset inventory
mkdocs-ai assets list
```

### Asset Processing

```bash
# Process all assets
mkdocs-ai assets process

# Process specific asset
mkdocs-ai assets process src/mymodule.py

# Process with options
mkdocs-ai assets process \
  --type python \
  --output docs/api \
  --diagrams \
  --examples
```

### Docker Commands

```bash
# Build Docker image
docker-compose build

# Run development server
docker-compose up

# Build documentation
docker-compose --profile build up build

# Run with custom config
docker-compose run mkdocs mkdocs build -f custom.yml
```

---

## Data Models

```python
# mkdocs_ai/assets/models.py

@dataclass
class Asset:
    """Represents a project asset."""
    type: str  # python, docker-compose, openapi
    path: Path
    name: str
    metadata: dict = field(default_factory=dict)

@dataclass
class Documentation:
    """Generated documentation."""
    content: str
    diagrams: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    examples: list[str] = field(default_factory=list)

@dataclass
class AssetConfig:
    """Configuration for asset processing."""
    enabled: bool = False
    sources: list[AssetSource] = field(default_factory=list)
    use_mkdocstrings: bool = True
    generate_diagrams: bool = True
    ai_summaries: bool = True
    ai_examples: bool = True
```

---

## Testing Strategy

### Unit Tests
- Asset discovery
- Each processor independently
- Diagram generation
- AI enhancement

### Integration Tests
- Full asset processing pipeline
- mkdocstrings integration
- Docker build and run
- Documentation generation

### Manual Tests
- Process real Python modules
- Process real Docker Compose files
- Verify diagram rendering
- Check AI-generated content quality

---

## Success Metrics

### Functionality
- [ ] Discover Python modules automatically
- [ ] Generate API docs with mkdocstrings
- [ ] Add AI summaries and examples
- [ ] Generate class diagrams
- [ ] Process Docker Compose files
- [ ] Generate architecture diagrams
- [ ] Docker image builds successfully
- [ ] Hot-reload works in Docker

### Quality
- [ ] API docs are accurate
- [ ] AI summaries are helpful
- [ ] Examples are runnable
- [ ] Diagrams are clear
- [ ] Docker setup is easy

### Performance
- [ ] Asset discovery < 5s for 100 files
- [ ] Processing < 10s per module
- [ ] Docker build < 2 minutes
- [ ] Hot-reload < 1s

---

## Timeline

### Week 1: Core Implementation (7-8 hours)
- Day 1-2: Asset discovery and base processor (2h)
- Day 2-3: Docker Compose processor (1.5h)
- Day 3-4: Python code processor with mkdocstrings (2h)
- Day 4-5: Mermaid processor (1h)
- Day 5-6: Docker integration (1.5h)

### Week 2: Testing and Documentation
- Testing (2h)
- Documentation (1h)
- Examples (1h)

---

## Dependencies

### New Dependencies

```toml
# pyproject.toml
dependencies = [
    # ... existing ...
    "mkdocstrings[python]>=0.24.0",  # NEW
    "mkdocs-mermaid2-plugin>=1.1.0",  # NEW
]
```

---

## Conclusion

Priority 4 (Asset Processing) enhanced with industry best practices will provide:

1. **Automatic API Documentation** - mkdocstrings integration
2. **AI-Enhanced Content** - Summaries and examples
3. **Visual Documentation** - Mermaid diagrams
4. **Docker Support** - Reproducible builds
5. **Comprehensive Coverage** - Code, Docker, OpenAPI

**Estimated Effort**: 7-8 hours (worth the enhancement!)

**Next**: Implement Phase 1 (Core Infrastructure)

---

**Last Updated**: October 17, 2025
