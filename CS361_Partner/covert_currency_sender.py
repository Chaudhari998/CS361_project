import zmq
import time
import subprocess


def execute_receiver():
    file_path = "convert_currency_receiver.py"
    try:
        subprocess.Popen(['python', file_path], shell=True)
    except:
        print("File not found")
        return

    connect_socket()


def connect_socket():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to CS361 pipeline…\n")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    send_message(socket)


def send_message(socket):
    #  Sends a message
    print(f"==Sending message…\n")
    message = "{USD, EUR, 10000}"
    socket.send_string(message)

    #  Get the reply.
    time.sleep(1)
    result = socket.recv()
    print(f"==Result: " + str(result) + "\n")

    end_receiver(socket)


def end_receiver(socket):
    # Sends message to end
    time.sleep(1)
    print(f"==Sending message… \n")
    message = "END"
    socket.send_string(message)

    # Receives confirmation it successfully ended
    time.sleep(1)
    result = socket.recv()
    print(f"==Result: " + str(result) + "\n")


def main():
    execute_receiver()
    return


if __name__ == "__main__":
    main()
