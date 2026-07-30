# Reference Architecture — Full Serverless Application 2026

## Complete Stack Diagram

```mermaid
flowchart TD
    EDGE["<b>EDGE LAYER</b><br/>CloudFront CDN + CloudFront Functions KVS + Lambda@Edge"]
    FRONTEND["<b>FRONTEND LAYER</b><br/>Next.js/Astro → Amplify Hosting or SST (S3 + CloudFront + Lambda)"]
    API["<b>API LAYER</b><br/>AppSync (GraphQL + Subscriptions) │ API Gateway HTTP API (REST)<br/>Lambda Function URLs (webhooks) │ AppSync Events (PubSub)"]
    COMPUTE["<b>COMPUTE LAYER</b><br/>Lambda (SnapStart + ARM64) │ Step Functions │ ECS + Fargate"]
    AIML["<b>AI/ML LAYER</b><br/>Bedrock (FMs) → AgentCore Runtime → Strands Agents<br/>Guardrails │ Knowledge Bases (RAG) │ AgentCore Gateway (MCP Tools)"]
    EVENTS["<b>EVENT BACKBONE</b><br/>EventBridge (Bus + Pipes + Scheduler) │ SNS/SQS │ VPC Lattice"]
    DATA["<b>DATA LAYER</b><br/>DynamoDB │ Aurora Serverless v2 │ ElastiCache Serverless (Valkey)<br/>OpenSearch Serverless │ S3 Express │ Timestream"]
    AUTH["<b>AUTH & SECURITY</b><br/>Amazon Cognito │ IAM │ Secrets Manager │ WAF │ Shield"]
    OBS["<b>OBSERVABILITY</b><br/>Powertools │ X-Ray │ Application Signals │ Logs Insights"]
    IAC["<b>IaC & DEPLOYMENT</b><br/>CDK + Express Mode │ CDK Pipelines │ Canary Deploys │ Evidently"]

    EDGE --> FRONTEND
    FRONTEND --> API
    API --> COMPUTE
    COMPUTE --> AIML
    AIML --> EVENTS
    EVENTS --> DATA
    DATA --> AUTH
    AUTH --> OBS
    OBS --> IAC
```

---

## Example: E-Commerce Application

### Synchronous Flow (User-Facing)

```mermaid
flowchart LR
    Browser --> CloudFront["CloudFront<br/>(static assets + Functions for A/B testing)"]
    CloudFront --> NextJS["Next.js SSR → Lambda<br/>(server-side rendering)"]
    CloudFront --> AppSync["AppSync (GraphQL API)"]
    CloudFront --> Auth["Auth → Cognito<br/>(social login + MFA)"]

    AppSync --> Products["Product catalog queries → DynamoDB"]
    AppSync --> Search["Search → OpenSearch Serverless"]
    AppSync --> Cart["Cart operations → DynamoDB"]
    AppSync --> AI["AI recommendations → Lambda → Bedrock"]
    AppSync --> Realtime["Real-time order updates → Subscriptions"]
```

### Asynchronous Flow (Backend Processing)

```mermaid
flowchart TD
    Order["Order Placed (DynamoDB write)"]
    Order --> Stream["DynamoDB Stream → EventBridge Pipe"]
    Stream --> Filter["Filter (only new orders)"]
    Stream --> SF["Target: Step Functions<br/>(Order Processing Workflow)"]

    SF --> Step1["Step 1: Validate inventory (Lambda)"]
    SF --> Step2["Step 2: Process payment (Lambda → Stripe)"]
    SF --> Step3["Step 3: Reserve stock (Lambda → DynamoDB)"]
    SF --> Step4["Step 4: Send confirmation (Lambda → SES)"]
    SF --> Step5["Step 5: Emit OrderCompleted → EventBridge"]

    Step5 --> EB["EventBridge OrderCompleted event"]
    EB --> Rule1["Rule → SQS → Lambda<br/>(update analytics in Timestream)"]
    EB --> Rule2["Rule → Lambda<br/>(notify warehouse via VPC Lattice)"]
    EB --> Rule3["Rule → Lambda<br/>(AI agent generates shipping estimate)"]

    Scheduler["EventBridge Scheduler"]
    Scheduler --> Daily["Daily: Generate sales reports → Lambda → S3"]
    Scheduler --> Hourly["Hourly: Sync inventory → Lambda → DynamoDB"]
    Scheduler --> Every5["Every 5 min: Process abandoned carts → Lambda → SES"]
```

### AI Layer

```mermaid
flowchart TD
    Agent["Customer Service AI Agent<br/>(Strands + AgentCore)"]
    Agent --> KB["Knowledge Base: Product manuals, FAQ<br/>(S3 → OpenSearch vectors)"]
    Agent --> Action1["Action Group: Check order status<br/>(Lambda → DynamoDB)"]
    Agent --> Action2["Action Group: Initiate return<br/>(Lambda → Step Functions)"]
    Agent --> Guard["Guardrails: No PII leakage,<br/>no competitor discussions"]
    Agent --> Memory["Memory: Conversation history per session"]
```

---

## Example: SaaS Platform

### Multi-Tenant Architecture

