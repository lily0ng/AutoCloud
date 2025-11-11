package main

import (
	"fmt"
	"log"
)

type ComplianceChecker struct {
	rules []ComplianceRule
}

type ComplianceRule struct {
	ID          string
	Name        string
	Description string
	Check       func() bool
}

type ComplianceResult struct {
	Rule   ComplianceRule
	Passed bool
	Message string
}

func NewComplianceChecker() *ComplianceChecker {
	return &ComplianceChecker{
		rules: make([]ComplianceRule, 0),
	}
}

func (cc *ComplianceChecker) AddRule(rule ComplianceRule) {
	cc.rules = append(cc.rules, rule)
}

func (cc *ComplianceChecker) RunChecks() []ComplianceResult {
	results := make([]ComplianceResult, 0)
	
	log.Println("🔍 Running compliance checks...")
	
	for _, rule := range cc.rules {
		passed := rule.Check()
		result := ComplianceResult{
			Rule:   rule,
			Passed: passed,
		}
		
		if passed {
			result.Message = "Compliant"
		} else {
			result.Message = "Non-compliant"
		}
		
		results = append(results, result)
	}
	
	return results
}

func (cc *ComplianceChecker) GenerateReport(results []ComplianceResult) {
	fmt.Println("\n📋 Compliance Report")
	fmt.Println("====================")
	
	passed := 0
	failed := 0
	
	for _, result := range results {
		status := "❌"
		if result.Passed {
			status = "✅"
			passed++
		} else {
			failed++
		}
		
		fmt.Printf("%s %s: %s\n", status, result.Rule.Name, result.Message)
	}
	
	fmt.Printf("\nTotal: %d | Passed: %d | Failed: %d\n", len(results), passed, failed)
}

func main() {
	checker := NewComplianceChecker()
	
	checker.AddRule(ComplianceRule{
		ID:          "ENC-001",
		Name:        "Encryption at Rest",
		Description: "All data must be encrypted at rest",
		Check: func() bool {
			return true
		},
	})
	
	checker.AddRule(ComplianceRule{
		ID:          "IAM-001",
		Name:        "MFA Enabled",
		Description: "MFA must be enabled for all users",
		Check: func() bool {
			return false
		},
	})
	
	checker.AddRule(ComplianceRule{
		ID:          "NET-001",
		Name:        "VPC Flow Logs",
		Description: "VPC flow logs must be enabled",
		Check: func() bool {
			return true
		},
	})
	
	results := checker.RunChecks()
	checker.GenerateReport(results)
}
