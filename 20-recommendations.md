# Recommendations — AWS Serverless 2026

## The New Paradigm Post-CloudFormation Express

CloudFormation Express mode (June 2026) fundamentally changes the IaC recommendation landscape. The "CloudFormation is too slow" narrative that drove adoption of SST/Terraform/Pulumi is no longer valid.

---

## Primary Recommendation: CDK v2 + Express Mode

For **AWS-only teams** building serverless applications in 2026, **AWS CDK v2 with Express mode** is the strongest overall choice:

| Dimension | CDK v2 + Express |
|-----------|-----------------|
| Speed | `--express` (seconds) + `--hotswap` (instant for Lambda) |
| Type Safety | Full TypeScript/Python/Java with IDE support |
| Abstractions | L2 + L3 constructs reduce boilerplate by 70%+ |
| Compliance | cdk-nag validates security automatically |
| CI/CD | CDK Pipelines (self-mutating, cross-account) |
| Ecosystem | Construct Hub (thousands of community constructs) |
| AI Integration | Largest template corpus for AI-generated infrastructure |
| Maturity | Backed by AWS, used in production across AWS services |

---

## Recommended Stack by Application Type

### 1. Startup MVP / Full-Stack App

```mermaid
flowchart LR
    subgraph Startup["Startup MVP / Full-Stack App"]
        IaC["IaC: SST v3 (or Amplify Gen 2)"]
        FE["Frontend: Next.js"] --> SSTFE["SST Nextjs component (or Amplify Hosting)"]
        API["API: AppSync (GraphQL + real-time)"]
        Auth["Auth: Amazon Cognito"]
        DB["Database: DynamoDB On-Demand"]
        AI["AI: Bedrock (Converse API) + Guardrails"]
        Obs["Observ: Lambda Powertools + Application Signals"]
        Deploy["Deploy: sst deploy (or npx ampx pipeline-deploy)"]
    end
```

**Why:** Fastest time-to-production. SST provides Live Lambda development. Amplify Gen 2 provides even higher abstraction with built-in auth/data/AI.

### 2. Enterprise Application

```mermaid
flowchart LR
    subgraph Enterprise["Enterprise Application"]
        IaC["IaC: AWS CDK v2 + Express Mode"]
        FE["Frontend: Next.js"] --> Hosting["CloudFront + S3 + Lambda (SSR via CDK)"]
        API["API: AppSync (Merged APIs) + API Gateway HTTP API"]
        Auth["Auth: Cognito + IAM (fine-grained)"]
        DB["Database: DynamoDB + Aurora Serverless v2 (reporting)"]
        Cache["Cache: ElastiCache Serverless (Valkey)"]
        Events["Events: EventBridge (Bus + Pipes + Scheduler)"]
        AI["AI: Bedrock Agents + AgentCore (Cedar policies)"]
        Obs["Observ: Powertools + Application Signals + SLOs"]
        Deploy["Deploy: CDK Pipelines + Canary + Manual Approval"]
        Comply["Comply: cdk-nag + Guardrails + WAF"]
    end
```

**Why:** CDK provides type safety, compliance validation, self-mutating CI/CD, and the largest AWS ecosystem. Express mode makes iteration fast. Multi-team support via AppSync Merged APIs.

### 3. Data Processing / Event-Driven System

```mermaid
flowchart LR
    subgraph DataProc["Data Processing / Event-Driven System"]
        IaC["IaC: AWS SAM + Express Mode"]
        Compute["Compute: Lambda (SnapStart + ARM64)"]
        Workflow["Workflow: Step Functions (Distributed Map)"]
        Events["Events: EventBridge (Pipes for CDC, Scheduler for cron)"]
        Data["Data: DynamoDB Streams"] --> Pipe["EventBridge Pipe"] --> Lambda["Lambda"]
        Storage["Storage: S3 Express One Zone (hot data)"]
        AI["AI: Bedrock (summarization, classification)"]
        Obs["Observ: Powertools + X-Ray traces"]
        Deploy["Deploy: SAM Pipelines + Canary deployments"]
    end
```

**Why:** SAM is simplest for Lambda-centric workloads. Express mode + sam sync provides rapid iteration. Step Functions Distributed Map handles massive parallel processing.

### 4. AI Agent Application

