#!/bin/bash
# IAM Security Audit Tool

set -e

echo "========================================="
echo "IAM Security Audit"
echo "========================================="

# Check for users without MFA
echo ""
echo "Users without MFA enabled:"
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    mfa_devices=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
    if [ -z "$mfa_devices" ]; then
        echo "  ⚠️  $user"
    fi
done

# Check for unused access keys
echo ""
echo "Checking for old/unused access keys (>90 days):"
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    aws iam list-access-keys --user-name $user --query 'AccessKeyMetadata[*].[AccessKeyId,CreateDate]' --output text | while read key_id create_date; do
        days_old=$(( ($(date +%s) - $(date -d "$create_date" +%s)) / 86400 ))
        if [ $days_old -gt 90 ]; then
            echo "  ⚠️  User: $user, Key: $key_id, Age: $days_old days"
        fi
    done
done

# Check for overly permissive policies
echo ""
echo "Checking for wildcard policies:"
aws iam list-policies --scope Local --query 'Policies[*].[PolicyName,Arn]' --output text | while read name arn; do
    version=$(aws iam get-policy --policy-arn $arn --query 'Policy.DefaultVersionId' --output text)
    doc=$(aws iam get-policy-version --policy-arn $arn --version-id $version --query 'PolicyVersion.Document' --output json)
    
    if echo "$doc" | grep -q '"Action":\s*"\*"'; then
        echo "  ⚠️  Policy with wildcard actions: $name"
    fi
done

# Check for root account usage
echo ""
echo "Checking root account activity:"
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=root --max-results 10 --query 'Events[*].[EventTime,EventName]' --output table

echo ""
echo "========================================="
echo "Audit completed"
echo "========================================="
