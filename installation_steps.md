Prodigy Audio Annotation Setup and Usage Guide

1. TKI (Tunnel Keeper Installation) Setup:
   a. Visit: https://emory.service-now.com/sp?sys_kb_id=fe1f88c61bc8f3cc8508437ead4bcbf9&id=kb_article_view&sysparm_rank=1&sysparm_tsqueryId=5bba49f01b20425062e42fc42a4bcb92
   b. Follow the instructions to install TKI on your local machine.
   c. Ensure TKI is properly configured with your Emory credentials.

2. EC2 Instance Setup:
   a. Log into the AWS Console.
   b. In the top right corner, ensure you're in the "N. Virginia (us-east-1)" region.
   c. In the search bar at the top, type "EC2" and select it from the results.
   d. In the EC2 dashboard, navigate to "Images" -> "AMIs".
   e. Search for "teammate-template" in the AMI list.
   f. Select the AMI and click "Launch instance from AMI".
   g. In the instance configuration page:
      - Choose an appropriate instance type (e.g., t2.micro for testing, or as recommended).
      - Under "Advanced details", find "IAM instance profile" and select "TEAMMAITEC2accessingS3".
   h. Configure the security group with the following inbound rules:
      - Type: SSH, Protocol: TCP, Port Range: 22, Source: Your IP
      - Type: Custom TCP, Protocol: TCP, Port Range: 8090, Source: Your IP
      - Type: Custom TCP, Protocol: TCP, Port Range: 8070, Source: Your IP
   i. Review and launch the instance. Select an existing key pair or create a new one.
   j. Note down the instance ID and public IP address.

3. Local Setup:
   a. Locate your TKI installation directory.
   b. In the 'bin' folder of your TKI installation, create or edit 'start_prodigy_service.sh'.
   c. Update 'start_prodigy_service.sh' with your EC2 instance details:
      
      ```bash
      #!/bin/bash
      EC2_INSTANCE_ID="your-instance-id"
      EC2_USER="ec2-user"
      EC2_IP="your-instance-public-ip"
      EC2_KEY="/path/to/your/key.pem"
      REGION="us-east-1"
      # ... (rest of the script)
      ```
   d. Ensure 'ec2_script.sh' is also in the same 'bin' folder.

4. Starting the Annotation Session:
   a. Open a terminal and navigate to your TKI 'bin' folder.
   b. Run the TKI to establish a secure connection:
      ```
      ./tki
      ```
   c. Once connected, start the Prodigy service:
      ```
      ./start_prodigy_service.sh
      ```
   d. Wait for the script to complete. It will output a URL (http://your-ip-address:8090).
   e. Open this URL in your web browser to access the Prodigy interface.

5. Annotating:
   a. In the Prodigy interface, you'll see an audio player, transcription, and annotation options.
   b. Listen to the audio, review the transcription, and add your annotations.
   c. Use the provided labels to categorize the audio content.
   d. Submit your annotation and move to the next audio file.

6. Ending the Session:
   a. When finished annotating, close the Prodigy browser tab.
   b. In your terminal (still connected via TKI), run:
      ```
      sudo fuser -k 8090/tcp
      ```
   c. Exit the TKI session by typing 'exit'.

7. Stopping the EC2 Instance:
   a. In your local terminal (not TKI), navigate to the TKI 'bin' folder.
   b. Run the stop script:
      ```
      ./stop_prodigy_service.sh
      ```
   c. Wait for confirmation that the EC2 instance has stopped.

Notes:
- Ensure you're using a compatible web browser. Chrome and Firefox are configured to work with the audio files.
- If you encounter any issues, please contact the system administrator.
- Remember to stop your EC2 instance after each session to avoid unnecessary charges.
