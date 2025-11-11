#!/bin/bash

# Terraform Automation Wrapper

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TERRAFORM_DIR=${TERRAFORM_DIR:-"./terraform"}
ENVIRONMENT=${ENVIRONMENT:-"dev"}
STATE_BUCKET=${STATE_BUCKET:-""}
BACKEND_CONFIG=${BACKEND_CONFIG:-""}

echo -e "${BLUE}🏗️  Terraform Wrapper${NC}"
echo "================================"

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform not found${NC}"
    exit 1
fi

cd "$TERRAFORM_DIR"

function tf_init() {
    echo -e "${BLUE}🔧 Initializing Terraform...${NC}"
    
    INIT_ARGS=""
    if [ -n "$BACKEND_CONFIG" ]; then
        INIT_ARGS="-backend-config=$BACKEND_CONFIG"
    fi
    
    terraform init $INIT_ARGS
    echo -e "${GREEN}✅ Initialization complete${NC}"
}

function tf_validate() {
    echo -e "${BLUE}✓ Validating configuration...${NC}"
    terraform validate
    echo -e "${GREEN}✅ Validation passed${NC}"
}

function tf_format() {
    echo -e "${BLUE}📝 Formatting code...${NC}"
    terraform fmt -recursive
    echo -e "${GREEN}✅ Formatting complete${NC}"
}

function tf_plan() {
    echo -e "${BLUE}📋 Creating execution plan...${NC}"
    terraform plan \
        -var-file="environments/$ENVIRONMENT.tfvars" \
        -out="tfplan-$ENVIRONMENT"
    echo -e "${GREEN}✅ Plan created${NC}"
}

function tf_apply() {
    echo -e "${YELLOW}🚀 Applying changes...${NC}"
    read -p "Are you sure you want to apply? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        terraform apply "tfplan-$ENVIRONMENT"
        echo -e "${GREEN}✅ Apply complete${NC}"
    else
        echo -e "${YELLOW}⚠️  Apply cancelled${NC}"
    fi
}

function tf_destroy() {
    echo -e "${RED}💥 Destroying infrastructure...${NC}"
    read -p "Are you ABSOLUTELY sure? Type 'destroy' to confirm: " confirm
    
    if [ "$confirm" = "destroy" ]; then
        terraform destroy \
            -var-file="environments/$ENVIRONMENT.tfvars" \
            -auto-approve
        echo -e "${GREEN}✅ Destroy complete${NC}"
    else
        echo -e "${YELLOW}⚠️  Destroy cancelled${NC}"
    fi
}

function tf_output() {
    echo -e "${BLUE}📤 Terraform Outputs:${NC}"
    terraform output
}

function tf_state_list() {
    echo -e "${BLUE}📋 State Resources:${NC}"
    terraform state list
}

function tf_graph() {
    echo -e "${BLUE}🕸️  Generating dependency graph...${NC}"
    terraform graph | dot -Tpng > graph.png
    echo -e "${GREEN}✅ Graph saved to graph.png${NC}"
}

function tf_import() {
    RESOURCE=$1
    ID=$2
    echo -e "${BLUE}📥 Importing resource: $RESOURCE${NC}"
    terraform import "$RESOURCE" "$ID"
    echo -e "${GREEN}✅ Import complete${NC}"
}

case "${1:-plan}" in
    init)
        tf_init
        ;;
    validate)
        tf_validate
        ;;
    format)
        tf_format
        ;;
    plan)
        tf_init
        tf_validate
        tf_plan
        ;;
    apply)
        tf_apply
        ;;
    destroy)
        tf_destroy
        ;;
    output)
        tf_output
        ;;
    state)
        tf_state_list
        ;;
    graph)
        tf_graph
        ;;
    import)
        tf_import "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {init|validate|format|plan|apply|destroy|output|state|graph|import}"
        exit 1
        ;;
esac
