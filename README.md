# Modern Cloud-Native Serverless Framework on AWS — 2026

## Executive Summary

This document provides a comprehensive investigation into the modern serverless ecosystem on AWS for building full applications in 2026. A major paradigm shift occurred in **June 2026** with the launch of **CloudFormation Express Mode**, which eliminates the primary criticism of CloudFormation-based tools (slow deployments) and fundamentally changes the IaC landscape.

## Key Paradigm Shift: CloudFormation Express Mode (June 2026)

**What changed:** CloudFormation Express mode completes stack operations as soon as resource configuration is applied — **without waiting for full stabilization** — reducing deployment times by **up to 4x**.

**Why it matters:** The #1 reason teams adopted SST v3/Pulumi/Terraform over CDK/SAM was CloudFormation's slow deployment speed. Express mode eliminates this gap, making the entire CloudFormation ecosystem (CDK, SAM, native CFN) competitive on speed.

### Before vs After Express Mode

| Scenario | Standard Mode | Express Mode |
|----------|--------------|--------------|
| SQS queue + DLQ | 64 seconds | ~10 seconds |
| Lambda delete (with ENI) | 20-30 minutes | ~10 seconds |
| CloudFront distribution | 5-10 minutes | Sub-minute |
| VPC + Subnets + ALB | Minutes | Seconds (get ARN/DNS immediately) |

### How to Enable

```bash
# CLI
aws cloudformation create-stack \
  --stack-name my-app \
  --template-body file://template.yaml \
  --deployment-config '{"mode": "EXPRESS"}'

# CDK
cdk deploy --express

# SAM
sam deploy --express
sam sync --express
```

---

## Table of Contents

1. [Compute Layer](./01-compute.md)
2. [Infrastructure as Code (IaC)](./02-iac.md)
3. [API & Event-Driven Patterns](./03-api-events.md)
4. [Data Layer](./04-data-layer.md)
5. [Frontend & Full-Stack](./05-frontend-fullstack.md)
6. [Observability & DevOps](./06-observability-devops.md)
7. [AI/ML Integration](./07-ai-ml.md)
8. [CloudFormation Express - Paradigm Shift Analysis](./08-cfn-express-paradigm-shift.md)
9. [Reference Architecture](./09-reference-architecture.md)
10. [Recommendations](./10-recommendations.md)
11. [Architecture Principles & 2026 Tendencies](./11-architecture-principles.md)
