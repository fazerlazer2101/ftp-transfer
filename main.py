from ftplib import FTP

#Menu
menu_options = {
    1: 'Connect',
    2: 'Change Source',
    3: 'Change Server',
    4: 'Change Credentials',
    5: 'Exit'
}

#ftp menu
ftp_options = {
    1: 'Transfer Files',
    2: 'Create Directory',
    3: 'List Current Directory',
    4: 'Change Directory',
    5: 'Exit'
}

#ftp instance
ftp = FTP()

def ftp_response_menu():
    for key in ftp_options.keys():
        print (key, '--', ftp_options[key] )
    validation()


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

#Prints a menu
def user_response_menu():
    
    print ("Welcome to the FTP transfer Tool Please select an option.")
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
    validation()
 
user_response_menu()

def create_directory():
    folder_name = input("Name of Directory:")
    ftp.mkd(folder_name)


control = True
def ftp_control():
    
    if True:
            #FTP menu
            ftp_response_menu()

            #respond to inputs
            if valid_response == 1:
                print("Transfer Files")
                ftp_control()
            elif valid_response == 2:
                print("Create Directory")
                create_directory()
                ftp_control()
            elif valid_response == 3:
                print("List Current Directory")
                print(ftp.pwd())
                ftp_control()
            elif valid_response == 4:
                print("Change Directory")
                ftp_control()
            else:
               global control
               control = False



#Manage user option
if valid_response == 1:
    print("Start Transfer")
    ftp.connect(host="10.0.0.16",port=2121)
    ftp.login(user="deck", passwd="1506")
    #Starts connection
    #Connect to FTP server
    ftp_control()
    
elif valid_response == 2:
    print("Change Source")
elif valid_response == 3:
    print("Change Server")
elif valid_response == 4:
    print("Change Credentials")
else:
    exit()