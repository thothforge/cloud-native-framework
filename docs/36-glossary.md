# Glossary

Terminology used across the framework. Terms are grouped by area; within each
group they are alphabetical. Where a concept has a dedicated chapter, the
"Learn more" link points to it.

---

## Architecture & Patterns

**Cell-Based Architecture** — A design that partitions a system into independent,
self-contained "cells," each serving a subset of traffic so that a failure is
contained to a single cell rather than the whole system. Learn more:
[Architecture Principles](01-architecture-principles.md).

**CQRS (Command Query Responsibility Segregation)** — Separating the write model
(commands) from the read model (queries) so each can be optimized independently.
Learn more: [Software Architecture Patterns](02-software-architecture-patterns.md).

**DDD (Domain-Driven Design)** — Modeling software around the business domain,
using bounded contexts and a ubiquitous language shared by engineers and domain
experts. Learn more: [Software Architecture Patterns](02-software-architecture-patterns.md).

**ECST (Event-Carried State Transfer)** — An event-driven pattern where events
carry the full state a consumer needs, avoiding a synchronous call back to the
producer. Learn more: [Data Strategy](29-data-strategy.md).

**Event Sourcing** — Persisting state as an append-only log of events rather than
as current-state rows, reconstructing state by replaying events. Learn more:
[Software Architecture Patterns](02-software-architecture-patterns.md).

**Hexagonal Architecture (Ports & Adapters)** — Structuring code so the domain
core depends only on abstract "ports," with infrastructure plugged in via
"adapters," keeping business logic independent of frameworks and I/O. Learn more:
[Software Architecture Patterns](02-software-architecture-patterns.md).

**16-Factor App** — An extension of the Twelve-Factor App methodology for modern
cloud-native and serverless applications. Learn more:
[Architecture Principles](01-architecture-principles.md).

**Vertical Slice Architecture** — Organizing code by feature (end-to-end slices)
rather than by technical layer. Learn more:
[Software Architecture Patterns](02-software-architecture-patterns.md).

**Well-Architected Framework** — AWS's set of six pillars (operational excellence,
security, reliability, performance efficiency, cost optimization, sustainability)
for evaluating architectures. Learn more:
[Architecture Principles](01-architecture-principles.md).

---

## Compute & Infrastructure

**ARM64 (Graviton)** — AWS's Arm-based processors that typically offer better
price-performance than x86 for many serverless and container workloads. Learn
more: [Compute Layer](08-compute.md).

**CDK (AWS Cloud Development Kit)** — An IaC framework for defining cloud
infrastructure in general-purpose languages (e.g. TypeScript) that synthesize to
CloudFormation. Learn more: [Infrastructure as Code](09-iac.md).

**CloudFormation Express Mode** — A CloudFormation deployment mode (June 2026)
that completes operations once configuration is applied, without waiting for full
stabilization, cutting deployment times up to ~4×. Learn more:
[CloudFormation Express](10-cfn-express.md).

**Fargate** — AWS's serverless compute engine for containers (ECS/EKS), removing
the need to manage EC2 hosts. Learn more: [Compute Layer](08-compute.md).

**IaC (Infrastructure as Code)** — Managing infrastructure through
version-controlled declarative or programmatic definitions rather than manual
console actions. Learn more: [Infrastructure as Code](09-iac.md).

**Lambda** — AWS's function-as-a-service compute; runs code in response to events
and scales to zero. Learn more: [Compute Layer](08-compute.md).

**SAM (Serverless Application Model)** — An AWS framework and CLI for building
serverless applications on top of CloudFormation. Learn more:
[Infrastructure as Code](09-iac.md).

**SnapStart** — A Lambda feature that caches an initialized execution environment
snapshot to reduce cold-start latency. Learn more: [Compute Layer](08-compute.md).

**SST** — An open-source framework for building full-stack serverless
applications on AWS. Learn more: [Infrastructure as Code](09-iac.md).

**Step Functions** — AWS's serverless workflow orchestrator for coordinating
distributed tasks as state machines. Learn more: [Compute Layer](08-compute.md).

---

## API, Events & Data

**AppSync** — AWS's managed GraphQL service, including real-time subscriptions.
Learn more: [API & Event Patterns](11-api-events.md).

**AsyncAPI** — A specification for describing event-driven and asynchronous APIs,
the async counterpart to OpenAPI. Learn more: [APIOps Model](28-apiops.md).

**Aurora Serverless v2** — An on-demand, auto-scaling configuration of Amazon
Aurora (relational). Learn more: [Data Layer](12-data-layer.md).

**Data Contract** — A formal, versioned agreement describing the schema, semantics,
and SLAs of data shared between producer and consumer. Learn more:
[Data Strategy](29-data-strategy.md).

**Data Mesh** — A decentralized data architecture where domain teams own their
data as products. Learn more: [Data Strategy](29-data-strategy.md).

**DynamoDB** — AWS's fully managed, serverless key-value and document NoSQL
database; the framework's default data store. Learn more:
[Data Layer](12-data-layer.md).

**EventBridge** — AWS's serverless event bus (with Pipes and Scheduler) that forms
the asynchronous backbone of event-driven systems. Learn more:
[API & Event Patterns](11-api-events.md).

**OpenAPI** — A specification for describing REST APIs, used for contract-first
API design and governance. Learn more: [APIOps Model](28-apiops.md).

**VPC Lattice** — An AWS service for connecting, securing, and monitoring
service-to-service communication across accounts and VPCs. Learn more:
[API & Event Patterns](11-api-events.md).

---

## Operations, Security & Governance

**ADOT (AWS Distro for OpenTelemetry)** — AWS's supported distribution of the
OpenTelemetry collector and SDKs for vendor-neutral telemetry. Learn more:
[Observability](15-observability.md).

