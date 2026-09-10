# 24 — Developer Onboarding Guide

> **Goal:** A new developer joins your team and is productive within 1 day.  
> This is your "Day 1" document. Follow it top-to-bottom.

---

## 1. Prerequisites

Most tooling is installed automatically via ThothCTL:

```bash
thothctl init env
```

This bootstraps your local environment with:

- **Node.js 24+** (via nvm)
- **AWS CDK CLI** (latest v2)
- **Docker Desktop** (required for local development)
- **AWS CLI v2** (configured with SSO or credentials)
- **ThothCTL** (the framework CLI)
- **pnpm** or **npm** (package manager)
- **Git** (with commit hooks pre-configured)

### Manual checks

| Tool | Verify | Minimum Version |
|------|--------|-----------------|
| Node.js | `node --version` | 20.x |
| Docker | `docker --version` | 24.x |
| AWS CLI | `aws --version` | 2.x |
| CDK | `cdk --version` | 2.170+ |
| ThothCTL | `thothctl --version` | latest |

### AWS Access

Ensure you have:
- AWS SSO configured (`aws sso login --profile <your-profile>`)
- Access to the team's dev account
- Permissions to deploy CloudFormation stacks

---

## 2. First 30 Minutes

### Clone and install

```bash
# Clone the project scaffold
git clone <your-team-repo-url>
cd <project-name>

# Install dependencies
npm install

# Verify everything compiles
npm run build
```

### Understand the project structure

```
project-root/
├── .kiro/                    # AI steering files (specs, tasks, rules)
├── bin/
│   └── app.ts               # CDK app entry point
├── lib/
│   ├── stacks/              # CDK stack definitions
│   └── constructs/          # Reusable L3 constructs
├── src/
│   ├── domain/              # Pure business logic (no AWS imports!)
│   │   ├── models/          # Domain entities and value objects
│   │   ├── services/        # Domain services / use cases
│   │   └── ports/           # Interfaces (inbound + outbound)
│   ├── adapters/
│   │   ├── inbound/         # Lambda handlers, API controllers
│   │   └── outbound/        # DynamoDB repos, SQS publishers, HTTP clients
│   └── shared/              # Cross-cutting: logging, errors, config
├── test/
│   ├── unit/                # Fast, isolated tests
│   ├── integration/         # Tests with real AWS (localstack or deployed)
│   └── cdk/                 # CDK snapshot + cdk-nag tests
├── docker-compose.yml        # Local development environment
├── cdk.json                  # CDK configuration
├── thoth.config.ts           # ThothCTL configuration
└── package.json
```

**Key insight:** The `src/domain/` folder should NEVER import from `@aws-sdk/*`. If it does, the architecture boundary has been violated.

---

## 3. Understanding the Architecture

This framework uses the **Hexagonal Architecture** (Ports & Adapters) pattern:

```
                    ┌─────────────────────────────┐
  Inbound          │         DOMAIN               │         Outbound
  Adapters         │                               │         Adapters
                   │  ┌───────────────────────┐   │
 ┌──────────┐     │  │   Business Logic       │   │     ┌──────────────┐
 │ Lambda    │────▶│  │   (pure functions)     │   │────▶│ DynamoDB     │
 │ Handler   │     │  │                        │   │     │ Repository   │
 └──────────┘     │  └───────────────────────┘   │     └──────────────┘
                   │         ▲         │           │
 ┌──────────┐     │         │         ▼           │     ┌──────────────┐
 │ SQS      │────▶│  ┌──────┴───┐ ┌──────────┐   │────▶│ EventBridge  │
 │ Consumer  │     │  │  Inbound │ │ Outbound │   │     │ Publisher    │
 └──────────┘     │  │  Ports   │ │ Ports    │   │     └──────────────┘
                   │  └──────────┘ └──────────┘   │
                   └─────────────────────────────┘
```

### Where does my code go?

| I need to... | Put it in... |
|---|---|
| Define a business rule | `src/domain/services/` |
| Define a data entity | `src/domain/models/` |
| Define an interface for external systems | `src/domain/ports/` |
| Handle an incoming Lambda event | `src/adapters/inbound/` |
| Read/write to DynamoDB | `src/adapters/outbound/` |
| Publish events to EventBridge | `src/adapters/outbound/` |
| Call an external HTTP API | `src/adapters/outbound/` |
| Define CDK infrastructure | `lib/stacks/` or `lib/constructs/` |

