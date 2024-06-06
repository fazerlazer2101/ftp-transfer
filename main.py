from ftplib import FTP
import os

import tkinter
from tkinter import filedialog

import yaml

#Menu
menu_options = {
    1: 'Connect',
    2: 'Change Server',
    3: 'Change Credentials',
    4: 'Exit'
}



#ftp menu
ftp_options = {
    1: 'Transfer Files',
    2: 'Create Directory',
    3: 'List Current Directory',
    4: 'Change Directory',
    5: 'Current Directory',
    6: 'Exit'
}

#ftp instance
ftp = FTP()

# Method handles ftp menu responses.
def ftp_response_menu():
    for key in ftp_options.keys():
        print (key, '--', ftp_options[key] )
    validation()

# Method that Handles user input validation
valid_response = 5    
def validation():
    valid = True
    if valid:    
        #Check if input is an int or string
        try:
            global valid_response
            valid_response = int(input("Choose an option: "))
            valid = False
        #Throws an error if anything occurs and goes back to menu
        except Exception:
            validation()

# Method that prints options for the ftp client
def user_response_menu():
    
    print ("Welcome to the FTP transfer Tool Please select an option.")
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
        continue
    validation()
    #Manage user option
    if valid_response == 1:
        print("Start Transfer")
        try:
            #Read config
            with open('serverConfig.yaml', 'r') as server:
                data = yaml.safe_load(server)
                
            with open('userConfig.yaml', 'r') as user:
                user_data = yaml.safe_load(user)
            #Starts connection
            ftp.connect(host=f"{data["host"]}",port=int(data["port"]))
            ftp.login(user=f"{user_data["user"]}", passwd=f"{user_data["password"]}")
            
        except Exception:
            print("Failed to connect")
            user_response_menu()
        ftp_control()
    elif valid_response == 2:
        change_server_settings()
        
    elif valid_response == 3:
        change_user_settings()
    else:
        exit()
        

#Method to Create a directory
def create_directory():
    folder_name = input("Name of Directory: ")
    ftp.mkd(folder_name)

#Method to change directory in
def change_directory():
    path = input("Path: ")
    ftp.cwd(path)
    
# Method to change the connection / server settings.
def change_server_settings():
    new_host = input("Enter new server: ")
    #Validates port to be only a number.
    try:
        new_port = int(input("Enter new port: "))
    except Exception as e:
        change_user_settings()      
    data = {
        "host": f"{str(new_host)}",
        "port": int(new_port),
    }
    #Dumps into a yaml file
    with open('serverConfig.yaml', 'w') as file:
        yaml.dump(data, file)
    user_response_menu()
    
# Method that changes user configuration
def change_user_settings():
    new_username = input("Enter username: ")
    #Validates port to be only a number.
    new_password = input("Enter your password: ")
    data_user = {
        "user": f"{str(new_username)}",
        "password": f"{new_password}",
    }
    #Dumps into a yaml file
    with open('userConfig.yaml', 'w') as userfile:
        yaml.dump(data_user, userfile)
        
    user_response_menu()

# Method that checks if an item is a directory
def check_if_directory(path, item):
  item_path = os.path.join(path, item)
  if os.path.isfile(item_path):
      return True
  else:
      return False
    
# Method that handles uploading folders
def upload_folder(local_path, remote_path):
    #Parent folder name
    local_directory_name = os.path.basename(local_path)
    #Change to the remote directory
    print(remote_path)
    
    #Check if parent folder exists in remote
    try:
        ftp.cwd(local_directory_name)
    except Exception as e:
        print("No Folder found")
        ftp.mkd(local_directory_name)
        #Goes to parent folder
        ftp.cwd(local_directory_name)
    
    #List of files in local directory
    local_files = os.listdir(local_path)
    
    #Iterate over the local directory.
    for item in local_files:
        #Determine if item is a file or folder
        if check_if_directory(local_path, item):
            #Copy file
            print(f"Copied to {ftp.pwd()} {item}")
            try:
                file_name = str(item)
                folder_path = os.path.join(local_path, item)
                with open(folder_path, 'rb') as file:
                    ftp.storbinary(f"STOR {file_name}",file, 8192)
                    print("Transfer Complete")
            except Exception as e:
                print(e)
        else:
            #Make Directory
            print(f"{item}")
            #Fails means that directory exists
            try:
                ftp.mkd(f"{item}")
            except Exception as e:
                pass
            local_files = os.listdir(os.path.join(local_path, item))
            print(f"New path: {os.path.join(local_path, item)}")
            #Go into that directory
            upload_folder(os.path.join(local_path, item), os.path.join(local_path, item))
    ftp.cwd("..")
    ftp_control()   

# Method that handles individual file upload.
def upload_files():
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

    
    folder_path = ""
    
    #Ask if you are transfering a file or folder
    file_options = {
        1: "Transfer a file?",
        2: "Transfer a folder?",
        3: "Exit"
    }
    
    for key in file_options.keys():
        print (key, '--', file_options[key] )
    validation()
    
    
    
    if valid_response == 1:
        folder_path = filedialog.askopenfilename()
    elif valid_response == 2:
        folder_path = filedialog.askdirectory()
    else:
        ftp_control()
    
    #Recursivly check start transfer of a folder
    
    #First check if path recieved is a folder or a file
    if os.path.isdir(str(folder_path)):
        upload_folder(folder_path, ftp.pwd())
    else:
        try:
            file_name = os.path.basename(str(folder_path))
            with open(folder_path, 'rb') as file:
                ftp.storbinary(f"STOR {file_name}",file, 8192)
                print("Transfer Complete")
        except Exception as e:
            print(e)
            
# Method that handles the ftp control responses.
def ftp_control():
    if True:
            #FTP menu
            ftp_response_menu()

            #respond to inputs
            if valid_response == 1:
                print("Transfer files to the directory " +ftp.pwd())
                confirmation = input("Continue? Y/n ")
                if(confirmation.__eq__("Y")):
                    upload_files()
                else:
                    ftp_control()
            elif valid_response == 2:
                print("Create Directory")
                create_directory()
                ftp_control()
            elif valid_response == 3:
                currentfiles = ftp.nlst()
                for item in currentfiles:
                    print(item)
                ftp_control()
            elif valid_response == 4:
                change_directory()
                ftp_control()
            elif valid_response== 5:
                print(ftp.pwd())
                ftp_control()
            else:
                exit()

#Start of application
user_response_menu()