# Local LLM Model Capability Matrix

Comprehensive reference for model selection in air-gapped/local environments. **Updated January 2025**.

## Quick Reference

### By Task Type

| Task | Tier 1 (Best) | Tier 2 (Good) | Tier 3 (Basic) |
|------|---------------|---------------|----------------|
| **Coding** | DeepSeek-V3, Qwen2.5-Coder-32B | Qwen2.5-Coder-14B, Phi-4 | Qwen2.5-Coder-7B, CodeLlama-7B |
| **Reasoning** | DeepSeek-R1, DeepSeek-V3 | DeepSeek-R1-Distill-32B, Phi-4 | DeepSeek-R1-Distill-8B, Gemma-2-9B |
| **Analysis** | DeepSeek-V3 + Serena, Qwen2.5-Coder-32B | CodeLlama-34B-Instruct | - |
| **Documentation** | Qwen2.5-72B-Instruct, Llama-3.3-70B | Mistral-Small-24B | Mistral-Nemo-12B |

### By VRAM Requirement

| VRAM | Models |
|------|--------|
| **3-6 GB** | Llama-3.2-3B, DeepSeek-R1-Distill-8B, Qwen2.5-Coder-7B |
| **7-10 GB** | Gemma-2-9B, Phi-4, DeepSeek-R1-Distill-14B, Qwen2.5-Coder-14B |
| **16-22 GB** | Mistral-Small-24B, Qwen2.5-Coder-32B, DeepSeek-R1-Distill-32B |
| **40-48 GB** | DeepSeek-V3, Llama-3.3-70B, Qwen2.5-72B, DeepSeek-R1-Distill-70B |
| **160+ GB** | DeepSeek-R1 (full) |

---

## Top Performing Models (2024-2025)

### DeepSeek-V3 (BEST OVERALL)
- **Parameters**: 685B MoE (37B active)
- **Context Window**: 128,000 tokens
- **VRAM Required**: 48 GB (Q4 quantized)
- **Strengths**: #1 open model, rivals GPT-4, excellent at coding
- **Best For**: Complex coding, reasoning, analysis
- **Ollama**: `ollama pull deepseek-v3`

### DeepSeek-R1 (BEST REASONING)
- **Parameters**: 671B
- **Context Window**: 128,000 tokens
- **VRAM Required**: 160 GB (full) / 48 GB (distilled)
- **Strengths**: Chain-of-thought reasoning, matches o1
- **Best For**: Complex problem solving, step-by-step reasoning
- **Distill Variants**: 70B, 32B, 14B, 8B, 7B, 1.5B

### Qwen2.5-Coder-32B (BEST CODING)
- **Parameters**: 32B
- **Context Window**: 131,072 tokens
- **VRAM Required**: 22 GB
- **Strengths**: State-of-the-art code generation
- **Best For**: Code completion, debugging, refactoring
- **Ollama**: `ollama pull qwen2.5-coder:32b`

---

## Coding Specialists

### Tier 1 - Best Performance

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| DeepSeek-V3 | 128K | 48 GB | `ollama pull deepseek-v3` |
| Qwen2.5-Coder-32B | 131K | 22 GB | `ollama pull qwen2.5-coder:32b` |
| DeepSeek-Coder-V2 | 128K | 48 GB | `ollama pull deepseek-coder-v2` |

### Tier 2 - Good Balance

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| Qwen2.5-Coder-14B | 131K | 10 GB | `ollama pull qwen2.5-coder:14b` |
| CodeLlama-34B | 100K | 20 GB | `ollama pull codellama:34b` |
| Phi-4 | 16K | 10 GB | `ollama pull phi4` |
| StarCoder2-15B | 16K | 10 GB | `ollama pull starcoder2:15b` |

### Tier 3 - Minimal Resources

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| Qwen2.5-Coder-7B | 131K | 5 GB | `ollama pull qwen2.5-coder:7b` |
| DeepSeek-Coder-6.7B | 16K | 5 GB | `ollama pull deepseek-coder:6.7b` |
| CodeLlama-7B | 16K | 5 GB | `ollama pull codellama:7b` |

---

## Reasoning Specialists

