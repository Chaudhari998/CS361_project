import json
import time
import zmq
import http.client

def connect_socket():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Receiver running")
    receive_message(socket)

def receive_message(socket):
    while True:
        # Receive and parse the JSON message
        message_json = socket.recv_json()
        print(f"Message Received: {message_json}")

        if message_json == "END":
            print("Ending Receiver")
            socket.send_string("Ended Receiver")
            break

        # Perform currency conversion
        result_msg = perform_conversion(message_json)
        socket.send_json(result_msg)

def perform_conversion(message_json):
    convert_from = message_json['source_currency']
    convert_to = message_json['target_currency']
    amount = float(message_json['amount'])

    # Single API call to get both rates
    conn = http.client.HTTPConnection("data.fixer.io")
    url = f"/api/latest?access_key=c1ac9ab43f880df6293265dd830e85fb&symbols={convert_from},{convert_to}"
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()
    conversion = json.loads(data.decode("utf-8"))

    if conversion.get("success", False):
        rates = conversion["rates"]
        converted_amount = amount / rates[convert_from] * rates[convert_to]
        result = {
            "date": conversion["date"],
            "convert_from": convert_from,
            "convert_to": convert_to,
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2)
        }
    else:
        result = {"error": "Conversion failed"}
    
    return result

def main():
    connect_socket()

if __name__ == "__main__":
    main()
