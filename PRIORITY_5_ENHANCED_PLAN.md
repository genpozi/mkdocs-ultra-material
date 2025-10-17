# Priority 5: Obelisk Integration - Enhanced Plan

**Date**: October 17, 2025  
**Status**: Planning Phase  
**Estimated Effort**: 5-6 hours (enhanced from 3-4 hours)

---

## Overview

Obelisk Integration connects the documentation system with a RAG (Retrieval-Augmented Generation) chatbot, creating an interactive documentation experience. Enhanced with "Smart CMS" capabilities that turn user questions into documentation improvements.

---

## Goals

### Original Goals
1. ✅ RAG chatbot interface
2. ✅ Export format compatibility
3. ✅ API client integration

### Enhanced Goals (From Research)
4. **Smart CMS Bridge** ⭐⭐⭐
   - User questions → Missing docs detection
   - AI draft generation
   - Editor review workflow
   - Auto-commit approved docs

5. **Continuous Improvement Loop** ⭐⭐
   - Track common questions
   - Identify documentation gaps
   - Prioritize doc improvements
   - Measure documentation effectiveness

6. **Interactive Features** ⭐⭐
   - In-page chatbot widget
   - Context-aware responses
   - Code example generation
   - Troubleshooting assistant

---

## Architecture

### Component Overview

```
Obelisk Integration System
├── ObeliskClient
│   ├── API client for Obelisk
│   ├── Authentication
│   └── Request/response handling
│
├── DocumentationExporter
│   ├── Export to Obelisk format
│   ├── Chunk documentation
│   ├── Generate embeddings
│   └── Sync with Obelisk
│
├── SmartCMSBridge (NEW)
│   ├── Question analysis
│   ├── Gap detection
│   ├── Draft generation
│   ├── Review workflow
│   └── Auto-commit
│
├── AnalyticsDashboard (NEW)
│   ├── Question tracking
│   ├── Gap analysis
│   ├── Usage metrics
│   └── Improvement suggestions
│
└── ChatbotWidget (NEW)
    ├── In-page chat interface
    ├── Context-aware responses
    ├── Code examples
    └── Troubleshooting
```

---

## Implementation Plan

### Phase 1: Obelisk Client (1 hour)

```python
# mkdocs_ai/obelisk/client.py
class ObeliskClient:
    """Client for Obelisk RAG chatbot API."""
    
    def __init__(self, config: ObeliskConfig):
        self.base_url = config.service_url
        self.api_key = config.api_key
        self.client = httpx.AsyncClient()
    
    async def upload_document(self, doc: Document) -> str:
        """Upload document to Obelisk."""
        response = await self.client.post(
            f"{self.base_url}/api/documents",
            json={
                "title": doc.title,
                "content": doc.content,
                "metadata": doc.metadata,
                "embeddings": doc.embeddings
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()["id"]
    
    async def query(self, question: str, context: dict = None) -> QueryResponse:
        """Query Obelisk with a question."""
        response = await self.client.post(
            f"{self.base_url}/api/query",
            json={
                "question": question,
                "context": context,
                "max_results": 5
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return QueryResponse(**response.json())
    
    async def track_question(self, question: str, results: list, feedback: dict = None):
        """Track question for analytics."""
        await self.client.post(
            f"{self.base_url}/api/analytics/questions",
            json={
                "question": question,
                "results_count": len(results),
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
```

### Phase 2: Documentation Exporter (1 hour)

```python
# mkdocs_ai/obelisk/exporter.py
class DocumentationExporter:
    """Export documentation to Obelisk format."""
    
    def __init__(self, client: ObeliskClient, provider: AIProvider):
        self.client = client
        self.provider = provider
    
    async def export_all(self, docs_dir: Path) -> ExportResult:
        """Export all documentation to Obelisk."""
        documents = []
        
        # Process all markdown files
        for md_file in docs_dir.rglob("*.md"):
            doc = await self._process_file(md_file)
            documents.append(doc)
        
        # Upload to Obelisk
        results = []
        for doc in documents:
            doc_id = await self.client.upload_document(doc)
            results.append(doc_id)
        
        return ExportResult(
            total_docs=len(documents),
            uploaded=len(results),
            doc_ids=results
        )
    
    async def _process_file(self, file_path: Path) -> Document:
        """Process markdown file for Obelisk."""
        content = file_path.read_text()
        
        # Extract metadata
        metadata = self._extract_metadata(content)
        
        # Generate embeddings
        embeddings = await self.provider.embed(content)
        
        # Chunk content
        chunks = self._chunk_content(content)
        
        return Document(
            title=metadata.get("title", file_path.stem),
            content=content,
            chunks=chunks,
            embeddings=embeddings,
            metadata=metadata,
            source_path=str(file_path)
        )
```