```mermaid
flowchart LR
    TenantA["Tenant A"] --> APIGW["API Gateway"]
    TenantB["Tenant B"] --> APIGW
    TenantC["Tenant C"] --> APIGW
    APIGW --> Lambda["Lambda<br/>(tenant isolation via Cognito claims)"]
    Lambda --> DDB["DynamoDB<br/>(partition key = tenant_id)"]
    Lambda --> S3["S3<br/>(prefix = tenant_id/)"]
    Lambda --> Cache["ElastiCache<br/>(namespace = tenant_id)"]

    Admin["Admin Panel"] --> Merged["AppSync Merged API"]
    Merged --> Billing["Source API: Billing<br/>(Team A's AppSync)"]
    Merged --> Analytics["Source API: Analytics<br/>(Team B's AppSync)"]
    Merged --> UserMgmt["Source API: User Management<br/>(Team C's AppSync)"]

    BGJobs["Background Jobs → EventBridge Scheduler"]
    BGJobs --> Metering["Per-tenant: Usage metering<br/>(Lambda → Timestream)"]
    BGJobs --> Invoice["Per-tenant: Invoice generation<br/>(Step Functions)"]
    BGJobs --> Health["Global: System health checks<br/>(Lambda → CloudWatch)"]
```

---

## Example: IoT / Real-Time Dashboard

```mermaid
flowchart TD
    IoT["IoT Devices"] --> IoTCore["IoT Core"] --> Kinesis["Kinesis Data Streams"]
    Kinesis --> Pipe["EventBridge Pipe<br/>(filter + enrich)"]
    Pipe --> Process["Lambda<br/>(process + aggregate)"]
    Process --> Timestream["Timestream<br/>(store time-series)"]
    Process --> DDB["DynamoDB<br/>(latest device state)"]
    Process --> AppSyncEvents["AppSync Events<br/>(push to dashboard via WebSocket)"]

    Dashboard["Dashboard (React)"] --> PubSub["AppSync Events (real-time PubSub)"]
    PubSub --> Telemetry["Device telemetry feed"]
    PubSub --> Alerts["Alert notifications"]
    PubSub --> Historical["Historical queries → Timestream via Lambda"]

    AIAgent["AI Anomaly Agent<br/>(Strands + AgentCore)"]
    AIAgent --> Tool1["Tool: Query Timestream (Lambda)"]
    AIAgent --> Tool2["Tool: Get device metadata<br/>(Lambda → DynamoDB)"]
    AIAgent --> Tool3["Tool: Send alert (Lambda → SNS)"]
    AIAgent --> Trigger["Triggered by: EventBridge rule<br/>(anomaly pattern detected)"]
```

---

## IaC Implementation (CDK + Express)

### Project Structure

```
my-app/
├── bin/
│   └── app.ts                    # CDK app entry point
├── lib/
│   ├── stacks/
│   │   ├── api-stack.ts          # AppSync / API Gateway
│   │   ├── compute-stack.ts      # Lambda functions
│   │   ├── data-stack.ts         # DynamoDB, Aurora, ElastiCache
│   │   ├── events-stack.ts       # EventBridge, SQS
│   │   ├── ai-stack.ts           # Bedrock, AgentCore
│   │   ├── frontend-stack.ts     # CloudFront, S3, hosting
│   │   └── observability-stack.ts # Alarms, dashboards
│   ├── constructs/
│   │   ├── secure-api.ts         # L3: API + WAF + Auth
│   │   └── event-processor.ts    # L3: SQS + DLQ + Lambda
│   └── pipeline-stack.ts         # CDK Pipelines CI/CD
├── lambda/
│   ├── api/                      # API handler functions
│   ├── events/                   # Event processing functions
│   └── ai/                       # AI agent action handlers
├── frontend/
│   └── next-app/                 # Next.js application
├── cdk.json
└── package.json
```

### Development Commands

```bash
# Development iteration (seconds with Express mode)
cdk deploy --express

# Lambda code only (instant, bypasses CloudFormation)
cdk deploy --hotswap

# Production deployment (full stabilization + canary)
cdk deploy  # via CDK Pipelines with approval gates

# Destroy dev environment
cdk destroy --express
```

---

## Cost Optimization Strategies

| Strategy | Savings | Applies To |
|----------|---------|------------|
| ARM64/Graviton | ~20% | Lambda |
| SnapStart | Free cold start fix | Lambda (Python/Java/.NET) |
| Valkey over Redis | 33% | ElastiCache Serverless |
| HTTP API over REST API | 70% | API Gateway |
| Express Workflows | Per-execution vs per-transition | Step Functions |
| On-Demand over Provisioned | Avoid idle capacity | DynamoDB |
| Scales-to-zero | No idle costs | OpenSearch, ElastiCache, Aurora |
| EventBridge Scheduler | 14M free/month | Scheduled tasks |
| CloudFront Functions over Lambda@Edge | Fraction of cost | Edge compute |

---

## Security Best Practices

1. **Least privilege IAM** — scoped per-function, per-resource
2. **WAF on all public APIs** — rate limiting, geo-blocking, bot mitigation
3. **Cognito for auth** — MFA enabled, short token expiration
4. **Secrets Manager** — no hardcoded secrets, automatic rotation
5. **VPC for sensitive workloads** — Lambda in VPC when accessing RDS/ElastiCache
6. **Guardrails on all AI** — prevent data leakage and prompt injection
7. **Cedar policies for agents** — fine-grained agent action authorization
8. **cdk-nag** — automated security validation at build time
9. **Encryption everywhere** — at-rest (KMS) and in-transit (TLS)
10. **DLQs on all async processing** — no lost messages
