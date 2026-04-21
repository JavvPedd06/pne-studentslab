import http.client
import json
import termcolor

PORT = 8080
SERVER = 'localhost'

print(f"\nConnecting to server: {SERVER}:{PORT}\n")

conn = http.client.HTTPConnection(SERVER, PORT)

try:
    conn.request("GET", "/listusers")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

r1 = conn.getresponse()
print(f"Response received!: {r1.status} {r1.reason}\n")

data1 = r1.read().decode("utf-8")


people = json.loads(data1)

print("CONTENT: ")

termcolor.cprint(f"Total people in database: {len(people)}", 'yellow', attrs=['bold'])
print("-" * 30)


for person in people:
    print()
    termcolor.cprint("Name: ", 'green', end="")
    print(person['Firstname'], person['Lastname'])

    termcolor.cprint("Age: ", 'green', end="")
    print(person['age'])


    phoneNumbers = person['phoneNumber']

    termcolor.cprint("Phone numbers: ", 'green', end='')
    print(len(phoneNumbers))


    for i, phone_val in enumerate(phoneNumbers):

        termcolor.cprint(f"  Phone {i + 1}: ", 'blue', end="")
        print(phone_val)

    print("-" * 20)

conn.close()
