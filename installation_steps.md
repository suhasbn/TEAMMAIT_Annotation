Prodigy Audio Annotation Setup and Usage Guide

### 0. Windows Setup (for Windows users only):
## Install Windows Subsystem for Linux (WSL):
* Open PowerShell as Administrator:
  * Click on the Start menu or press the Windows key.
  * Type "PowerShell" (without quotes).
  * In the search results, you should see "Windows PowerShell" or "PowerShell".
  * Right-click on "Windows PowerShell" or "PowerShell".
  * In the menu that appears, click on "Run as administrator".
  * If a User Account Control prompt appears asking "Do you want to allow this app to make changes to your device?", click "Yes".
* In the PowerShell window that opens, type or copy-paste the following command and press Enter: `wsl --install`
* Wait for the installation to complete. You may see various messages about the installation progress.
* Once it's done, you'll need to restart your computer. Save any open work, close all programs, and restart your computer.
* After your computer restarts, WSL will finish the installation. A new window will open automatically, asking you to create a username and password for your Linux distribution. Follow the prompts to do so.
* You can now use WSL by typing "wsl" in the Start menu and pressing Enter.

`Windows users: Please refer to the notes at the bottom.`

### 1. TKI (Tunnel Keeper Installation) Setup (Needs to be done only once):
* Visit: https://emory.service-now.com/sp?sys_kb_id=fe1f88c61bc8f3cc8508437ead4bcbf9&id=kb_article_view&sysparm_rank=1&sysparm_tsqueryId=5bba49f01b20425062e42fc42a4bcb92
* Follow the instructions to install TKI on your local machine.

### 2. EC2 Instance Setup (Needs to be done only once):
* Log into the Emory AWS Console.
* In the top right corner, ensure you're in the `N. Virginia (us-east-1)` region.
* In the search bar at the top, type `EC2` and select it from the results.
* In the EC2 dashboard, navigate to `Images -> AMIs`.
* Search for `teammate-template` in the AMI list.
* Select the AMI and click `Launch instance from AMI`.
* In the instance configuration page:
  * Choose an appropriate instance type (e.g., t2.micro for testing, or as recommended).
  * Under `Advanced details`, find `IAM instance profile` and select `TEAMMAITEC2accessingS3`.
* Configure the security group with the following inbound rules:
  * `launch-wizard-1`
* Review and launch the instance. Select an existing key pair or create a new one.
* Note down the instance ID and public IP address.

### 3. Local Setup (Needs to be done only once):
* Locate your TKI installation directory.
* In the 'bin' folder of your TKI installation, create or edit `start_prodigy_service.sh`.
* Update `start_prodigy_service.sh` with your EC2 instance details:
      
      ```bash
      #!/bin/bash
      EC2_INSTANCE_ID="your-instance-id"
      EC2_USER="ec2-user"
      EC2_IP="your-instance-public-ip"
      EC2_KEY="/path/to/your/key.pem"
      REGION="us-east-1"
      # ... (rest of the script)
      ```
* Ensure `ec2_script.sh` is also in the same `bin` folder.


### 4. Starting the Annotation Session (Needs to be done whenever we need to annotate):
* Connect to the Emory VPN (Big-IP).
* Open a terminal and navigate to your TKI 'bin' folder.
* Run the TKI to establish a secure connection:
      ```
      ./tki
      ```
  and follow the instructions (as as entering your `Emory username and password`, as well as selecting `us-east-1`. 
* Once connected, start the Prodigy service:
      ```
      ./start_prodigy_service.sh (On UNIX)
      OR
      bash start_prodigy_service.sh (On WSL)
      ```
* Wait for the script to complete. It will output a URL (http://your-ip-address:8090).
* Copy and paste this URL in your web browser to access the Prodigy interface.

### 5. Annotating (Done during every session):
* In the Prodigy interface, you'll see an audio player, transcription, and annotation options.
* Listen to the audio, review the transcription, and add your annotations.
* Use the provided labels to categorize the audio content.
* Submit your annotation and move to the next audio file.
* Make sure you're saving your progress regularly by clicking the save button on top left. You should get a notification box on the bottom right confirming that your annotations have been saved.

### 6. Ending the Session (At the end of every annotation session):
* When finished annotating, make sure you save your progress one last time, before closing the Prodigy browser tab.
* In your terminal (still connected via TKI), run:
      ```
      sudo fuser -k 8090/tcp
      ```
* Then, type `exit` to return back to the `bin/` folder.

### 7. Stopping the EC2 Instance (Needs to be done whenever we need to annotate):
* Run the stop script:
      ```
      ./stop_prodigy_service.sh (On UNIX)
      OR
      bash stop_prodigy_service.sh (On WSL)
      ```
* Wait for confirmation that the EC2 instance has stopped.

# Notes:
- When the guide refers to opening a terminal, use your WSL terminal (By typing "wsl" in the Start menu).
- File paths in WSL use forward slashes (/), while Windows typically uses backslashes (\).
- If using WSL, your `Windows C:` drive is typically accessible at `/mnt/c/`.
- Make sure to adjust any file paths in the scripts to match your Windows environment.
- When running scripts in WSL, you may need to use bash before the script name, e.g., `bash start_prodigy_service.sh`.
- If you encounter any issues, please contact me at [bnsuhas@psu.edu](mailto:bnsuhas@psu.edu).
- Remember to stop your EC2 instance after each session to avoid unnecessary charges.
