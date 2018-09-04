# Live server architecture:
For a aws architure, setup:
- a iam user
- a vpc
- a ECS Kernel
- a RDS
- a ELB

# Deployment:
If CI is avalaible, configure the ci, for each tag pushed, to build images, push it to ECR and upload the tasks using blue-green deployment process with ECS. 
If no CI, build image locally and use ecs-cli to add a new ec2 and then update the service to do blue-green deployment with zero downtime.