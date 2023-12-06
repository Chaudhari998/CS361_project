import zmq
import json
import time
import subprocess

def convert_currency(source_currency, target_currencies, amount):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    conversion_results = {}
    for target_currency in target_currencies:
        # Format the message for conversion
        message = json.dumps({
            'source_currency': source_currency,
            'target_currency': target_currency,
            'amount': amount
        })
        socket.send_string(message)

        # Wait for the response
        time.sleep(1)
        result = socket.recv().decode('utf-8')
        conversion_results[target_currency] = json.loads(result)

    socket.close()
    context.term()
    return conversion_results

def execute_receiver():
    file_path = "./receiver.py"
    try:
        subprocess.Popen(['python', file_path], shell=True)
    except:
        print("File not found")
        return

    # Wait a bit to ensure the receiver is ready
    time.sleep(2)

def main():
    execute_receiver()

    # Example conversion request
    results = convert_currency("USD", ["EUR", "CAD", "JPY"], 100)
    print("Conversion Results:", results)


if __name__ == "__main__":
    main()
