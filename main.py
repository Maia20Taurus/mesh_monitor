if __name__ == "__main__":
    import json
    import os
    import time

    import meshtastic
    import meshtastic.serial_interface
    import requests
    from pubsub import pub

    cf_id = os.getenv("ACCESS_CLIENT_ID")
    cf_secret = os.getenv("ACCESS_CLIENT_SECRET")
    print(f"access_id: {cf_id}, access_secret: {cf_secret}")

    # Set headers for the session:
    sesh = requests.Session()
    headers = {
        "CF-Access-Client-Id": cf_id,
        "CF-Access-Client-Secret": cf_secret,
        "Content-Type": "application/json",
    }
    sesh.headers.update(headers)

    def onReceiveMessage(packet, interface):
        try:
            if packet["decoded"]["portnum"] == "TEXT_MESSAGE_APP":
                message = packet["decoded"]["text"]
                id = packet["fromId"]
                timeUnixEpoch = packet["rxTime"]

                try:
                    response = sesh.post(
                        "https://maia395.dev/api/send-mesh-message",
                        json={
                            "message": message,
                            "nodeID": id,
                            "rxTimestamp": timeUnixEpoch,
                        },
                    )
                except Exception as e:
                    print(f"Exception occurred when posting message: {e}")

            elif packet["decoded"]["portnum"] == "NODEINFO_APP":
                nodeInfo = packet["decoded"]["user"]

                try:
                    response = sesh.post(
                        "https://maia395.dev/api/send-node-info",
                        json={
                            "nodeID": nodeInfo['id'],
                            "shortname": nodeInfo['shortName'],
                            "longname": nodeInfo['longName']
                        },
                    )
                except Exception as e:
                    print(f"Exception occurred when posting node info: {e}")



        except Exception as e:
            print(f"Could not key packet: {packet} \n {'-'*30} \n with exception {e}")

    def onConnection(interface, topic=pub.AUTO_TOPIC):
        print("Connected to device")
        print(f"self node user: {interface.getMyUser()}")

    def onLogLine(interface, line):
        print(f"LOG LINE: {line}")

    pub.subscribe(onReceiveMessage, "meshtastic.receive")
    pub.subscribe(onConnection, "meshtastic.connection.established")
    interface = meshtastic.serial_interface.SerialInterface()

    while True:
        time.sleep(1)