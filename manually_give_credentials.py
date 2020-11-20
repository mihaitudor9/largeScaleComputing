import json
import keyboard

credentialsIndex = 0

print("Press C to add additional credentials\n")
user = {}

while True:

    try:
        if keyboard.is_pressed('c'):
            name = input("\nName: ")
            ID = input("\nID: ")
            user = {'index': credentialsIndex, 'user_name': name, 'user_ID': ID}

            with open('data/credentials.json', 'w') as outfile:
                outfile.write(
                    '[' +
                    '\n' + json.dumps(user) +
                    ']\n')

            credentialsIndex = credentialsIndex + 1

            print("Press C to add additional credentials\n")

    except:
        break