### Phase 3: Smart CMS Bridge (2 hours)

```python
# mkdocs_ai/obelisk/smart_cms.py
class SmartCMSBridge:
    """Bridge between Obelisk and documentation system.
    
    Turns user questions into documentation improvements.
    """
    
    def __init__(
        self,
        client: ObeliskClient,
        search_index: VectorIndex,
        generator: PromptGenerator,
        git_repo: str = None
    ):
        self.client = client
        self.search_index = search_index
        self.generator = generator
        self.git_repo = git_repo
    
    async def handle_user_question(self, question: str) -> CMSResponse:
        """Process user question and improve docs if needed."""
        # 1. Search existing docs
        results = await self.search_index.search(
            query=question,
            provider=self.generator.provider,
            limit=5
        )
        
        # 2. Analyze if answer is adequate
        has_good_answer = await self._has_good_answer(question, results)
        
        # 3. If no good answer, create draft
        if not has_good_answer:
            draft = await self._create_doc_draft(question, results)
            await self._submit_for_review(draft)
        
        # 4. Track question for analytics
        await self.client.track_question(
            question=question,
            results=results,
            feedback={"has_good_answer": has_good_answer}
        )
        
        return CMSResponse(
            results=results,
            has_good_answer=has_good_answer,
            draft_created=not has_good_answer
        )
    
    async def _has_good_answer(self, question: str, results: list) -> bool:
        """Determine if existing docs answer the question well."""
        if not results or results[0].score < 0.7:
            return False
        
        # Use AI to judge answer quality
        prompt = f"""
Question: {question}

Best matching documentation:
{results[0].text}

Does this documentation adequately answer the question?
Answer with just "yes" or "no" and a brief reason.
"""
        
        response = await self.generator.provider.generate(prompt)
        return response.content.lower().startswith("yes")
    
    async def _create_doc_draft(self, question: str, existing_results: list) -> DocDraft:
        """Generate documentation draft from question."""
        # Build context from existing docs
        context = "\n\n".join([r.text for r in existing_results[:3]])
        
        # Generate draft
        prompt = f"""
Create documentation to answer this user question:

Question: {question}

Related existing documentation:
{context}

Create a comprehensive documentation page that:
1. Directly answers the question
2. Provides context and background
3. Includes practical examples
4. Links to related topics
5. Follows our documentation style

Format as Markdown with proper headings and structure.
"""
        
        response = await self.generator.provider.generate(prompt)
        
        # Determine appropriate file path
        file_path = self._suggest_file_path(question)
        
        return DocDraft(
            title=self._generate_title(question),
            content=response.content,
            file_path=file_path,
            source_question=question,
            related_docs=[r.page_url for r in existing_results]
        )
    
    async def _submit_for_review(self, draft: DocDraft):
        """Submit draft for editor review."""
        if self.git_repo:
            # Create Git branch and PR
            await self._create_pull_request(draft)
        else:
            # Save to drafts directory
            await self._save_draft(draft)
    
    async def _create_pull_request(self, draft: DocDraft):
        """Create GitHub PR with draft documentation."""
        import subprocess
        
        # Create branch
        branch_name = f"docs/auto-{draft.title.lower().replace(' ', '-')}"
        subprocess.run(["git", "checkout", "-b", branch_name])
        
        # Write file
        file_path = Path(draft.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(draft.content)
        
        # Commit
        subprocess.run(["git", "add", str(file_path)])
        subprocess.run([
            "git", "commit", "-m",
            f"docs: add documentation for '{draft.title}'\n\n"
            f"Auto-generated from user question:\n{draft.source_question}\n\n"
            f"Co-authored-by: AI Assistant <ai@mkdocs-ultra.com>"
        ])
        
        # Push and create PR
        subprocess.run(["git", "push", "origin", branch_name])
        # Use gh CLI or API to create PR
```

