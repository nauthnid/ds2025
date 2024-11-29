import socket
import os

def connect_to_server():
    SERVER_IP = input("Enter IP address of server: ") 
    PORT = int(input("Enter port of server: "))  

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORT))
        print(f"Connected to server at {SERVER_IP}:{PORT}")

        while True:
            print("\nOptions:")
            print("1. Upload a file")
            print("2. Download a file")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                client_socket.send(b"UPLOAD")
                upload_file(client_socket)
            elif choice == "2":
                client_socket.send(b"DOWNLOAD")
                download_file(client_socket)
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")
        
        client_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def upload_file(client_socket):
    filename = input("Enter full filename to upload: ")
    if os.path.isfile(filename):
        client_socket.send(filename.encode())  # send file name to server
        with open(filename, 'rb') as f:
            while chunk := f.read(1024):
                client_socket.send(chunk)  # send file data in blocks
        print(f"File '{filename}' uploaded successfully.")
    else:
        print("File not found. Please try again.")

def download_file(client_socket):
    filename = input("Enter full filename to download: ")
    client_socket.send(filename.encode())  # request filename from server

    response = client_socket.recv(1024).decode()
    if response == "OK":
        # To avoid overwriting, append a suffix to the downloaded file
        downloaded_filename = f"downloaded_{filename}"
        with open(downloaded_filename, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)  # save file received from server
        print(f"File '{filename}' downloaded successfully as '{downloaded_filename}'.")
    else:
        print(f"Error: {response}")

if __name__ == "__main__":
    connect_to_server()
