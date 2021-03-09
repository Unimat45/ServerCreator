#!/bin/bash
# Author: James Chambers
# Minecraft Bedrock server startup script using screen
path="PATH"
pathName="NAME"
# Check if server is already started
if screen -list | grep -q "$pathName"; then
    echo "Server is already started!  Press screen -r $pathName to open it"
    exit 1
fi

# Check if network interfaces are up
NetworkChecks=0
DefaultRoute=$(route -n | awk '$4 == "UG" {print $2}')
while [ -z "$DefaultRoute" ]; do
    echo "Network interface not up, will try again in 1 second";
    sleep 1;
    DefaultRoute=$(route -n | awk '$4 == "UG" {print $2}')
    NetworkChecks=$((NetworkChecks+1))
    if [ $NetworkChecks -gt 20 ]; then
        echo "Waiting for network interface to come up timed out - starting server without network connection ..."
        break
    fi
done

# Change directory to server directory
cd $path

#Starting server
echo "Starting Minecraft server.  To view window type screen -r $pathName"
echo "To minimize the window and let the server run in the background, press Ctrl+A then Ctrl+D"
screen -dmS $pathName PaperMC