### Phase 4: Analytics Dashboard (1 hour)

```python
# mkdocs_ai/obelisk/analytics.py
class AnalyticsDashboard:
    """Track and analyze documentation usage."""
    
    def __init__(self, client: ObeliskClient):
        self.client = client
    
    async def get_common_questions(self, limit: int = 20) -> list[Question]:
        """Get most common user questions."""
        response = await self.client.client.get(
            f"{self.client.base_url}/api/analytics/questions/common",
            params={"limit": limit}
        )
        return [Question(**q) for q in response.json()]
    
    async def identify_gaps(self) -> list[DocumentationGap]:
        """Identify documentation gaps from questions."""
        # Get questions without good answers
        questions = await self.get_common_questions(limit=100)
        
        gaps = []
        for question in questions:
            if question.avg_score < 0.7:
                gaps.append(DocumentationGap(
                    question=question.text,
                    frequency=question.count,
                    avg_score=question.avg_score,
                    priority=self._calculate_priority(question)
                ))
        
        return sorted(gaps, key=lambda g: g.priority, reverse=True)
    
    async def generate_report(self) -> AnalyticsReport:
        """Generate comprehensive analytics report."""
        return AnalyticsReport(
            total_questions=await self._get_total_questions(),
            common_questions=await self.get_common_questions(10),
            documentation_gaps=await self.identify_gaps(),
            coverage_score=await self._calculate_coverage(),
            improvement_suggestions=await self._get_suggestions()
        )
    
    def _calculate_priority(self, question: Question) -> float:
        """Calculate priority for addressing a question."""
        # High frequency + low score = high priority
        return question.count * (1 - question.avg_score)
```

### Phase 5: Chatbot Widget (1 hour)

```javascript
// static/js/chatbot-widget.js
class ChatbotWidget {
    constructor(config) {
        this.apiUrl = config.apiUrl;
        this.apiKey = config.apiKey;
        this.container = null;
        this.init();
    }
    
    init() {
        // Create widget UI
        this.container = document.createElement('div');
        this.container.className = 'mkdocs-chatbot-widget';
        this.container.innerHTML = `
            <div class="chatbot-header">
                <h3>Documentation Assistant</h3>
                <button class="chatbot-close">×</button>
            </div>
            <div class="chatbot-messages"></div>
            <div class="chatbot-input">
                <input type="text" placeholder="Ask a question...">
                <button class="chatbot-send">Send</button>
            </div>
        `;
        
        document.body.appendChild(this.container);
        this.attachEventListeners();
    }
    
    async sendMessage(message) {
        // Add user message to UI
        this.addMessage(message, 'user');
        
        // Get current page context
        const context = {
            page_url: window.location.pathname,
            page_title: document.title
        };
        
        // Query Obelisk
        const response = await fetch(`${this.apiUrl}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                question: message,
                context: context
            })
        });
        
        const data = await response.json();
        
        // Add bot response to UI
        this.addMessage(data.answer, 'bot');
        
        // Show related docs
        if (data.related_docs) {
            this.showRelatedDocs(data.related_docs);
        }
    }
    
    addMessage(text, sender) {
        const messagesDiv = this.container.querySelector('.chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message chatbot-message-${sender}`;
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    showRelatedDocs(docs) {
        const relatedDiv = document.createElement('div');
        relatedDiv.className = 'chatbot-related-docs';
        relatedDiv.innerHTML = '<h4>Related Documentation:</h4>';
        
        docs.forEach(doc => {
            const link = document.createElement('a');
            link.href = doc.url;
            link.textContent = doc.title;
            relatedDiv.appendChild(link);
        });
        
        this.container.querySelector('.chatbot-messages').appendChild(relatedDiv);
    }
}

// Initialize widget
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotWidget({
        apiUrl: window.OBELISK_API_URL,
        apiKey: window.OBELISK_API_KEY
    });
});
```

---

## Configuration

### mkdocs.yml

```yaml
plugins:
  - ai-assistant:
      obelisk:
        enabled: true
        service_url: http://localhost:8000
        api_key: !ENV OBELISK_API_KEY
        
        # Export settings
        export_format: true
        auto_sync: true
        sync_on_build: true
        
        # Smart CMS settings
        smart_cms:
          enabled: true
          auto_draft: true
          create_prs: true
          git_repo: https://github.com/user/repo.git
        
        # Analytics settings
        analytics:
          enabled: true
          track_questions: true
          generate_reports: true
        
        # Chatbot widget
        widget:
          enabled: true
          position: bottom-right
          theme: auto