### The golden rule

> **Domain logic is framework-agnostic.** It doesn't know about Lambda, DynamoDB, or SQS. Adapters translate between the outside world and your domain.

---

## 4. Development Workflow

The development loop follows a progressive confidence path:

```
Local (fast) ──▶ Express Deploy (minutes) ──▶ Pipeline (production)
```

### Step 1: Local development with Docker Compose

```bash
# Start local services (DynamoDB Local, LocalStack, etc.)
docker compose up -d

# Run your function locally with hot reload
npm run dev

# Or invoke a specific function
npm run invoke -- --function MyFunction --event events/sample.json
```

### Step 2: Express deploy to your sandbox

```bash
# Deploy directly to your personal dev account (skips pipeline)
cdk deploy --all --profile dev --hotswap-fallback

# For even faster iteration on Lambda code only:
cdk deploy --all --profile dev --hotswap
```

> **`--hotswap`** updates Lambda code in ~5 seconds without a full CloudFormation deployment.

### Step 3: Push through the pipeline

```bash
git add .
git commit -m "feat: add order validation logic"
git push origin feature/order-validation
# Open a PR → pipeline runs → deploys to staging → approval → production
```

### The feedback loop

| Stage | Speed | Confidence |
|-------|-------|-----------|
| Unit tests locally | Seconds | Code correctness |
| Docker Compose | Seconds | Integration logic |
| Express deploy | 1–3 min | Real AWS services |
| Pipeline (staging) | 5–10 min | Production parity |
| Pipeline (prod) | +approval | Full confidence |

---

## 5. AI-DLC (AI-Driven Development Lifecycle)

Every feature or task you work on follows the AI-DLC pattern. Start your prompt to the AI assistant with:

```
Using AI-DLC, implement <description of what you need>
```

This triggers a structured lifecycle:

### The Three Phases

#### Phase 1: Inception (Requirements → Design)

The AI will:
- Clarify requirements and ask questions
- Generate a specification document
- Define acceptance criteria
- Identify affected components and dependencies
- Produce a task breakdown

**Your role:** Answer questions, validate the spec, approve the design.

#### Phase 2: Construction (Design → Code)

The AI will:
- Implement code following the hexagonal architecture
- Write unit tests alongside implementation
- Run `cdk-nag` compliance checks
- Follow framework conventions automatically

**Your role:** Review the implementation, run tests, provide feedback.

#### Phase 3: Operations (Code → Production)

The AI will:
- Add observability (structured logging, metrics, alarms)
- Generate runbook entries
- Update documentation
- Verify pipeline compatibility

**Your role:** Approve the PR, monitor the deployment.

### Example prompt

```
Using AI-DLC, add a new endpoint POST /orders that validates the order,
stores it in DynamoDB, and publishes an OrderCreated event to EventBridge.
```

The AI handles the boilerplate. You focus on business decisions.

---

## 6. Kiro Steering Files

The `.kiro/` directory contains files that guide AI behavior for your project:

```
.kiro/
├── specs/                    # Feature specifications (AI-DLC artifacts)
│   ├── order-service.md      # Spec for the order service feature
│   └── auth-flow.md          # Spec for authentication flow
├── tasks/                    # Task breakdowns for in-progress work
│   └── current-sprint.md
├── rules/                    # Project-specific rules the AI must follow
│   ├── architecture.md       # "Always use hexagonal pattern"
│   ├── naming.md             # "Lambda handlers use handle* prefix"
│   ├── testing.md            # "Every adapter needs integration test"
│   └── security.md           # "Never log PII fields"
└── steering.md               # Top-level project context
```

### How it works

When you work with an AI assistant (Kiro, Copilot, etc.), these files provide:

- **Context:** The AI understands your project's architecture and conventions
- **Constraints:** Rules prevent the AI from generating non-compliant code
- **Continuity:** Specs persist across sessions — pick up where you left off
- **Consistency:** Every team member gets the same AI guidance

