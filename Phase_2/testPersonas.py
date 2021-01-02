import json

# We can view this phase as a simulation of a bank's database containing information about its employees
# and clients.

# Assume an employee X at least knows his Employee_ID and the company he works for
# Depending on the role of that employee (clerk, accountant, economist, etc), he will be granted a different
# set of available actions and access to different resources of the bank.
# Therefore, it's important to check the employee's info against the bank's database such that we know that
# the person is not lying.

# Clearly, an employee can be a customer as well, however, he would have a separate account if he wishes to perform
# actions on his personal account related to customers only

with open('personas_firms.json') as personas_firms:
    companies = json.loads(personas_firms.read())

with open('personas_individuals.json') as personas_individuals:
    individuals = json.loads(personas_individuals.read())

# Clearly, each role within a company should perform different actions and have access to different segments of the bank's DB
def valid_actions(role):
    switch = {
            "Economist" : 'I am a verified Economist and I shall perform Economist-like actions...',
            "Clerk" : 'I am a verified Clerk and I shall perform Clerk-like actions...',
            "Computer Engineer" : 'I am a verified Computer Engineer and I shall perform Computer Engineer-like actions...',
            "Data Analyst" : 'I am a verified Data Analyst and I shall perform Data Analyst-like actions...',
            "Customer" : 'I am a verified Customer and I shall perform Customer-like actions...'
             }
    return switch.get(role,"Invalid role")


# Let's test if the first individual in our json is indeed listed in either of the bank's database as an employee
# Clearly, we could have performed this test for all of the available individuals instead but with an increasing
# code readability complexity

individual1 = individuals['persons'][0]
credentialsFlag = False

for indexCompany in range(len(companies['organizations'])):

    print(individual1['employer'])
    print(companies['organizations'][indexCompany]['name'])
    print("---------------------")

    if (individual1['employer'] == companies['organizations'][indexCompany]['name']):

        # Imagine we are checking the badge of an employee/customer
        # So far we got a match for the name of the employer/customer's bank
        # Now, we still need to identify the employer's/customer's ID in the bank's database
        print("Got a match for the company")

        for indexPerson in range(len(companies['organizations'][indexCompany])):

            if (individual1['id'] == companies['organizations'][indexCompany]['employees'][indexPerson]['id']):

                credentialsFlag = True
                print (individual1['id'])
                print(companies['organizations'][indexCompany]['employees'][indexPerson]['id'])
                print("Got a match for the ID of the employee/Customer's ID")
                print("Credentials Accepted")

                # According to it's job
                actions = valid_actions(companies['organizations'][indexCompany]['employees'][indexPerson]['roles'][0])
                print(actions)

                print("--------------------------")

if(credentialsFlag == False):
    print("Credentials Refused")
    print("There was no match in the bank's database for the given Employee/Customer ID or Employer/Customer's Bank Name")


