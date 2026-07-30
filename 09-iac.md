# Infrastructure as Code (IaC) — AWS Serverless 2026

## The New Landscape Post-CloudFormation Express

With CloudFormation Express mode (June 2026), the IaC landscape has fundamentally shifted. Speed — once CloudFormation's weakness — is now competitive with direct-API tools.

## Tool Comparison

| Tool | Deploy Speed | Local Dev | DX | Community | Best For |
|------|-------------|-----------|-----|-----------|----------|
| **CDK v2 + Express** | ⭐⭐⭐⭐⭐ | Good (via SAM) | ⭐⭐⭐⭐ | Largest AWS | Enterprise, type-safe, compliance |
| **SAM + Express** | ⭐⭐⭐⭐⭐ | Best emulation | ⭐⭐⭐⭐ | Large | Pure serverless, simplest path |
| **SST v3 (Ion)** | ⭐⭐⭐⭐⭐ | Live Lambda | ⭐⭐⭐⭐⭐ | Growing | Full-stack, DX-first teams |
| **Terraform** | ⭐⭐⭐⭐ | Weak | ⭐⭐⭐ | Largest overall | Multi-cloud, platform teams |
| **Pulumi** | ⭐⭐⭐⭐ | Fair | ⭐⭐⭐⭐ | Large | Code-first, multi-cloud |

---

## 1. AWS CDK v2 + Express Mode — The New Default ⭐

**Post-Express Verdict:** CDK is now the strongest choice for AWS-only teams. It combines:
- **Speed:** `cdk deploy --express` (seconds) + `cdk deploy --hotswap` (instant Lambda code)
- **Type safety:** Full IDE support, autocomplete, refactoring
- **Abstractions:** L2 (sensible defaults), L3 (multi-resource patterns)
- **Compliance:** cdk-nag for security validation
- **CI/CD:** CDK Pipelines (self-mutating)
- **Ecosystem:** Construct Hub with thousands of community constructs

### Developer Workflow

```bash
# Lambda code change → instant (bypasses CloudFormation)
cdk deploy --hotswap

# Infrastructure change → seconds (Express mode)
cdk deploy --express

# Production → full stabilization
cdk deploy

# Self-mutating CI/CD pipeline
cdk deploy PipelineStack  # Pipeline updates itself on commits
```

### Example Stack

```typescript
import { Stack, StackProps } from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class MyAppStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const table = new dynamodb.Table(this, 'Items', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    const fn = new lambda.Function(this, 'Handler', {
      runtime: lambda.Runtime.NODEJS_20_X,
      architecture: lambda.Architecture.ARM_64,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: { TABLE_NAME: table.tableName },
    });

    table.grantReadWriteData(fn);

    new apigw.LambdaRestApi(this, 'Api', { handler: fn });
  }
}
```

---

## 2. AWS SAM + Express Mode

**Post-Express Verdict:** SAM remains the simplest and most productive tool for pure serverless applications. Express mode removes its last speed limitation.

### Developer Workflow

```bash
# Local development (Docker-based Lambda emulation)
sam local invoke MyFunction
sam local start-api  # Local API Gateway

# Deploy with Express (seconds)
sam deploy --express

# Watch mode (auto-redeploy on changes)
sam sync --express --watch

# Save Express as default
sam deploy --express --save-params
```

### Example Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.13
    Architectures: [arm64]
    SnapStart:
      ApplyOn: PublishedVersions

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      CodeUri: src/
      Events:
        Api:
          Type: HttpApi
          Properties:
            Path: /items
            Method: GET
      Environment:
        Variables:
          TABLE_NAME: !Ref ItemsTable

  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

---

## 3. SST v3 (Ion)

**Post-Express Verdict:** SST retains its superior DX for full-stack apps, but its speed advantage over CDK/SAM is now marginal. Its unique strengths are **Live Lambda** and **frontend framework integration**.

### Unique Differentiators (Still Unmatched)

1. **Live Lambda (<10ms reload):** Real AWS events proxied to your local machine
2. **Frontend integration:** First-class Next.js, Astro, Remix, SvelteKit components
3. **Type-safe bindings:** Wire frontend → API → database with full type safety
4. **No CloudFormation:** Uses Pulumi/Terraform (still faster for some edge cases)

### Developer Workflow

```bash
# Live development (code runs locally, triggered by real AWS events)
sst dev

# Deploy
sst deploy

# Remove
sst remove
```

### Example

```typescript
// sst.config.ts
export default $config({
  app(input) {
    return { name: "my-app", region: "us-east-1" };
  },
  async run() {
    const table = new sst.aws.Dynamo("Items", {
      fields: { id: "string" },
      primaryIndex: { hashKey: "id" },
    });

    const api = new sst.aws.Function("Api", {
      handler: "src/api.handler",
      link: [table],
    });

    const web = new sst.aws.Nextjs("Web", {
      link: [api],
    });
  },
});
```

### When SST v3 Still Wins Over CDK+Express

- Teams building full-stack apps with Next.js/Astro/Remix
- Teams that need Live Lambda development (code runs locally against real AWS)
- Projects where Pulumi/Terraform provider ecosystem matters
- Teams that prefer SST's simpler component API

---

## 4. Terraform

**Post-Express Verdict:** No longer offers a speed advantage for AWS-only deployments. Its strength is **multi-cloud** and the **largest IaC ecosystem**.

### When to Choose Terraform

- Multi-cloud environments (AWS + GCP + Azure)
- Platform teams managing infra at scale across providers
- Organizations with existing Terraform expertise
- Compliance workflows requiring `terraform plan` approvals

### Key Notes (2026)
- **CDKTF was sunsetted** in December 2025
- **OpenTofu** (open-source fork) gaining traction with state encryption
- **Serverless.tf** (v6.0+) integrates with SAM CLI for local testing

---

## 5. Pulumi

**Post-Express Verdict:** Code-first IaC without CloudFormation. Speed parity with Express mode means its deployment speed advantage is gone. Strengths: real languages, multi-cloud, ESC (secrets), powers SST v3.

### When to Choose Pulumi
- Multi-cloud with real programming languages
- Teams wanting SST-like flexibility without SST's opinions
- Need Pulumi ESC for centralized secrets management
- Want component resources without CloudFormation's constraints

---

## Recommendation Matrix (Post-Express Mode)

| Team Profile | Recommended Tool | Reason |
|-------------|-----------------|--------|
| AWS-only enterprise | **CDK v2 + Express** | Speed + compliance + ecosystem + type safety |
| Pure serverless microservices | **SAM + Express** | Simplest + best local testing + fastest path |
| Full-stack (Next.js + API + DB) | **SST v3** | Live Lambda + frontend integration + DX |
| Multi-cloud infrastructure | **Terraform** | Provider ecosystem + state management |
| Code-first, multi-cloud | **Pulumi** | Real languages + ESC + flexibility |
| AI-agent-driven development | **CDK/SAM + Express** | Sub-minute feedback loops for AI iteration |

---

## The AI Agent Angle

CloudFormation Express was explicitly designed for AI-assisted infrastructure:

> "AI-assisted infrastructure development that benefits from sub-minute feedback loops"

Tools like **Kiro** and custom AI agents can now:
1. Generate CDK/SAM/CFN templates
2. Deploy in seconds (Express mode)  
3. Get immediate feedback
4. Iterate rapidly

This makes CDK + Express the ideal target for AI-generated infrastructure code because:
- CloudFormation has the largest template corpus for AI training
- cdk-nag validates security automatically
- Pre-deployment validation catches errors before provisioning
- Express mode provides rapid iteration cycles
