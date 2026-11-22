# Token Usage Optimization Strategy

## Current Token Usage Analysis

**Baseline per request**: ~3,000-4,000 tokens
- Search agent: ~1,000 tokens
- Research agent: ~1,500 tokens  
- Article editor: ~500 tokens
- Final article generator: ~500 tokens

**Goal**: Reduce to ~1,500-2,000 tokens per request (50% reduction)

---

## Optimization Strategies

### 1. Prompt Compression
- Remove redundant instructions
- Use bullet points instead of paragraphs
- Eliminate examples from prompts
- Keep only essential context

### 2. Response Limiting
- Set max_tokens parameter on API calls
- Limit search results to top 2 instead of 3
- Reduce intermediate processing steps

### 3. Caching Strategy
- Cache search results for same topic+country (1 hour TTL)
- Reuse research findings across requests
- Store generated articles for similar queries

### 4. Agent Consolidation
- Combine search + research into single agent
- Reduce sequential processing steps
- Eliminate redundant context passing

### 5. Model Selection
- Use gemini-2.5-flash-lite (already done) ✅
- Consider gemini-1.5-flash for future optimization

---

## Implementation Priority

1. **High Impact** (Implement First)
   - Reduce search results from 3 to 2 articles
   - Compress search agent prompt (20% reduction)
   - Add response token limits

2. **Medium Impact** (Implement Second)
   - Implement basic caching for search results
   - Compress research agent prompt
   - Reduce intermediate logging

3. **Low Impact** (Implement Later)
   - Advanced caching with semantic similarity
   - Agent consolidation
   - Model switching logic

---

## Expected Results

| Strategy | Token Savings | Implementation Time |
|----------|---------------|-------------------|
| Reduce search results (3→2) | 300-400 tokens | 5 minutes |
| Compress prompts | 400-600 tokens | 15 minutes |
| Add token limits | 200-300 tokens | 10 minutes |
| Basic caching | 1000+ tokens | 30 minutes |
| **Total Potential** | **1900-2300 tokens** | **60 minutes** |

---

## Implementation Steps

### Step 1: Reduce Search Results
Edit `search_agent/prompt.py`:
- Change "top 3" to "top 2"
- Reduce output format accordingly

### Step 2: Compress Prompts
- Remove verbose explanations
- Use concise bullet points
- Keep only critical instructions

### Step 3: Add Token Limits
Update agent configurations:
```python
max_output_tokens=500  # Limit response size
```

### Step 4: Implement Caching
Create simple cache layer:
```python
cache = {}  # {topic+country: results}
cache_ttl = 3600  # 1 hour
```

---

## Monitoring

Track token usage with `/token-stats` endpoint:
```bash
curl http://localhost:8000/token-stats
```

Expected improvement: 50% reduction in tokens per request
