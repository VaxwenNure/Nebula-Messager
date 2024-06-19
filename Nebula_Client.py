import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import pygame

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




HOST = "127.0.0.1"
PORT = 1234

DARK_GREY = '#2D3250'
MEDIUM_GREY = '#424769'
OCEAN_BLUE = '#F6B17A'
WHITE = 'white'
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)
BUTTON_FONT = ("Helvetica", 13)

pygame.mixer.init()
send_sound = pygame.mixer.Sound("send.mp3")


def update_message(message):
    message_Box.config(state=tk.NORMAL)
    message_Box.insert(tk.END, message + '\n')
    message_Box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        update_message("[SERVER] Successfully connected to server")
    except:
        messagebox.showerror("Problem with connection!", f"Unable to connect to the server {HOST} {PORT}")
        exit(0)

    username = username_TextBox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username input!", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    username_Label.config(text="Your username:")
    username_TextBox.config(state=tk.DISABLED)
    username_LogIn_Button.config(state=tk.DISABLED)

def disconnect():
    try:
        client.sendall("/quit".encode())
        client.close()
        root.quit()
    except:
        messagebox.showerror("Disconnection error", "Failed to disconnect properly")

def send_message():
    message = message_TextBox.get()
    if message != '':
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client.sendall(f"{timestamp}~{message}".encode())
        message_TextBox.delete(0, len(message))
        send_sound.play()
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("680x670")
root.title("Nebula Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_Label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_Label.pack(side=tk.LEFT, padx=10)

username_TextBox = tk.Entry(top_frame, font=FONT, bg=DARK_GREY, fg=WHITE, width=22)
username_TextBox.pack(side=tk.LEFT)

username_LogIn_Button = tk.Button(top_frame, text='Join', font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_LogIn_Button.pack(side=tk.LEFT, padx=15)

username_LogOut_Button = tk.Button(top_frame, text='Disconnect', font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=disconnect)
username_LogOut_Button.pack(side=tk.LEFT, padx=15)

message_TextBox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=40)
message_TextBox.pack(side=tk.LEFT, padx=25)

send_message_Button = tk.Button(bottom_frame, text='Send', font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
send_message_Button.pack(side=tk.LEFT)

message_Box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=27)
message_Box.config(state=tk.DISABLED)
message_Box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                timestamp, username, content = message.split('~')
                update_message(f"[{timestamp}] [{username}] {content}")
            else:
                messagebox.showerror("Error", "Message received from server is empty")
        except ConnectionAbortedError:
            print("Connection was aborted")
            break
        except:
            break

def main():
    root.mainloop()

if __name__ == "__main__":
    main()
