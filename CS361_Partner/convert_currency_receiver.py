import json
import time
import zmq
import http.client


def connect_socket():
    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print(f"Receiver running")

    receive_message(socket)

def receive_message(socket):
    # Runs and waits for a message
    while True:
        #  Wait for next request from client
        message = socket.recv()
        message = str(message)
        print(f"Message Received: ", message, "\n")
        time.sleep(1)

        #  Send reply back to client and break
        if message != "":
            # If message is to end, ends
            if message == "b'END'":
                print("Ending Receiver \n")
                message = "Ended Receiver"
                socket.send_string(message)
                break

            # Otherwise, it gathers information from the message
            for i in range(len(message)):
                if message[i] == '{':
                    convert_from = message[i + 1] + message[i + 2] + message[i + 3]
                    convert_to = message[i + 6] + message[i + 7] + message[i + 8]
                    amount = ""
                    for i in range(13, len(message) - 2):
                        amount += message[i]

            # Connects to API to start the first conversion
            conn = http.client.HTTPConnection("data.fixer.io")
            currency = convert_from
            url = "/api/latest?access_key=c1ac9ab43f880df6293265dd830e85fb&symbols=" + currency
            payload = ""
            headers = {}

            # Gets message from the API
            conn.request("GET", url, payload, headers)
            res = conn.getresponse()
            data = res.read()
            conversion = json.loads(data.decode("utf-8"))
            success = conversion["success"]

            # IF API was successful it continues, else replies with fail
            if success == "false":
                socket.send(b"FAIL")
            else:
                # Gathers the first conversion
                print("First Conversion: ", data)
                rates = conversion["rates"]
                conversion_rates = rates[currency]

                # Starts the second conversion
                conn = http.client.HTTPConnection("data.fixer.io")
                currency = convert_to
                url = "/api/latest?access_key=c1ac9ab43f880df6293265dd830e85fb&symbols=" + currency
                payload = ""
                headers = {}

                conn.request("GET", url, payload, headers)
                res = conn.getresponse()
                data = res.read()
                conversion = json.loads(data.decode("utf-8"))
                success = conversion["success"]

                # If the second conversion was also successful
                if success == "false":
                    socket.send(b"FAIL")
                else:
                    # Gathers information from second conversion
                    print("Second Conversion: ", data)
                    date = conversion["date"]
                    rates = conversion["rates"]
                    total = rates[currency]

                    result = float(total)/float(conversion_rates)
                    result *= float(amount)
                    result = round(result, 2)

                    # Sends message back with the conversion
                    result_msg = "{" + date + ", " + convert_from + ", " + convert_to + ", " + str(amount) + ", " + str(result) + "}"
                    print("Message Sent: ", result_msg, "\n")
                    socket.send_string(result_msg)


def main():
    connect_socket()


if __name__ == "__main__":
    main()
