#!/bin/bash
# AWS EC2 Launch Template Automation

set -e

TEMPLATE_NAME=${1:-autocloud-template}
INSTANCE_TYPE=${2:-t3.medium}
AMI_ID=${3:-ami-0c55b159cbfafe1f0}

echo "Creating EC2 Launch Template..."
echo "Template Name: $TEMPLATE_NAME"
echo "Instance Type: $INSTANCE_TYPE"
echo "AMI ID: $AMI_ID"

aws ec2 create-launch-template \
    --launch-template-name $TEMPLATE_NAME \
    --version-description "AutoCloud Launch Template" \
    --launch-template-data "{
        \"ImageId\": \"$AMI_ID\",
        \"InstanceType\": \"$INSTANCE_TYPE\",
        \"KeyName\": \"autocloud-key\",
        \"SecurityGroupIds\": [\"sg-12345678\"],
        \"TagSpecifications\": [{
            \"ResourceType\": \"instance\",
            \"Tags\": [{
                \"Key\": \"Name\",
                \"Value\": \"AutoCloud-Instance\"
            }]
        }],
        \"UserData\": \"$(base64 <<< '#!/bin/bash
            yum update -y
            yum install -y docker
            systemctl start docker
            systemctl enable docker
        ')\"
    }"

echo "Launch template created successfully!"
