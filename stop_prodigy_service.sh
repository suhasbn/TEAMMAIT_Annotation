#!/bin/bash

# Define your EC2 instance details
EC2_INSTANCE_ID="i-0ca6b1c9410ffa7c7"
REGION="us-east-1"

# Stop the EC2 instance
echo "Stopping the EC2 instance..."
aws ec2 stop-instances --instance-ids $EC2_INSTANCE_ID --region $REGION

# Wait for the instance to stop
echo "Waiting for instance to stop..."
aws ec2 wait instance-stopped --instance-ids $EC2_INSTANCE_ID --region $REGION

echo "EC2 instance has been successfully stopped."