extra_javascript:
  - js/chatbot-widget.js

extra_css:
  - css/chatbot-widget.css
```

---

## CLI Commands

### Export to Obelisk

```bash
# Export all documentation
mkdocs-ai obelisk export

# Export specific directory
mkdocs-ai obelisk export --docs-dir docs/

# Sync with Obelisk
mkdocs-ai obelisk sync
```

### Analytics

```bash
# Show common questions
mkdocs-ai obelisk analytics questions

# Identify documentation gaps
mkdocs-ai obelisk analytics gaps

# Generate full report
mkdocs-ai obelisk analytics report
```

### Smart CMS

```bash
# Process pending questions
mkdocs-ai obelisk cms process

# Create draft from question
mkdocs-ai obelisk cms draft "How do I configure Docker?"

# Review pending drafts
mkdocs-ai obelisk cms review
```

---

## Data Models

```python
# mkdocs_ai/obelisk/models.py

@dataclass
class Document:
    """Document for Obelisk."""
    title: str
    content: str
    chunks: list[str]
    embeddings: list[float]
    metadata: dict
    source_path: str

@dataclass
class DocDraft:
    """Draft documentation."""
    title: str
    content: str
    file_path: str
    source_question: str
    related_docs: list[str]
    status: str = "pending"

@dataclass
class DocumentationGap:
    """Identified documentation gap."""
    question: str
    frequency: int
    avg_score: float
    priority: float

@dataclass
class AnalyticsReport:
    """Analytics report."""
    total_questions: int
    common_questions: list[Question]
    documentation_gaps: list[DocumentationGap]
    coverage_score: float
    improvement_suggestions: list[str]
```

---

## Workflow Example

### User Journey

1. **User asks question** in chatbot widget
2. **System searches** existing docs
3. **If no good answer**:
   - AI generates draft documentation
   - Creates GitHub PR
   - Notifies editors
4. **Editor reviews** and approves
5. **Documentation updated** automatically
6. **Future users** get better answers

### Editor Journey

1. **Receives notification** of new draft
2. **Reviews AI-generated content**
3. **Makes edits** if needed
4. **Approves** and merges PR
5. **Documentation improved** for all users

---

## Success Metrics

### Functionality
- [ ] Export docs to Obelisk
- [ ] Chatbot widget works
- [ ] Questions tracked
- [ ] Gaps identified
- [ ] Drafts generated automatically
- [ ] PRs created successfully

### Quality
- [ ] Chatbot answers are accurate
- [ ] Drafts are helpful
- [ ] Gap analysis is insightful
- [ ] PRs are well-formatted

### Impact
- [ ] Reduced repeat questions
- [ ] Improved documentation coverage
- [ ] Faster documentation updates
- [ ] Better user satisfaction

---

## Timeline

### Week 1: Core Implementation (5-6 hours)
- Day 1: Obelisk client (1h)
- Day 2: Documentation exporter (1h)
- Day 3-4: Smart CMS bridge (2h)
- Day 4: Analytics dashboard (1h)
- Day 5: Chatbot widget (1h)

### Week 2: Testing and Polish
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
    "gitpython>=3.1.0",  # NEW: For Git operations
]
```

---

## Conclusion

Priority 5 (Obelisk Integration) enhanced with Smart CMS capabilities will provide:

1. **Interactive Documentation** - Chatbot widget
2. **Continuous Improvement** - Questions → Documentation
3. **Analytics** - Track usage and gaps
4. **Automated Workflows** - Auto-generate drafts
5. **Editor Efficiency** - Review instead of write

**Estimated Effort**: 5-6 hours (worth the enhancement!)

**Next**: Complete Priority 4, then implement Priority 5

---

**Last Updated**: October 17, 2025
