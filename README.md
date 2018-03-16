# Jak shaver
Tool to allow commands execution (and updates) on the RT5350F based "Jak USB Streaming Stick"

With this toll you can execute commands on your streaming stick without cracking the housing open to expose the rx and tx tespoints.

## How does it work?

1. On startup the bCODA Jak app opens a http-server and another tcp-server on the smartphone that serves the files (and can change settings on the stick). 
2. As soon as the stick is connected the App sends an UDP-paket to port 20000 on the Jak IP address where it notifies the stick of the ip and port of the server (and some other informations).  
3. The stick connects back to the server on the smartphone and waits for commands or files.
4. To update the firmware the smartphone app sends the "upgrade firmware" command and includes a link to the internal http server to a file called "upgrade.txt" (and the password for the Wifi for some reason)
5. The stick executes the file upgrade.txt as shell script (and sets some environment variables if it is a real update)

So to emulate this behaviour we have to start a http server and a tcp-server and then send the UDP paket and wait for the stick to connect to the tcp-server so that we can send the update command with the link...


## How to use it?

Just place the command you want to execute on the stick in the [upgrade.txt] file and execute [shaver.py] while connected to the Jak wifi. (You might have to change the IP address in the python script to reflect your own)




