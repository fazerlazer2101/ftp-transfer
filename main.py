from ftplib import FTP


#Menu
menu_options = {
    1: 'Transfer from source to destination',
    2: 'Change Source',
    3: 'Change Server',
    4: 'Change Credentials',
    5: 'Exit'
}

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
        
        

         
#Manage user option
if valid_response == 1:
    print("Start Transfer")
elif valid_response == 2:
    print("Change Source")
elif valid_response == 3:
    print("Change Server")
elif valid_response == 4:
    print("Change Credentials")
else:
    exit()
    


# #Awaits user input for password
# username = input("Username:")
# password = input("Password:")
# #User Login
# FTP.login(user,password)



# #Connect to FTP server
# ftp = FTP.connect(
#     #FTP server Addresss
# )