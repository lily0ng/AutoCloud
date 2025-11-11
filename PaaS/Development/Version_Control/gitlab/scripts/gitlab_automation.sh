#!/bin/bash

# GitLab Automation Script
# This script helps manage GitLab projects and configurations

GITLAB_URL="https://gitlab.yourdomain.com"
GITLAB_TOKEN="your-token-here"

# Function to create a new project
create_project() {
    local project_name=$1
    local description=$2
    local visibility=${3:-private}

    curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
         --data "name=$project_name&description=$description&visibility=$visibility" \
         "$GITLAB_URL/api/v4/projects"
}

# Function to create project branch protection rules
set_branch_protection() {
    local project_id=$1
    local branch=${2:-main}

    curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
         --data "name=$branch&push_access_level=40&merge_access_level=40&unprotect_access_level=40" \
         "$GITLAB_URL/api/v4/projects/$project_id/protected_branches"
}

# Function to setup default project labels
setup_labels() {
    local project_id=$1
    local labels=(
        "bug|#FF0000|Bug reports"
        "feature|#00FF00|New features"
        "documentation|#0000FF|Documentation updates"
        "security|#FF4500|Security related issues"
    )

    for label in "${labels[@]}"; do
        IFS="|" read -r name color description <<< "$label"
        curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
             --data "name=$name&color=$color&description=$description" \
             "$GITLAB_URL/api/v4/projects/$project_id/labels"
    done
}

# Function to setup merge request templates
setup_mr_templates() {
    local project_id=$1
    
    # Create .gitlab/merge_request_templates directory
    curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
         --data "branch=main&content=# Merge Request Template\n\n## Description\n\n## Changes Made\n\n## Testing Done\n\n## Checklist\n- [ ] Tests\n- [ ] Documentation\n- [ ] Code Review&path=.gitlab/merge_request_templates/default.md" \
         "$GITLAB_URL/api/v4/projects/$project_id/repository/files"
}

# Function to enable CI/CD features
setup_cicd() {
    local project_id=$1
    
    curl --request PUT --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
         --data "builds_access_level=enabled&container_registry_access_level=enabled" \
         "$GITLAB_URL/api/v4/projects/$project_id"
}

# Main execution
case "$1" in
    "create")
        create_project "$2" "$3" "$4"
        ;;
    "protect")
        set_branch_protection "$2" "$3"
        ;;
    "labels")
        setup_labels "$2"
        ;;
    "templates")
        setup_mr_templates "$2"
        ;;
    "cicd")
        setup_cicd "$2"
        ;;
    "setup-all")
        project_id=$(create_project "$2" "$3" "$4" | jq '.id')
        set_branch_protection "$project_id"
        setup_labels "$project_id"
        setup_mr_templates "$project_id"
        setup_cicd "$project_id"
        ;;
    *)
        echo "Usage: $0 {create|protect|labels|templates|cicd|setup-all} [args...]"
        exit 1
        ;;
esac
