import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const config = new pulumi.Config();
const environmentName = config.get("environment") || "production";

// VPC
const vpc = new awsx.ec2.Vpc(`${environmentName}-vpc`, {
    cidrBlock: "10.0.0.0/16",
    numberOfAvailabilityZones: 2,
    tags: { Name: `${environmentName}-vpc` },
});

// Security Group
const securityGroup = new aws.ec2.SecurityGroup(`${environmentName}-sg`, {
    vpcId: vpc.vpcId,
    ingress: [
        { protocol: "tcp", fromPort: 80, toPort: 80, cidrBlocks: ["0.0.0.0/0"] },
        { protocol: "tcp", fromPort: 443, toPort: 443, cidrBlocks: ["0.0.0.0/0"] },
    ],
    egress: [
        { protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"] },
    ],
});

// ECS Cluster
const cluster = new aws.ecs.Cluster(`${environmentName}-cluster`);

// Load Balancer
const alb = new awsx.lb.ApplicationLoadBalancer(`${environmentName}-alb`, {
    subnetIds: vpc.publicSubnetIds,
    securityGroups: [securityGroup.id],
});

// ECS Service
const service = new awsx.ecs.FargateService(`${environmentName}-service`, {
    cluster: cluster.arn,
    taskDefinitionArgs: {
        container: {
            image: "autocloud/app:latest",
            cpu: 512,
            memory: 1024,
            essential: true,
            portMappings: [{ containerPort: 8080, targetGroup: alb.defaultTargetGroup }],
        },
    },
    desiredCount: 3,
});

export const url = alb.loadBalancer.dnsName;
