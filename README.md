# Modern Cloud-Native Serverless Framework on AWS — 2026

An opinionated, enterprise-grade framework for building cloud-native serverless
applications on AWS. It is a **decision framework**, not just documentation: it
tells you *what* to build with, *how* to structure code, *how* to deploy safely,
*how* to govern at scale, and *how* to develop with AI.

> **Published site:** the documentation is built with [Zensical](https://zensical.org)
> and published to GitHub Pages via [`.github/workflows/docs.yml`](.github/workflows/docs.yml).
> The canonical source for every chapter lives in **[`docs/`](./docs/)** — start at
> [`docs/index.md`](./docs/index.md).

---

## Repository Layout

```
cloud-native-framework/
├── docs/                 # ← single source of truth (all chapters + index.md)
│   ├── index.md          # navigation hub with diagrams and "start here" guide
│   └── NN-*.md           # 35 chapters
├── zensical.toml         # site config + authoritative navigation ordering
├── .github/workflows/    # docs.yml → builds docs/ and deploys to GitHub Pages
└── README.md             # this file
```

The chapter files live **only** in `docs/`. Edit them there — the site build
(`zensical build`) consumes `docs/` exclusively.

---

## Read It Locally

```bash
pip install zensical
zensical serve       # hot-reload preview at http://localhost:8000
zensical build       # static site → site/
```

---

## The Framework at a Glance

The chapters below follow the curated learning path defined in
[`zensical.toml`](./zensical.toml). Every link points into `docs/`.

### Principles & Patterns
| Chapter | Focus |
|---------|-------|
| [Architecture Principles](./docs/01-architecture-principles.md) | 16-Factor App, Well-Architected, cell-based, core 2026 principles |
| [Software Architecture Patterns](./docs/02-software-architecture-patterns.md) | Hexagonal, DDD, CQRS, vertical slice |
| [Platform Engineering Guidelines](./docs/03-platform-engineering-guidelines.md) | Platform-as-product, golden paths, DX metrics, maturity model |
| [Platform Engineering: IDP → ADP](./docs/04-platform-engineering-idp-to-adp.md) | Agentic developer platform evolution, core paths |
| [AI-SDLC (Agentic Lifecycle)](./docs/05-ai-sdlc.md) | AWS AI-DLC, Kiro/ThothCTL, 5-layer reference architecture |
| [DevOps & CI/CD (TPF)](./docs/06-devops-cicd.md) | Ten Pillars, trunk-based + progressive delivery, DORA |
| [Testing Strategy](./docs/07-testing-strategy.md) | Serverless testing pyramid, contract, chaos, load |
| [APIOps Model](./docs/28-apiops.md) | Contract-first API lifecycle, OpenAPI/AsyncAPI/GraphQL governance |
| [Data Strategy](./docs/29-data-strategy.md) | Cell data ownership, data mesh, data contracts |

### Infrastructure
| Chapter | Focus |
|---------|-------|
| [Compute Layer](./docs/08-compute.md) | Lambda, Step Functions, ECS/Fargate, decision matrix |
| [Infrastructure as Code](./docs/09-iac.md) | CDK v2 + Express, SAM, SST — post-Express comparison |
| [CloudFormation Express](./docs/10-cfn-express.md) | Express-mode mechanics, benchmarks, per-tool impact |
| [API & Event Patterns](./docs/11-api-events.md) | API Gateway, AppSync, EventBridge composition |
| [Data Layer](./docs/12-data-layer.md) | DynamoDB, Aurora Serverless v2, ElastiCache/Valkey, S3 Express |
| [Frontend & Full-Stack](./docs/13-frontend-fullstack.md) | Amplify Gen 2, SST v3, CloudFront/edge |
| [AI/ML Integration](./docs/14-ai-ml.md) | Bedrock, AgentCore, Strands SDK, RAG |

### Operations & Governance
| Chapter | Focus |
|---------|-------|
| [Observability](./docs/15-observability.md) | OpenTelemetry/ADOT, Powertools, Application Signals, SLOs |
| [Security Baseline](./docs/16-security-baseline.md) | Defense-in-depth, zero-trust, AI security, secrets |
| [Multi-Account Landing Zone](./docs/17-multi-account-landing-zone.md) | Control Tower, SCPs, RCPs, networking, centralized logging |
| [FinOps & Cost Governance](./docs/18-finops-cost-governance.md) | Tagging, service-level optimization, cost gates |
| [Disaster Recovery & Continuity](./docs/30-disaster-recovery-continuity.md) | RTO/RPO tiers, serverless DR patterns, failover runbooks |
| [Ephemeral Environments & Concurrency](./docs/34-ephemeral-environments.md) | Per-dev / per-PR sandboxes, TTL cleanup, cost guardrails |
| [Reference Architecture](./docs/19-reference-architecture.md) | Full-stack diagrams: e-commerce, SaaS, IoT |
| [Recommendations](./docs/20-recommendations.md) | Recommended stack by application type |

### Adoption & Onboarding
| Chapter | Focus |
|---------|-------|
| [Adoption Roadmap](./docs/21-adoption-roadmap.md) | Framework comparison, staged roadmap, checklists |
| [Developer Onboarding](./docs/22-developer-onboarding.md) | Prerequisites, first-30-minutes, dev workflow |

### Intelligence & AI Brains
| Chapter | Focus |
|---------|-------|
| [Custom Intelligent AI Brains](./docs/32-custom-intelligent-ai-brains.md) | Organizational learning-memory layer, AWS implementation, case studies |
| [Team Topologies, Roles & Permissions](./docs/33-team-topologies-roles.md) | AI-era roles, decision tiers, RACI, IAM + Cedar |

### Workshops
| Chapter | Focus |
|---------|-------|
| [Workshop 0: Foundations](./docs/35-workshop-foundations.md) | First Lambda + HTTP API with plain CDK — start here if new to IaC |
| [Workshop: Serverless End-to-End](./docs/23-workshop-serverless.md) | Full serverless app with AI-DLC + ThothCTL |
| [Workshop: Enterprise CDK](./docs/24-workshop-enterprise-cdk.md) | Private constructs, CodeArtifact, Projen, RCPs |
| [Workshop: ECS Backend](./docs/25-workshop-ecs-backend.md) | Containers on Fargate, ECS Express, Docker Compose → cloud |
| [Workshop: CI/CD Phase 1](./docs/26-workshop-cicd-phase1.md) | Team-level CDK Pipelines, canary, feature flags |
| [Workshop: CI/CD Phase 2](./docs/27-workshop-cicd-phase2.md) | Enterprise pipelines, DevOps/FinOps agents, SCPs + RCPs |
| [Workshop: Micro-Frontends](./docs/31-workshop-micro-frontends.md) | Micro-frontends on CloudFront + S3 vs Amplify |

### Reference
| Chapter | Focus |
|---------|-------|
| [Glossary](./docs/36-glossary.md) | Definitions of key terms across the framework, each linking to its chapter |

---

## Getting Started

| Your Goal | Start Here |
|-----------|-----------|
| New to AWS IaC — first deploy | [Workshop 0: Foundations](./docs/35-workshop-foundations.md) |
| Build a new serverless app | [Workshop: Serverless End-to-End](./docs/23-workshop-serverless.md) |
| Build a container-based backend | [Workshop: ECS Backend](./docs/25-workshop-ecs-backend.md) |
| Set up enterprise CI/CD | [Workshop: CI/CD Phase 1](./docs/26-workshop-cicd-phase1.md) |
| Understand architecture decisions | [Architecture Principles](./docs/01-architecture-principles.md) |
| Set up organizational governance | [Workshop: Enterprise CDK](./docs/24-workshop-enterprise-cdk.md) |

---

## Paradigm Shift: CloudFormation Express Mode (June 2026)

Express mode completes stack operations as soon as resource configuration is
applied — **without waiting for full stabilization** — cutting deployment times by
**up to 4×**. This closed the single biggest gap that pushed teams from CDK/SAM
toward SST/Pulumi/Terraform, making the entire CloudFormation ecosystem
competitive on speed.

| Scenario | Standard Mode | Express Mode |
|----------|--------------|--------------|
| SQS queue + DLQ | 64 seconds | ~10 seconds |
| Lambda delete (with ENI) | 20–30 minutes | ~10 seconds |
| CloudFront distribution | 5–10 minutes | Sub-minute |
| VPC + Subnets + ALB | Minutes | Seconds (ARN/DNS returned immediately) |

See [CloudFormation Express](./docs/10-cfn-express.md) for the deep dive and
[Infrastructure as Code](./docs/09-iac.md) for how it reshapes tool selection.

---

## Contributing

- Edit chapters in [`docs/`](./docs/) only — never re-create root copies.
- Keep the navigation in [`zensical.toml`](./zensical.toml) and the index in
  [`docs/index.md`](./docs/index.md) in sync when adding or renaming a chapter.
- Prefer Zensical's auto-generated table of contents over hand-maintained
  in-page TOCs.
- Preview locally with `zensical serve` before opening a pull request.
