#!/bin/bash
# IAM Compliance Checker

set -e

echo "========================================="
echo "IAM Compliance Check"
echo "========================================="

PASS=0
FAIL=0

# Check 1: Password policy
echo ""
echo "1. Checking password policy..."
policy=$(aws iam get-account-password-policy 2>/dev/null || echo "NONE")
if [ "$policy" != "NONE" ]; then
    echo "  ✅ Password policy is configured"
    ((PASS++))
else
    echo "  ❌ No password policy configured"
    ((FAIL++))
fi

# Check 2: MFA on root account
echo ""
echo "2. Checking root account MFA..."
root_mfa=$(aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text)
if [ "$root_mfa" == "1" ]; then
    echo "  ✅ Root account MFA is enabled"
    ((PASS++))
else
    echo "  ❌ Root account MFA is NOT enabled"
    ((FAIL++))
fi

# Check 3: IAM users with console access have MFA
echo ""
echo "3. Checking MFA for console users..."
users_without_mfa=0
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    login_profile=$(aws iam get-login-profile --user-name $user 2>/dev/null || echo "NONE")
    if [ "$login_profile" != "NONE" ]; then
        mfa=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
        if [ -z "$mfa" ]; then
            echo "  ❌ User $user has console access without MFA"
            ((users_without_mfa++))
        fi
    fi
done

if [ $users_without_mfa -eq 0 ]; then
    echo "  ✅ All console users have MFA enabled"
    ((PASS++))
else
    echo "  ❌ $users_without_mfa users without MFA"
    ((FAIL++))
fi

# Check 4: No inline policies
echo ""
echo "4. Checking for inline policies..."
inline_count=$(aws iam list-users --query 'Users[*].UserName' --output text | xargs -I {} aws iam list-user-policies --user-name {} --query 'PolicyNames' --output text | wc -l)
if [ $inline_count -eq 0 ]; then
    echo "  ✅ No inline policies found"
    ((PASS++))
else
    echo "  ❌ Found $inline_count inline policies"
    ((FAIL++))
fi

# Summary
echo ""
echo "========================================="
echo "Compliance Summary"
echo "========================================="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ All compliance checks passed"
    exit 0
else
    echo "❌ Some compliance checks failed"
    exit 1
fi
