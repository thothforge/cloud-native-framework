# 22 — Multi-Account Landing Zone

> Enterprise AWS governance with AWS Control Tower, SCPs, RCPs, and CDK Pipelines.

---

## Table of Contents

1. [Account Structure](#1-account-structure)
2. [AWS Control Tower](#2-aws-control-tower)
3. [Service Control Policies (SCPs)](#3-service-control-policies-scps)
4. [Resource Control Policies (RCPs)](#4-resource-control-policies-rcps)
5. [Permission Boundaries](#5-permission-boundaries)
6. [Networking](#6-networking)
7. [Centralized Logging](#7-centralized-logging)
8. [Pipeline Account](#8-pipeline-account)
9. [Cost Management](#9-cost-management)
10. [Bootstrap](#10-bootstrap)

---

## 1. Account Structure

### Organizational Units (OUs)

```mermaid
graph TD
    Root[AWS Organization Root]
    Root --> MgmtOU[Management OU]
    Root --> SecurityOU[Security OU]
    Root --> InfraOU[Infrastructure OU]
    Root --> WorkloadOU[Workload OU]
    Root --> SandboxOU[Sandbox OU]

    MgmtOU --> MgmtAcct["Management Account<br/>(Org master, billing)"]
    
    SecurityOU --> AuditAcct["Audit Account<br/>(CloudTrail, Config, GuardDuty)"]
    SecurityOU --> LogArchiveAcct["Log Archive Account<br/>(Immutable log storage)"]

    InfraOU --> SharedSvcAcct["Shared Services Account<br/>(DNS, CI/CD pipelines, artifacts)"]
    InfraOU --> NetworkAcct["Network Account<br/>(Transit Gateway, DNS hub)"]

    WorkloadOU --> DevOU[Dev OU]
    WorkloadOU --> StagingOU[Staging OU]
    WorkloadOU --> ProdOU[Prod OU]

    DevOU --> DevAcct["Dev Account(s)"]
    StagingOU --> StagingAcct["Staging Account(s)"]
    ProdOU --> ProdAcct["Prod Account(s)"]
```

### Account Responsibilities

| Account | Purpose | Key Services |
|---------|---------|--------------|
| **Management** | Organization root, billing, SCPs | AWS Organizations, SSO |
| **Audit** | Security monitoring, compliance | CloudTrail, Config, GuardDuty, Security Hub |
| **Log Archive** | Immutable centralized logs | S3 (Object Lock), Athena |
| **Shared Services** | CI/CD pipelines, shared artifacts | CodePipeline, ECR, S3 Artifacts |
| **Network** | Centralized networking | Transit Gateway, Route 53, VPC |
| **Dev / Staging / Prod** | Workload isolation per environment | Lambda, API Gateway, DynamoDB, etc. |

### Design Principles

- **Least privilege**: Each account has only the permissions it needs.
- **Blast radius reduction**: A compromise in Dev cannot reach Prod.
- **Separation of duties**: Security team owns Audit; platform team owns Shared Services.
- **Immutable audit trail**: Log Archive uses S3 Object Lock with governance mode.

---

## 2. AWS Control Tower

### Initial Setup

```bash
# Control Tower is set up via the AWS Console, but account vending is automated:
aws controltower create-managed-account \
  --account-name "prod-workload-team-a" \
  --account-email "prod-team-a@company.com" \
  --organizational-unit-name "Prod" \
  --sso-user-email "admin@company.com"
```

### Account Factory (AFT)

Use **Account Factory for Terraform (AFT)** or **CDK-based custom account vending**:

```typescript
// CDK: Invoke Control Tower Account Factory via Service Catalog
import { CfnProvisionedProduct } from 'aws-cdk-lib/aws-servicecatalog';

new CfnProvisionedProduct(this, 'NewWorkloadAccount', {
  productName: 'AWS Control Tower Account Factory',
  provisioningArtifactName: 'AWS Control Tower Account Factory',
  provisionedProductName: 'team-b-prod',
  provisioningParameters: [
    { key: 'AccountName', value: 'team-b-prod' },
    { key: 'AccountEmail', value: 'team-b-prod@company.com' },
    { key: 'ManagedOrganizationalUnit', value: 'Prod' },
    { key: 'SSOUserEmail', value: 'admin@company.com' },
    { key: 'SSOUserFirstName', value: 'Admin' },
    { key: 'SSOUserLastName', value: 'User' },
  ],
});
```

### Guardrails

#### Preventive Guardrails (SCPs)

| Guardrail | Effect |
|-----------|--------|
| Disallow changes to CloudTrail | Prevents tampering with audit logs |
| Disallow deletion of log archive | Protects immutable storage |
| Disallow changes to AWS Config | Maintains compliance visibility |
| Disallow public access to S3 | Prevents data leakage |

#### Detective Guardrails (AWS Config Rules)

| Guardrail | Detection |
|-----------|-----------|
| EBS volumes encrypted | Flags unencrypted volumes |
| RDS instances not public | Detects public DB endpoints |
| MFA enabled for root | Alerts if root lacks MFA |
| S3 bucket logging enabled | Ensures access logging |

```bash
# Enable a Control Tower guardrail
aws controltower enable-control \
  --control-identifier "arn:aws:controltower:us-east-1::control/AWS-GR_DISALLOW_CROSS_REGION_NETWORKING" \
  --target-identifier "arn:aws:organizations::111111111111:ou/o-abc123/ou-defg-456789"
```

---

## 3. Service Control Policies (SCPs)

SCPs are attached at the OU level and define the **maximum permissions** for all accounts within.

### 3.1 Deny Direct Deploy (Must Use Pipeline)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDirectDeploy",
      "Effect": "Deny",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "apigateway:POST",
        "apigateway:PUT",
        "apigateway:PATCH",
        "dynamodb:CreateTable",
        "dynamodb:DeleteTable"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalOrgPaths": [
            "o-orgid/r-rootid/ou-infraid/"
          ]
        },
        "ArnNotLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:role/cdk-*-deploy-role-*",
            "arn:aws:iam::*:role/cdk-*-cfn-exec-role-*",
            "arn:aws:iam::*:role/AWSControlTowerExecution"
          ]
        }
      }
    }
  ]
}
```

### 3.2 Deny Disable Security Services

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDisableSecurity",
      "Effect": "Deny",
      "Action": [
        "guardduty:DeleteDetector",
        "guardduty:DisassociateFromMasterAccount",
        "guardduty:UpdateDetector",
        "securityhub:DisableSecurityHub",
        "securityhub:DeleteMembers",
        "config:StopConfigurationRecorder",
        "config:DeleteConfigurationRecorder",
        "config:DeleteDeliveryChannel",
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "access-analyzer:DeleteAnalyzer"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:role/AWSControlTowerExecution",
            "arn:aws:iam::*:role/OrganizationAccountAccessRole"
          ]
        }
      }
    }
  ]
}
```

### 3.3 Deny Public S3

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyS3PublicAccess",
      "Effect": "Deny",
      "Action": "s3:PutBucketPublicAccessBlock",
      "Resource": "arn:aws:s3:::*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-public-access-block-configuration-block-public-acls": "true",
          "s3:x-amz-public-access-block-configuration-block-public-policy": "true",
          "s3:x-amz-public-access-block-configuration-ignore-public-acls": "true",
          "s3:x-amz-public-access-block-configuration-restrict-public-buckets": "true"
        }
      }
    },
    {
      "Sid": "DenyS3PublicObjectACLs",
      "Effect": "Deny",
      "Action": [
        "s3:PutBucketAcl",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": [
            "public-read",
            "public-read-write",
            "authenticated-read"
          ]
        }
      }
    }
  ]
}
```

### 3.4 Region Restriction

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "a]4m:*",
        "iam:*",
        "sts:*",
        "organizations:*",
        "route53:*",
        "cloudfront:*",
        "support:*",
        "billing:*",
        "health:*",
        "trustedadvisor:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    }
  ]
}
```

### CDK Implementation of SCPs

```typescript
import * as organizations from 'aws-cdk-lib/aws-organizations';
import * as iam from 'aws-cdk-lib/aws-iam';

// SCP: Deny direct deploy
const denyDirectDeployScp = new organizations.CfnPolicy(this, 'DenyDirectDeploy', {
  name: 'deny-direct-deploy',
  description: 'Force all deployments through CI/CD pipeline roles',
  type: 'SERVICE_CONTROL_POLICY',
  content: JSON.stringify({
    Version: '2012-10-17',
    Statement: [{
      Sid: 'DenyDirectDeploy',
      Effect: 'Deny',
      Action: [
        'cloudformation:CreateStack',
        'cloudformation:UpdateStack',
        'cloudformation:DeleteStack',
        'lambda:CreateFunction',
        'lambda:UpdateFunctionCode',
      ],
      Resource: '*',
      Condition: {
        ArnNotLike: {
          'aws:PrincipalArn': [
            'arn:aws:iam::*:role/cdk-*-deploy-role-*',
            'arn:aws:iam::*:role/cdk-*-cfn-exec-role-*',
          ],
        },
      },
    }],
  }),
  targetIds: ['ou-workload-id'], // Attach to Workload OU
});
```