### What you should do

1. **Read `steering.md`** — it's the project overview
2. **Check `rules/`** — understand what conventions are enforced
3. **Look at existing `specs/`** — see how features are documented
4. **Don't edit rules without team consensus** — they affect everyone

---

## 7. ThothCTL Commands You'll Use Daily

ThothCTL is your framework CLI. These are the commands you'll reach for every day:

### `thothctl scan`

Analyze your project for compliance and best practices:

```bash
# Full scan — architecture, security, performance
thothctl scan

# Scan specific category
thothctl scan --category security
thothctl scan --category architecture
```

Catches issues like:
- Domain importing from AWS SDK (architecture violation)
- Missing error handling in Lambda handlers
- Unencrypted resources in CDK stacks
- Missing alarms for critical functions

### `thothctl check`

Quick validation before committing:

```bash
# Pre-commit check (runs automatically via git hook)
thothctl check

# Check specific aspect
thothctl check --type types      # TypeScript strict mode compliance
thothctl check --type deps       # Dependency vulnerabilities
thothctl check --type cdk-nag    # CDK security/compliance
```

### `thothctl workflow`

Manage development workflows:

```bash
# Start a new feature workflow
thothctl workflow start --feature "order-validation"

# See current workflow status
thothctl workflow status

# Complete current workflow step
thothctl workflow next
```

### `thothctl document`

Auto-generate documentation from your code:

```bash
# Generate API docs from CDK constructs
thothctl document --type api

# Generate architecture decision records
thothctl document --type adr

# Update README with current project state
thothctl document --type readme
```

### Quick reference

| Command | When to use |
|---------|------------|
| `thothctl scan` | Before opening a PR |
| `thothctl check` | Before every commit (auto via hook) |
| `thothctl workflow start` | Beginning a new feature |
| `thothctl document` | After significant changes |
| `thothctl init env` | First-time setup |

---

## 8. Git Workflow

We follow **trunk-based development** with short-lived feature branches.

### Branch naming

```
feature/<ticket-id>-short-description
fix/<ticket-id>-short-description
chore/<description>
```

### Daily flow

```bash
# Start from main (always up to date)
git checkout main
git pull

# Create a short-lived branch
git checkout -b feature/ORD-123-add-order-validation

# Work, commit often with conventional commits
git commit -m "feat(orders): add validation for order amounts"
git commit -m "test(orders): add unit tests for validation"

# Push and open a PR
git push -u origin feature/ORD-123-add-order-validation
gh pr create --title "feat(orders): add order validation" --body "..."
```

### Commit message format

```
<type>(<scope>): <description>

Types: feat, fix, refactor, test, chore, docs
Scope: the domain area (orders, auth, infra, etc.)
```

### PR rules

- **Branch lifetime:** < 1 day ideal, < 3 days maximum
- **Size:** < 400 lines changed (split larger work)
- **Reviews:** 1 approval minimum
- **Checks must pass:** tests, cdk-nag, thothctl scan
- **Squash merge** into main

### What triggers deployment?

```
Push to main → Pipeline → Build → Test → Deploy Staging → Approval → Deploy Prod
```

---

## 9. Testing

### Where tests live

```
test/
├── unit/                     # Mirror of src/ structure
│   ├── domain/
│   │   └── services/
│   │       └── order-service.test.ts
│   └── adapters/
│       └── inbound/
│           └── create-order-handler.test.ts
├── integration/              # Tests against real/emulated services
│   └── order-repository.integration.test.ts
└── cdk/                      # Infrastructure tests
    ├── snapshot.test.ts      # Detect unintended CDK changes
    └── compliance.test.ts    # cdk-nag rule validation
```

### Running tests

```bash
# Run everything (unit + cdk-nag) — this is what CI runs
npm test

# Run only unit tests
npm run test:unit

# Run with coverage
npm run test:coverage

# Run a specific test file
npx jest test/unit/domain/services/order-service.test.ts

# Run integration tests (requires Docker or AWS credentials)
npm run test:integration

# Run CDK compliance tests only
npm run test:cdk
```

### What `npm test` actually does

