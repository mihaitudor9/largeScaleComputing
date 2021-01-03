import json
import keyboard

# a class that manually gives a client's credentials
credentialsIndex = 0

print("Press C to add additional credentials\n")
user = {}

while True:

    try:
        if keyboard.is_pressed('c'):
            # input the name and id and add them to the array
            name = input("\nName: ")
            ID = input("\nID: ")
            user = {'index': credentialsIndex, 'user_name': name, 'user_ID': ID}

            # save user's credentials in the log file
            with open('data/credentials.json', 'w') as outfile:
                outfile.write(
                    '[' +
                    '\n' + json.dumps(user) +
                    ']\n')

            # increase the index
            credentialsIndex = credentialsIndex + 1

            print("Press C to add additional credentials\n")

    except:
        break