### Tier 1 - Best Performance

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| DeepSeek-R1 | 128K | 160 GB | `ollama pull deepseek-r1` |
| DeepSeek-V3 | 128K | 48 GB | `ollama pull deepseek-v3` |
| DeepSeek-R1-Distill-70B | 128K | 42 GB | `ollama pull deepseek-r1:70b` |
| Qwen2.5-72B-Instruct | 131K | 48 GB | `ollama pull qwen2.5:72b-instruct` |
| Llama-3.3-70B-Instruct | 128K | 42 GB | `ollama pull llama3.3:70b` |

### Tier 2 - Good Balance

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| DeepSeek-R1-Distill-32B | 128K | 22 GB | `ollama pull deepseek-r1:32b` |
| Mistral-Small-24B | 32K | 16 GB | `ollama pull mistral-small` |
| Qwen2.5-32B-Instruct | 131K | 22 GB | `ollama pull qwen2.5:32b-instruct` |
| Phi-4 | 16K | 10 GB | `ollama pull phi4` |
| Gemma-2-27B | 8K | 18 GB | `ollama pull gemma2:27b` |

### Tier 3 - Minimal Resources

| Model | Context | VRAM | Ollama Command |
|-------|---------|------|----------------|
| DeepSeek-R1-Distill-14B | 128K | 10 GB | `ollama pull deepseek-r1:14b` |
| DeepSeek-R1-Distill-8B | 128K | 6 GB | `ollama pull deepseek-r1:8b` |
| Gemma-2-9B | 8K | 7 GB | `ollama pull gemma2:9b` |
| Llama-3.2-3B | 128K | 3 GB | `ollama pull llama3.2:3b` |

---

## Analysis Specialists

> **Note**: Analysis tasks REQUIRE Serena MCP for semantic code understanding

| Model | VRAM | Best For | Requires Serena |
|-------|------|----------|-----------------|
| DeepSeek-V3 | 48 GB | Deep security audits | Yes |
| Qwen2.5-Coder-32B | 22 GB | Code review | Yes |
| DeepSeek-Coder-V2 | 48 GB | Vulnerability analysis | Yes |
| CodeLlama-34B-Instruct | 20 GB | General analysis | Yes |

---

## Documentation Specialists

| Model | VRAM | Best For | Ollama Command |
|-------|------|----------|----------------|
| Qwen2.5-72B-Instruct | 48 GB | Technical docs, API refs | `ollama pull qwen2.5:72b-instruct` |
| Llama-3.3-70B-Instruct | 42 GB | Clear, natural writing | `ollama pull llama3.3:70b` |
| Qwen2.5-32B-Instruct | 22 GB | Efficient docs | `ollama pull qwen2.5:32b-instruct` |
| Mistral-Small-24B | 16 GB | Quick docs | `ollama pull mistral-small` |
| Mistral-Nemo-12B | 8 GB | Comments, docstrings | `ollama pull mistral-nemo` |

---

## Model Families

### DeepSeek (Recommended)
- **DeepSeek-V3**: Best overall, MoE architecture (685B/37B active)
- **DeepSeek-R1**: Best reasoning, chain-of-thought
- **DeepSeek-Coder-V2**: Excellent coding, MoE (236B/21B active)
- **Distill variants**: R1 distilled to 70B/32B/14B/8B/7B/1.5B

### Qwen (Alibaba)
- **Qwen2.5-Coder**: State-of-the-art coding (32B/14B/7B)
- **Qwen2.5-Instruct**: General purpose (72B/32B/14B/7B)
- **Huge context**: 131K tokens standard

### Llama (Meta)
- **Llama-3.3-70B**: Strong all-around
- **Llama-3.2**: Vision support (11B/3B)
- **CodeLlama**: Specialized for code (70B/34B/7B)

### Mistral
- **Mistral-Small-24B**: New efficient model
- **Mistral-Nemo-12B**: Good documentation
- **Mixtral-8x22B**: MoE, diverse expertise

### Google
- **Gemma-2-27B**: Good balance
- **Gemma-2-9B**: Efficient small model

### Microsoft
- **Phi-4**: Punches above weight, 14B params