1. **Unit tests** — Jest runs all `*.test.ts` files in `test/unit/`
2. **CDK-nag tests** — Validates your infrastructure against AWS best practices (security, reliability, compliance rules)

Both must pass for CI to go green.

### Testing philosophy

| Layer | What to test | How |
|-------|-------------|-----|
| Domain services | Business logic, edge cases | Pure unit tests (no mocks needed!) |
| Inbound adapters | Event parsing, error handling | Unit tests with mocked ports |
| Outbound adapters | Correct AWS SDK calls | Integration tests |
| CDK stacks | Security compliance, no regressions | cdk-nag + snapshots |

### Writing a test

```typescript
// test/unit/domain/services/order-service.test.ts
import { validateOrder } from '@domain/services/order-service';

describe('OrderService', () => {
  describe('validateOrder', () => {
    it('rejects orders with zero amount', () => {
      const order = { id: '123', amount: 0, currency: 'USD' };
      const result = validateOrder(order);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Amount must be greater than zero');
    });

    it('accepts valid orders', () => {
      const order = { id: '123', amount: 99.99, currency: 'USD' };
      const result = validateOrder(order);
      expect(result.isValid).toBe(true);
    });
  });
});
```

---

## 10. Common Tasks

### Add a new Lambda function

1. **Create the domain logic** (if new):
   ```typescript
   // src/domain/services/my-feature-service.ts
   export function processFeature(input: FeatureInput): FeatureOutput {
     // Pure business logic here
   }
   ```

2. **Create the inbound adapter** (Lambda handler):
   ```typescript
   // src/adapters/inbound/my-feature-handler.ts
   import { processFeature } from '@domain/services/my-feature-service';
   import { MyRepository } from '@domain/ports/my-repository.port';

   export const handler = async (event: APIGatewayProxyEventV2) => {
     const input = parseEvent(event);
     const result = processFeature(input);
     return { statusCode: 200, body: JSON.stringify(result) };
   };
   ```

3. **Add CDK infrastructure**:
   ```typescript
   // lib/constructs/my-feature-function.ts
   const fn = new NodejsFunction(this, 'MyFeatureFunction', {
     entry: 'src/adapters/inbound/my-feature-handler.ts',
     handler: 'handler',
     runtime: Runtime.NODEJS_24_X,
     environment: { TABLE_NAME: table.tableName },
   });
   table.grantReadWriteData(fn);
   ```

4. **Add tests** in `test/unit/domain/services/` and `test/unit/adapters/inbound/`

5. **Run `thothctl scan`** to validate compliance

### Add a new API endpoint

```typescript
// In your API construct or stack
const api = new HttpApi(this, 'Api');

api.addRoutes({
  path: '/orders/{id}',
  methods: [HttpMethod.GET],
  integration: new HttpLambdaIntegration('GetOrder', getOrderFn),
});
```

Then create the handler following the pattern above.

### Add a new event consumer (SQS/EventBridge)

1. **Create the handler**:
   ```typescript
   // src/adapters/inbound/order-created-consumer.ts
   import { SQSEvent } from 'aws-lambda';
   import { processOrderCreated } from '@domain/services/notification-service';

   export const handler = async (event: SQSEvent) => {
     for (const record of event.Records) {
       const orderEvent = JSON.parse(record.body);
       await processOrderCreated(orderEvent);
     }
   };
   ```

2. **Wire up the infrastructure**:
   ```typescript
   const queue = new Queue(this, 'OrderCreatedQueue', {
     deadLetterQueue: { queue: dlq, maxReceiveCount: 3 },
   });

   const consumer = new NodejsFunction(this, 'OrderCreatedConsumer', {
     entry: 'src/adapters/inbound/order-created-consumer.ts',
   });

   consumer.addEventSource(new SqsEventSource(queue, { batchSize: 10 }));
   ```

3. **Connect to EventBridge** (if sourcing from EventBridge):
   ```typescript
   new Rule(this, 'OrderCreatedRule', {
     eventBus,
     eventPattern: { source: ['orders'], detailType: ['OrderCreated'] },
     targets: [new SqsQueue(queue)],
   });
   ```

---

## 11. Troubleshooting

### Common errors and fixes

#### `Error: Cannot find module '@domain/...'`

