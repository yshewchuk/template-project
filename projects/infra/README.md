# Infrastructure

AWS infrastructure managed with Terraform.

## Stack

- **Tool:** Terraform
- **Linter:** tflint + tfsec
- **Test Framework:** terratest

## Development

```bash
# Initialize
terraform init

# Plan
terraform plan

# Lint
tflint
tfsec .
```

## Directory Structure

```
infra/
└── ...   # Terraform modules and configuration
```
