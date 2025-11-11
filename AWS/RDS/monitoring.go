package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatch"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatch/types"
)

type RDSMonitoring struct {
	client *cloudwatch.Client
	ctx    context.Context
}

func NewRDSMonitoring(region string) (*RDSMonitoring, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		return nil, err
	}

	return &RDSMonitoring{
		client: cloudwatch.NewFromConfig(cfg),
		ctx:    context.Background(),
	}, nil
}

func (m *RDSMonitoring) CreateAlarm(dbInstanceID, alarmName string, threshold float64) error {
	input := &cloudwatch.PutMetricAlarmInput{
		AlarmName:          &alarmName,
		ComparisonOperator: types.ComparisonOperatorGreaterThanThreshold,
		EvaluationPeriods:  intPtr(2),
		MetricName:         strPtr("CPUUtilization"),
		Namespace:          strPtr("AWS/RDS"),
		Period:             intPtr(300),
		Statistic:          types.StatisticAverage,
		Threshold:          &threshold,
		ActionsEnabled:     boolPtr(true),
		AlarmDescription:   strPtr("Alarm when CPU exceeds threshold"),
		Dimensions: []types.Dimension{
			{
				Name:  strPtr("DBInstanceIdentifier"),
				Value: &dbInstanceID,
			},
		},
	}

	_, err := m.client.PutMetricAlarm(m.ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create alarm: %w", err)
	}

	log.Printf("Successfully created CloudWatch alarm: %s", alarmName)
	return nil
}

func strPtr(s string) *string { return &s }
func intPtr(i int32) *int32   { return &i }
func boolPtr(b bool) *bool    { return &b }

func main() {
	monitor, err := NewRDSMonitoring("us-east-1")
	if err != nil {
		log.Fatal(err)
	}

	err = monitor.CreateAlarm("autocloud-db", "high-cpu-alarm", 80.0)
	if err != nil {
		log.Fatal(err)
	}
}
