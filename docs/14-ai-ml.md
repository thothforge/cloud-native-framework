# AI/ML Integration — AWS Serverless 2026

## The Agentic AI Era

2026 marks the year AI agents became first-class serverless citizens on AWS. The stack has evolved from "call an LLM API" to "deploy autonomous AI agents at scale."

## Architecture Overview

```mermaid
graph TD
    subgraph APP["APPLICATION LAYER"]
        A1["Strands Agents SDK (Python/TypeScript) — build agents"]
        A2["Amazon Bedrock Agents — managed agent orchestration"]
    end
    subgraph RUNTIME["RUNTIME LAYER"]
        R1["AgentCore Runtime — serverless, secure, scalable execution"]
        R2["AgentCore Gateway — MCP tool discovery and conversion"]
        R3["AgentCore Memory — short-term + long-term agent memory"]
    end
    subgraph MODEL["MODEL LAYER"]
        M1["Amazon Bedrock — Foundation models (Claude, Nova, Llama, etc)"]
        M2["SageMaker Serverless — Custom-trained ML models"]
    end
    subgraph SAFETY["SAFETY & GOVERNANCE"]
        S1["Bedrock Guardrails — content filters, PII masking, topics"]
        S2["AgentCore Identity — Cedar policies for agent authorization"]
        S3["AgentCore Observability — OpenTelemetry traces via CloudWatch"]
    end
    APP --> RUNTIME --> MODEL --> SAFETY
```

---

## 1. Amazon Bedrock — Foundation Models

Fully managed, serverless access to foundation models via a single API.

### Available Models (2026)
- **Anthropic:** Claude 3.5 Sonnet, Claude 3 Opus/Haiku
- **Amazon:** Nova Micro, Nova Lite, Nova Pro
- **Meta:** Llama 3.x
- **Mistral AI:** Mistral Large, Mixtral
- **DeepSeek, Cohere, AI21 Labs, Stability AI, Luma**

### Key Features
- **Pay-per-token** — no provisioning
- **Converse API** (recommended) — unified interface across models
- **Response streaming** — real-time token delivery
- **Cross-region inference** — automatic routing during peak utilization
- **No infrastructure management**

### Lambda Integration Pattern

```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime")

def handler(event, context):
    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": event["prompt"]}]
        }],
        inferenceConfig={"maxTokens": 1024, "temperature": 0.7}
    )
    return response["output"]["message"]["content"][0]["text"]
```

---

## 2. Amazon Bedrock Agents

Managed AI agents that understand requests, break down tasks, and orchestrate actions.

### Capabilities
- **Action Groups:** Interact with external systems via APIs (Lambda functions)
- **Knowledge Bases (RAG):** Connect to S3/Redshift data for grounded responses
- **Multi-Agent Collaboration (GA March 2025):** Multiple agents coordinate on complex workflows
- **Inline Agents:** Dynamically adjust agent roles at runtime
- **MCP Support:** Connect to Model Context Protocol servers for tool access

### RAG Pattern

```mermaid
flowchart TD
    UQ[User Query] --> BA[Bedrock Agent]
    BA --> KB[Knowledge Base]
    KB --> VDB[Vector DB - OpenSearch/Pinecone]
    VDB --> RC[Retrieve relevant chunks]
    RC --> FM[Foundation Model - with context]
    FM --> GR[Grounded Response with Citations]
```

### Setting Up Knowledge Bases
1. Upload documents to S3
2. Configure Knowledge Base (embedding model, vector store, chunking strategy)
3. Run ingestion job (StartIngestionJob API)
4. Connect to agent or query directly

---

## 3. Amazon Bedrock AgentCore (2025-2026)

Enterprise-grade platform to **build, deploy, and operate agents** at scale using any framework.

### Core Services

| Service | Purpose |
|---------|---------|
| **AgentCore Runtime** | Serverless execution with session isolation, long-running task support |
| **AgentCore Gateway** | Converts Lambda/APIs to MCP-compatible tools; tool discovery |
| **AgentCore Memory** | Managed short-term (conversation) + long-term memory |
| **AgentCore Identity** | Agent-specific IAM with Cedar policy authorization |
| **AgentCore Built-in Tools** | Code Interpreter (sandbox), Browser Tool (web at scale) |
| **AgentCore Observability** | OpenTelemetry traces → CloudWatch |

### Key Insight: Framework Agnostic
AgentCore works with **any** agent framework:
- Strands Agents SDK
- LangGraph
- CrewAI
- LlamaIndex
- Custom frameworks

And **any** model:
- Bedrock models
- Models outside Bedrock (OpenAI, self-hosted)

---

## 4. Strands Agents SDK — Open Source (1.0 GA)

The model-driven agent SDK used in production by Kiro, AWS Glue, VPC Reachability Analyzer.

### Key Facts
- **2,000+ GitHub stars**, 150K+ PyPI downloads
- **Python** and **TypeScript** (RC since April 2026)
- **Version 1.0** — production-ready with stability guarantees
- Used internally across AWS services

### Core Philosophy
Model-driven: Give the model tools and a prompt → it plans, chains thoughts, calls tools, and reflects. Strands manages the event loop.

### Minimal Agent

```python
from strands import Agent
from strands.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Call weather API
    return f"72°F, sunny in {city}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    # Send via SES
    return f"Email sent to {to}"

agent = Agent(
    system_prompt="You are a helpful assistant that can check weather and send emails.",
    tools=[get_weather, send_email]
)

response = agent("What's the weather in Seattle? If it's nice, email john@example.com about it.")
```