**Cause:** TypeScript path aliases not configured.  
**Fix:** Check `tsconfig.json` has path mappings:
```json
{
  "compilerOptions": {
    "paths": {
      "@domain/*": ["./src/domain/*"],
      "@adapters/*": ["./src/adapters/*"]
    }
  }
}
```
And ensure Jest config has `moduleNameMapper` set accordingly.

#### `cdk-nag: AwsSolutions-IAM4 - The IAM user, role, or group uses AWS managed policies`

**Cause:** Using broad managed policies like `AdministratorAccess`.  
**Fix:** Replace with scoped inline policies or use `grant*` methods:
```typescript
// ❌ Don't do this
role.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AmazonDynamoDBFullAccess'));

// ✅ Do this instead
table.grantReadWriteData(fn);
```

#### `Docker: Cannot connect to the Docker daemon`

**Cause:** Docker Desktop not running.  
**Fix:** Start Docker Desktop. On WSL2, ensure Docker integration is enabled for your distro.

#### `CDK deploy fails with "Resource already exists"`

**Cause:** Resource name collision (often from hardcoded physical names).  
**Fix:** Remove hardcoded `tableName`, `functionName`, etc. Let CDK generate unique names:
```typescript
// ❌ Fragile
new Table(this, 'Orders', { tableName: 'orders-table' });

// ✅ Resilient
new Table(this, 'Orders', { /* tableName omitted — CDK generates it */ });
```

#### `thothctl scan` reports architecture violation

**Cause:** Domain code imports AWS SDK or adapter code.  
**Fix:** Move the AWS-specific code to an adapter and inject it via a port:
```typescript
// ❌ In domain/services/
import { DynamoDBClient } from '@aws-sdk/client-dynamodb'; // VIOLATION

// ✅ In domain/ports/
export interface OrderRepository {
  save(order: Order): Promise<void>;
}

// ✅ In adapters/outbound/
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
export class DynamoOrderRepository implements OrderRepository { ... }
```

#### `npm test` passes locally but fails in CI

**Cause:** Usually timezone, environment variable, or dependency caching issues.  
**Fix:**
1. Ensure tests don't depend on local time — use UTC
2. Check that all env vars are set in CI config
3. Run `npm ci` (not `npm install`) in CI for deterministic installs

#### `AWS credentials not found`

**Fix:**
```bash
aws sso login --profile <your-profile>
export AWS_PROFILE=<your-profile>
```

---

## 12. Learning Resources

### Framework documentation (start here)

| Doc | What you'll learn |
|-----|------------------|
| `docs/01-philosophy.md` | Why this framework exists |
| `docs/02-architecture.md` | Deep dive on hexagonal pattern |
| `docs/05-ai-dlc.md` | Full AI-DLC methodology |
| `docs/07-thothctl.md` | Complete ThothCTL reference |
| `docs/10-testing-strategy.md` | Testing pyramid and patterns |
| `docs/15-observability.md` | Logging, metrics, alarms |
| `docs/20-pipeline.md` | CI/CD pipeline details |

### AWS CDK

- [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/)
- [CDK Patterns](https://cdkpatterns.com/)

### Serverless on AWS

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Serverless Land Patterns](https://serverlessland.com/patterns)
- [AWS Well-Architected Serverless Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html)

### Hexagonal Architecture

- [Alistair Cockburn — Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [AWS Prescriptive Guidance — Hexagonal Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/welcome.html)

### Trunk-Based Development

- [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/)

---

## Quick Start Checklist

Copy this and check off items as you go:

```
[ ] Run `thothctl init env` and verify all tools installed
[ ] Clone the repo and run `npm install`
[ ] Run `npm test` — all tests pass
[ ] Read `.kiro/steering.md` for project context
[ ] Read `.kiro/rules/` for coding conventions
[ ] Start Docker and run `docker compose up -d`
[ ] Run `npm run dev` to see local execution
[ ] Do an express deploy: `cdk deploy --all --profile dev --hotswap`
[ ] Try "Using AI-DLC, add a health check endpoint" as practice
[ ] Open your first PR using the git workflow above
```

**You're ready.** Welcome to the team. 🚀
