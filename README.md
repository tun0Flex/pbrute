ftp_flex.py:
    File Transfer Protocol, known as FTP, is actually a network protocol that, as the name suggests,
    allows files to be sent between a client's computer and a server on a computer network.

    FTP is a much older protocol than HTTP.

    usually runs on port 21

    We brute-force the ftp port with the following information

    --------------------------
    Host(İP/domain): 
    User: 
    Port([ftp]defaulth:21): 
    Wordlists(defaulth:wordlist_flex.txt): 
    -----------------------------------


ssh_flex.py:
    SSH or Secure Shell is a remote management protocol that allows users to control and organize their servers over the internet.
    SSH was created as a secure replacement for unencrypted Telnet. SSH uses encryption technique to ensure that all communications
    to and from the remote server are encrypted. It provides a mechanism
    to authenticate a remote user, transfer inputs from the client to the host, and send the output back to the client.

    -------------------------------------------------------------------------------
    python3 ssh_flex.py 111.111.1.1  -u john  -P /usr/share/eordlists/rockyou.txt
    ------------------------------------------------------------------------------

    
