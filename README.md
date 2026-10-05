# Meshtastic Monitoring Program

## What is this?

This program runs on a raspberry pi connected to a Meshtastic device (which will hence be referred to as the radio). Upon receiving a packet from the radio, this program will determine what actions to take,
which typically involves sending the information to a Cloudflare worker to be stored in a database.
