# 11. Infrastructure and Deployment
### Infrastructure as Code
- **MVP (Local)**: The primary IaC tool will be Docker Compose. The docker-compose.yml file will define and configure the PostgreSQL service.
- **Future (AWS)**: The recommended IaC tool is Terraform.

### Deployment Strategy
- **MVP (Local)**: Deployment is handled by running docker-compose up.
- **Future (AWS)**: A CI/CD-driven strategy will be implemented using GitHub Actions.

### Environments
| Environment | Purpose | Details |
|-------------|---------|---------|
| Development | Local development | Run via docker-compose up on a developer's machine. |
| Staging     | Pre-production testing | A mirror of the production environment in AWS. |
| Production  | Live application     | The public-facing application running on AWS. |

### Environment Promotion Flow
The promotion of code will follow a standard Git-based workflow:
Feature Branch -> Pull Request -> main (triggers Staging deploy) -> Manual Promotion/Tag (triggers Production deploy).

### Rollback Strategy
- **MVP (Local)**: Rollback is achieved by checking out a previous Git commit.
- **Future (AWS)**: A Blue/Green deployment strategy is recommended.