---

## Quantization Guide

### Quantization Levels

| Level | Quality Loss | VRAM Savings | Recommended Use |
|-------|--------------|--------------|-----------------|
| FP16 | 0% | Baseline | Maximum quality |
| Q8_0 | ~1% | 50% | Best quantized quality |
| Q6_K | ~2% | 60% | Good balance |
| Q5_K_M | ~3% | 65% | **Recommended** |
| Q4_K_M | ~5% | 70% | VRAM constrained |
| Q3_K_M | ~10% | 75% | Extreme constraint |

### Recommended Quantizations

| Model | Full VRAM | Q4_K_M VRAM | Recommended |
|-------|-----------|-------------|-------------|
| DeepSeek-V3 | 140 GB | 48 GB | Q4_K_M |
| Qwen2.5-72B | 145 GB | 48 GB | Q4_K_M |
| DeepSeek-R1-70B | 140 GB | 42 GB | Q4_K_M |
| Qwen2.5-Coder-32B | 65 GB | 22 GB | Q5_K_M |
| Llama-3.3-70B | 140 GB | 42 GB | Q4_K_M |

---

## Hardware Recommendations

### Minimal Setup (8 GB VRAM)
- **GPU**: RTX 3060 12GB, RTX 4060 8GB
- **Models**: 7B-14B models
- **Tasks**: Basic coding, quick tasks

### Standard Setup (24 GB VRAM)
- **GPU**: RTX 3090, RTX 4090
- **Models**: 32B models, 70B Q4 quantized
- **Tasks**: Full coding, analysis, docs

### Professional Setup (48+ GB VRAM)
- **GPU**: A6000, 2x RTX 4090
- **Models**: DeepSeek-V3, 70B+ full
- **Tasks**: Complex reasoning, deep analysis

### Enterprise Setup (Multi-GPU)
- **GPU**: 4x A100, 8x H100
- **Models**: DeepSeek-R1 full, 200B+
- **Tasks**: Frontier-level capabilities

---

## Supported Services

| Service | Port | API Style | Install |
|---------|------|-----------|---------|
| Ollama | 11434 | Native | `brew install ollama` |
| LM Studio | 1234 | OpenAI | Download from lmstudio.ai |
| Jan | 1337 | OpenAI | Download from jan.ai |
| vLLM | 8000 | OpenAI | `pip install vllm` |
| llama.cpp | 8080 | OpenAI | Build from source |
| LocalAI | 8080 | OpenAI | Docker or binary |
| Kobold.cpp | 5001 | Custom | Build from source |
| GPT4All | 4891 | OpenAI | Download from gpt4all.io |
| OpenWebUI | 3000 | Custom | Docker |

---

## Service-Specific Notes

### Ollama (Recommended)
```bash
# Install
curl -fsSL https://ollama.ai/install.sh | sh

# Pull top models
ollama pull deepseek-v3
ollama pull qwen2.5-coder:32b
ollama pull deepseek-r1:32b
ollama pull phi4

# Start server
ollama serve
```

### vLLM (Production)
```bash
# Install
pip install vllm

# Run server
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/deepseek-v3 \
    --tensor-parallel-size 2
```

### LM Studio
- Download from https://lmstudio.ai
- GUI for model management
- Easy quantization selection
- Built-in server

---

## Quick Selection Guide

**"I have 8GB VRAM, what should I use for coding?"**
- Qwen2.5-Coder-7B or DeepSeek-Coder-6.7B

**"I have 24GB VRAM, best overall model?"**
- Qwen2.5-Coder-32B for coding
- DeepSeek-R1-Distill-32B for reasoning

**"I have 48GB VRAM, maximum performance?"**
- DeepSeek-V3 (Q4_K_M quantization)

**"I need reasoning/chain-of-thought?"**
- DeepSeek-R1 or any DeepSeek-R1-Distill variant

**"I need fast inference for IDE completions?"**
- Phi-4 or Qwen2.5-Coder-7B

**"I'm in an air-gapped environment?"**
- Pre-download models with checksums
- Use Ollama or llama.cpp (no cloud dependencies)
- Enable Serena LSP for code intelligence
