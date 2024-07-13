#!/bin/bash

# Define your EC2 instance details
EC2_INSTANCE_ID="i-0ca6b1c9410ffa7c7"
EC2_USER="ec2-user"
EC2_IP="10.65.201.85"
EC2_KEY="/Users/suhas/Docs/WHI_Lab/Amanda_Speech_Transcript_Data/TEAMMAIT_Annotation_Trial/teammait-key-pair.pem"
REGION="us-east-1"

# Start the EC2 instance
aws ec2 start-instances --instance-ids $EC2_INSTANCE_ID --region $REGION

# Wait for the instance to be running
echo "Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids $EC2_INSTANCE_ID --region $REGION

# Function to check if SSH is ready
check_ssh() {
    ssh -i $EC2_KEY -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP exit 2>/dev/null
    return $?
}

# Wait for SSH to be ready
echo "Waiting for SSH to be ready..."
while ! check_ssh; do
    echo "SSH not ready yet, waiting 10 seconds..."
    sleep 10
done

echo "SSH is ready. Proceeding with file transfer and script execution."

# Copy the script to the EC2 instance
scp -i $EC2_KEY ec2_script.sh $EC2_USER@$EC2_IP:/home/ec2-user/

# SSH into the EC2 instance and run the script
ssh -tt -i $EC2_KEY $EC2_USER@$EC2_IP "bash /home/ec2-user/ec2_script.sh"

echo "SSH session ended. You can now stop the EC2 instance if needed."