**Application Signals** — An AWS observability feature for automatically tracking
application health, SLIs, and SLOs. Learn more: [Observability](15-observability.md).

**Canary Deployment** — A progressive rollout strategy that shifts a small
percentage of traffic to a new version before full release. Learn more:
[DevOps & CI/CD (TPF)](06-devops-cicd.md).

**cdk-nag** — A tool that checks CDK applications against security and compliance
rule packs at synth time. Learn more: [Security Baseline](16-security-baseline.md).

**Cedar** — AWS's open-source policy language for fine-grained authorization.
Learn more: [Team Topologies, Roles & Permissions](33-team-topologies-roles.md).

**Continuum** — Continuous, automated security validation (e.g. ongoing
penetration testing) integrated into the delivery pipeline. Learn more:
[Security Baseline](16-security-baseline.md).

**Control Tower** — AWS's service for setting up and governing a secure
multi-account environment (landing zone). Learn more:
[Multi-Account Landing Zone](17-multi-account-landing-zone.md).

**DORA Metrics** — Four key delivery-performance metrics (deployment frequency,
lead time for changes, change failure rate, time to restore). Learn more:
[DevOps & CI/CD (TPF)](06-devops-cicd.md).

**Ephemeral Environment** — A short-lived, disposable environment (per-developer or
per-PR) created on demand and torn down automatically. Learn more:
[Ephemeral Environments & Concurrency](34-ephemeral-environments.md).

**FinOps** — The practice of bringing financial accountability to cloud spend
through shared ownership of cost and usage. Learn more:
[FinOps & Cost Governance](18-finops-cost-governance.md).

**Permission Boundary** — An IAM feature that caps the maximum permissions an IAM
principal can have, regardless of its attached policies. Learn more:
[Multi-Account Landing Zone](17-multi-account-landing-zone.md).

**RCP (Resource Control Policy)** — An organization policy that restricts which
external principals can access your resources (the complement to SCPs). Learn
more: [Multi-Account Landing Zone](17-multi-account-landing-zone.md).

**RTO / RPO** — Recovery Time Objective (how quickly service must be restored) and
Recovery Point Objective (how much data loss is tolerable). Learn more:
[Disaster Recovery & Continuity](30-disaster-recovery-continuity.md).

**SCP (Service Control Policy)** — An organization policy that sets the maximum
available permissions for accounts in an AWS Organization. Learn more:
[Multi-Account Landing Zone](17-multi-account-landing-zone.md).

**SLO / SLI** — Service Level Objective (target for reliability) and Service Level
Indicator (the measured signal). Learn more: [Observability](15-observability.md).

**TPF (Trunk-based, Progressive rollout, Feature toggles)** — The framework's
deployment model combining trunk-based development, progressive delivery, and
feature flags. Learn more: [DevOps & CI/CD (TPF)](06-devops-cicd.md).

---

## AI, Agents & Methodology

**AgentCore** — AWS's runtime and supporting services (memory, gateway) for
building and operating AI agents. Learn more: [AI/ML Integration](14-ai-ml.md).

**AI Brain** — An organizational, shared learning-memory layer that provides
persistent context to agents and humans across the product lifecycle. Learn more:
[Custom Intelligent AI Brains](32-custom-intelligent-ai-brains.md).

**AI-DLC (AI Development Lifecycle)** — AWS's AI-driven development methodology
spanning Inception → Construction → Operations. Learn more: [AI-SDLC](05-ai-sdlc.md).

**Bedrock** — AWS's managed service for accessing foundation models and building
generative-AI applications. Learn more: [AI/ML Integration](14-ai-ml.md).

**Golden Path** — A supported, opinionated, well-paved route for building and
shipping software that encodes best practices by default. Learn more:
[Platform Engineering Guidelines](03-platform-engineering-guidelines.md).

**Guardrails** — Configurable safety controls for foundation models (content
filtering, PII redaction, denied topics). Learn more:
[AI/ML Integration](14-ai-ml.md).

**Kiro** — An AI-assisted development agent/environment used within the AI-DLC
workflow. Learn more: [AI-SDLC](05-ai-sdlc.md).

**MCP (Model Context Protocol)** — An open protocol for connecting AI models and
agents to tools and context sources. Learn more: [AI-SDLC](05-ai-sdlc.md).

**RAG (Retrieval-Augmented Generation)** — Augmenting model responses with
retrieved, relevant context (e.g. from a knowledge base). Learn more:
[AI/ML Integration](14-ai-ml.md).

**Strands SDK** — An SDK for building AI agents that run on AgentCore. Learn more:
[AI/ML Integration](14-ai-ml.md).

**ThothCTL** — A platform-engineering CLI for DevSecOps automation, scanning, cost
analysis, and governance. Learn more:
[Platform Engineering Guidelines](03-platform-engineering-guidelines.md).

---

## Platform Engineering

**ADP (Agentic Developer Platform)** — The evolution of an IDP where AI agents
provide and operate self-service capabilities. Learn more:
[Platform Engineering: IDP → ADP](04-platform-engineering-idp-to-adp.md).

**IDP (Internal Developer Platform)** — A self-service layer of tools and
workflows that lets product teams ship independently. Learn more:
[Platform Engineering Guidelines](03-platform-engineering-guidelines.md).

**Platform as a Product** — Treating the internal platform as a product with users,
a roadmap, and adoption metrics. Learn more:
[Platform Engineering Guidelines](03-platform-engineering-guidelines.md).

<!-- FRAMEWORK-NAV -->
---

[← Back to index](index.md)

| Previous | Next |
|:---------|-----:|
| ← [Workshop: Micro-Frontends](31-workshop-micro-frontends.md) | &nbsp; |