```mermaid
flowchart LR
    subgraph AIAgent["AI Agent Application"]
        IaC["IaC: CDK v2 + Express Mode"]
        Agent["Agent: Strands Agents SDK (TypeScript or Python)"]
        Runtime["Runtime: Amazon Bedrock AgentCore Runtime"]
        Tools["Tools: AgentCore Gateway"] --> MCP["Lambda → MCP conversion"]
        RAG["RAG: Bedrock Knowledge Bases + OpenSearch Serverless"]
        Memory["Memory: AgentCore Memory"]
        Safety["Safety: Bedrock Guardrails + Cedar policies"]
        Models["Models: Bedrock (Claude/Nova) + SageMaker Serverless"]
        Obs["Observ: AgentCore Observability + CloudWatch"]
        Deploy["Deploy: CDK Pipelines with security review gates"]
    end
```

**Why:** AgentCore provides production-grade serverless agent execution. Strands is AWS-battle-tested (powers Kiro). CDK manages all infrastructure including agent resources.

### 5. Multi-Cloud / Platform Team

```
IaC:      Terraform (or OpenTofu)
AWS:      Lambda, DynamoDB, EventBridge
GCP/Azure: Comparable services
State:    Terraform Cloud / S3 backend
Modules:  terraform-aws-lambda, custom modules
Testing:  SAM CLI (via Serverless.tf integration)
Deploy:   Terraform Cloud / GitHub Actions
```

**Why:** Only Terraform provides true multi-cloud with a unified language and state management.

---

## Key Decision: CDK vs SAM vs SST

```mermaid
flowchart TD
    Q1{"Do you need frontend framework integration<br/>(Next.js/Astro/Remix)?"}
    Q1 -->|YES| Q2{"Do you need Live Lambda development?"}
    Q1 -->|NO| Q3{"Is your app pure serverless<br/>(Lambda + API + DB)?"}
    
    Q2 -->|YES| SST["SST v3"]
    Q2 -->|NO| Amplify["Amplify Gen 2 (fastest)<br/>or CDK (most control)"]
    
    Q3 -->|YES| Q4{"Do you need enterprise compliance?"}
    Q3 -->|NO| CDK1["CDK v2 + Express<br/>(handles any AWS service)"]
    
    Q4 -->|YES| CDK2["CDK v2 + Express<br/>(cdk-nag, CDK Pipelines)"]
    Q4 -->|NO| SAM["SAM + Express<br/>(simplest, best local testing)"]
```

---

## The Express Mode Development Workflow

```bash
# Morning: Start development
cdk deploy --express          # Deploy full stack in seconds

# During the day: Iterate on Lambda code
cdk deploy --hotswap          # Instant Lambda updates (no CFN)

# Infrastructure changes (add a DynamoDB table, new API route)
cdk deploy --express          # Still seconds, not minutes

# Ready for staging
git push                      # CDK Pipelines auto-deploys to staging
                              # Standard mode (full stabilization)
                              # Canary deployment strategy

# Ready for production
# Manual approval gate in pipeline
# Standard mode + canary + alarms + auto-rollback
```

---

## Principles for 2026

1. **Default serverless** — Use managed services that scale to zero
2. **Express mode for dev, Standard for prod** — Fast iteration, safe deployments
3. **Event-driven architecture** — Decouple via EventBridge, process async
4. **AI-native** — Every app should integrate Bedrock (just an API call)
5. **MCP as tool standard** — Build tools as Lambda, expose via AgentCore Gateway
6. **Observe everything** — Powertools + Application Signals = zero-effort APM
7. **Deploy safely** — Canary via CodeDeploy, never all-at-once
8. **Cost-optimize** — ARM64, SnapStart, Valkey, HTTP API, scales-to-zero services
9. **Compliance as code** — cdk-nag + Guardrails + Cedar policies
10. **AI-assisted development** — Use Express mode feedback loops with Kiro

---

## What CloudFormation Express Means for the Ecosystem

### Winners
- **CDK** — Gains speed without losing anything. Now has best overall package.
- **SAM** — Simple + fast. Perfect for serverless microservices.
- **CloudFormation native** — Direct templates now deploy in seconds.
- **AI agents** — Sub-minute feedback loops enable rapid infrastructure iteration.

### Repositioned
- **SST v3** — Live Lambda remains unique, but speed is no longer a differentiator.
- **Terraform** — Multi-cloud is its story now, not speed.
- **Pulumi** — Code-first without CFN opinions, but CDK offers similar with bigger ecosystem.

### The Bottom Line

> In 2026, there is no longer a compelling speed reason to avoid CloudFormation-based tools.
> CDK + Express mode gives you: fast deployments + type safety + L2/L3 abstractions + 
> compliance validation + self-mutating CI/CD + the largest AWS ecosystem.
>
> Choose SST v3 for Live Lambda DX. Choose Terraform for multi-cloud. 
> Choose CDK for everything else.
