package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/accessanalyzer"
	"github.com/aws/aws-sdk-go-v2/service/accessanalyzer/types"
)

type AccessAnalyzer struct {
	client *accessanalyzer.Client
	ctx    context.Context
}

func NewAccessAnalyzer(region string) (*AccessAnalyzer, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &AccessAnalyzer{
		client: accessanalyzer.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *AccessAnalyzer) CreateAnalyzer(analyzerName string) (string, error) {
	input := &accessanalyzer.CreateAnalyzerInput{
		AnalyzerName: &analyzerName,
		Type:         types.TypeAccount,
	}

	result, err := m.client.CreateAnalyzer(m.ctx, input)
	if err != nil {
		return "", fmt.Errorf("failed to create analyzer: %w", err)
	}

	analyzerArn := *result.Arn
	log.Printf("Successfully created access analyzer: %s", analyzerName)
	return analyzerArn, nil
}

func (m *AccessAnalyzer) ListFindings(analyzerArn string) error {
	input := &accessanalyzer.ListFindingsInput{
		AnalyzerArn: &analyzerArn,
	}

	result, err := m.client.ListFindings(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to list findings: %w", err)
	}

	log.Printf("Found %d findings", len(result.Findings))
	for _, finding := range result.Findings {
		log.Printf("Finding: %s - %s", *finding.Id, finding.Status)
	}

	return nil
}

func main() {
	analyzer, err := NewAccessAnalyzer("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	analyzerArn, err := analyzer.CreateAnalyzer("autocloud-analyzer")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Analyzer ARN: %s\n", analyzerArn)
}
