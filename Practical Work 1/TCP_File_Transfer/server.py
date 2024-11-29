import socket
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999    

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Accept max 5 devices
    print(f"Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        operation = conn.recv(1024).decode()
        if operation == "UPLOAD":
            handle_upload(conn) 
        elif operation == "DOWNLOAD":
            handle_download(conn) 
        else:
            conn.send(b"ERROR: Invalid operation")  
        
        conn.close()  # Ensure connection is closed after each operation

def handle_upload(conn):
    filename = conn.recv(1024).decode()  # Get filename from client
    print(f"Receiving file: {filename}")

    # Check if file already exists and create a new name if necessary
    if os.path.isfile(filename):
        # If the file exists, create a new name by appending a number
        base_name, ext = os.path.splitext(filename)
        counter = 1
        new_filename = f"{base_name}_{counter}{ext}"
        while os.path.isfile(new_filename):  # Check if the new name already exists
            counter += 1
            new_filename = f"{base_name}_{counter}{ext}"
        filename = new_filename
        print(f"File already exists. Renaming to {filename}")

    # Write the received file data directly to the new file
    with open(filename, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # If no more data, stop writing
            f.write(data)  # Write data to file
    print(f"File '{filename}' received and saved.")

def handle_download(conn):
    filename = conn.recv(1024).decode()  # Get filename from client
    print(f"Client requested file: {filename}")

    if os.path.isfile(filename):  # Check if file exists
        conn.send(b"OK")  
        with open(filename, 'rb') as f:
            while chunk := f.read(1024):  # Read file in chunks
                conn.send(chunk)
        print(f"File '{filename}' sent successfully.")
    else:
        conn.send(b"ERROR: File not found")  # Error if file doesn't exist
        print(f"File '{filename}' not found")

if __name__ == "__main__":
    start_server()