### 1.0 Features (2026)
- **Multi-agent orchestration** — 4 new coordination primitives
- **Agent-to-Agent (A2A) protocol** — agents communicate with each other
- **Session Manager** — remote state persistence
- **Improved async support** throughout
- **5+ model providers** — Anthropic, Meta, OpenAI, Cohere, Mistral, Stability, Writer

### Deployment to AgentCore

```python
from strands import Agent
# Build agent locally
agent = Agent(system_prompt="...", tools=[...])

# Deploy to AgentCore Runtime for production
# → Serverless execution
# → Session isolation
# → Auto-scaling
# → Cedar policy authorization
# → OpenTelemetry observability
```

---

## 5. Bedrock Guardrails

Configurable safety policies applied consistently across all AI interactions.

### Policy Types

| Policy | Function |
|--------|----------|
| **Content filters** | Block hate, insults, sexual, violence (configurable thresholds) |
| **Denied topics** | Block specific topics via natural language description |
| **Word filters** | Block words, phrases, profanity |
| **Sensitive info** | Block or mask PII (built-in types + custom regex) |
| **Image filters** | Filter harmful image content |

### How It Works
```mermaid
flowchart TD
    Input --> GR1[Guardrails - parallel policy evaluation]
    GR1 -->|PASS| Model[Model processes request]
    GR1 -->|FAIL| Blocked1[Return blocked message - model never sees input]
    Model --> Response
    Response --> GR2[Guardrails - output evaluation]
    GR2 -->|PASS| Return[Return to user]
    GR2 -->|FAIL| Blocked2[Return blocked message / mask PII]
```

### Apply to Any Model
```python
# Works with Converse, InvokeModel, Agents, Knowledge Bases
response = bedrock.converse(
    modelId="...",
    messages=[...],
    guardrailConfig={
        "guardrailIdentifier": "my-guardrail-id",
        "guardrailVersion": "1"
    }
)

# Also works with self-hosted models via ApplyGuardrail API
```

---

## 6. SageMaker Serverless Inference

For **custom-trained** ML models with intermittent traffic.

### When to Use (vs Bedrock)

| Dimension | Bedrock | SageMaker Serverless |
|-----------|---------|---------------------|
| Model type | Foundation models (LLMs) | Custom-trained models |
| Setup | Minimal (API call) | Requires model training/packaging |
| Use case | Generative, conversational | Predictive, numerical, structured |
| Scaling | Always available | Scales to zero (cold starts) |
| Cost | Pay per token | Pay per inference |

### Best For
- Custom classification/regression models
- Proprietary algorithms
- Structured data prediction
- Intermittent traffic patterns (scales to zero)

---

## 7. Serverless AI Services (Pre-trained)

| Service | Capability | Use Case |
|---------|------------|----------|
| **Comprehend** | NLP (sentiment, entities, key phrases) | Text analysis pipelines |
| **Rekognition** | Computer vision (objects, faces, content moderation) | Image/video processing |
| **Textract** | Document processing (tables, forms, handwriting) | Document automation |

All integrate directly with Lambda for event-driven AI pipelines:
```mermaid
flowchart LR
    S3[S3 - document upload] --> Lambda --> Textract --> DDB[DynamoDB - structured data]
```

---

## Architecture Patterns

### Pattern 1: RAG Application (Serverless)
```mermaid
flowchart LR
    User --> APIGW[API Gateway] --> Lambda --> Agent[Bedrock Agent]
    Agent --> KB[Knowledge Base - S3 → OpenSearch Serverless]
    Agent --> AG[Action Group - Lambda → DynamoDB]
    Agent --> Guard[Guardrails - safety check]
    Guard --> GR[Grounded Response with Citations]
```

### Pattern 2: Multi-Agent System
```mermaid
flowchart TD
    User --> Supervisor[Supervisor Agent - Strands]
    Supervisor --> Research[Research Agent - web search, knowledge base]
    Supervisor --> Analysis[Analysis Agent - data processing, SageMaker]
    Supervisor --> Action[Action Agent - send emails, update records]
    
    subgraph Infrastructure
        ACR[AgentCore Runtime - All deployed here]
        ACG[AgentCore Gateway - Tools exposed via MCP]
        ACM[AgentCore Memory - State persisted here]
    end
```

### Pattern 3: Event-Driven AI Pipeline
```mermaid
flowchart TD
    Doc[Document] --> S3 --> EB[EventBridge] --> L1[Lambda] --> Textract[Textract - extract]
    Textract --> L2[Lambda] --> Bedrock[Bedrock - summarize]
    Bedrock --> L3[Lambda] --> Comprehend[Comprehend - classify]
    Comprehend --> L4[Lambda] --> DDB[DynamoDB - store]
    DDB --> AppSync[AppSync - notify user]
```

---

## Key Principles for AI in Serverless (2026)

1. **Every app should integrate Bedrock** — it's just an API call with pay-per-token
2. **Use Guardrails on every AI interaction** — safety is not optional
3. **MCP is the tool standard** — expose Lambda functions as MCP tools via AgentCore Gateway
4. **Strands for custom agents** — production-ready, used by AWS internally
5. **AgentCore for deployment** — don't run agents on raw Lambda, use the managed runtime
6. **RAG for grounded responses** — Knowledge Bases + OpenSearch Serverless for vector search
7. **Cedar policies govern agent actions** — fine-grained authorization for production agents
8. **Observe agent behavior** — OpenTelemetry traces show every tool call, every decision
