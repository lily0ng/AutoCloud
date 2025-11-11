---

# How to Use EC2 YAML Templates

This guide explains how to deploy the provided EC2 YAML templates using AWS services.

---
**
## Prerequisites

Before deploying the templates, ensure you have the following

1. **AWS CLI Installed**  
   Install the AWS Command Line Interface ([Download AWS CLI](https://aws.amazon.com/cli/)).

2. **AWS Account and IAM Role**  
   - Set up an AWS account.
   - Ensure you have an IAM role or user with sufficient permissions (e.g., EC2, VPC, CloudFormation).

3. **AWS CLI Configured**  
   Run the following command to configure your credentials
   ```bash
   aws configure
   ```
   Enter your:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., `us-east-1`)
   - Default output format (e.g., `json`)

4. **YAML Template Files**  
   Save the YAML templates as separate files
   - `ec2-management.yml`
   - `ec2-logging.yml`
   - `ec2-monitoring.yml`
   - `ec2-scaling.yml`
   - `ec2-network.yml`

---

## Steps to Deploy the YAML Templates

### 1. **Validate the YAML Template**

Before deploying, validate the template using the AWS CLI

```bash
aws cloudformation validate-template --template-body file://<template-file>
```


```bash
aws cloudformation validate-template --template-body file://ec2-management.yml
```

If the template is valid, you will see the output confirming it.

---

### 2. **Deploy the Template**

Use the following command to create a stack using the template

```bash
aws cloudformation create-stack --stack-name <stack-name> --template-body file://<template-file>
```

Example for deploying `ec2-management.yml`:
```bash
aws cloudformation create-stack --stack-name ec2-management-stack --template-body file://ec2-management.yml
```

---

### 3. **Monitor the Stack Deployment**

Check the status of the stack deployment with this command

```bash
aws cloudformation describe-stacks --stack-name <stack-name>
```


```bash
aws cloudformation describe-stacks --stack-name ec2-management-stack
```

---

### 4. **Update the Stack**

If you make changes to the YAML template, update the existing stack

```bash
aws cloudformation update-stack --stack-name <stack-name> --template-body file://<template-file>
```

---

### 5. **Delete the Stack**

When the resources are no longer needed, delete the stack to avoid unnecessary costs

```bash
aws cloudformation delete-stack --stack-name <stack-name>
```


```bash
aws cloudformation delete-stack --stack-name ec2-management-stack
```

---

## Additional Notes

- Replace `<stack-name>` with a unique name for each stack.
- Replace `<template-file>` with the file name of the YAML template.
- Review each YAML file to customize configurations like instance type, AMI ID, and security groups.

[AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html).

