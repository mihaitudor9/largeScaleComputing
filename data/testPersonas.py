import json

with open('personas_firms.json') as personas_firms:
    companies = json.loads(personas_firms.read())


with open('personas_individuals.json') as personas_individuals:
    individuals = json.loads(personas_individuals.read())

# Let's test if individual1 is indeed listen in either of the bank's database as an employee
individual1 = individuals['persons'][0]

for indexCompany in range (0,3):

    print(individual1['employer'])
    print(companies['organizations'][indexCompany]['name'])
    print("---------------------")

    if (individual1['employer'] == companies['organizations'][indexCompany]['name']):

        # Imagine we are checking the badge of an employee
        # So far we got a match for the name of the employer
        # Now, we still to identify the employer's id against the bank's database
        print("Got a match for the company")

        # We have to iterate over all the employees in the bank's DB
        # Don't seem to get len(obj) working rn

        for indexPerson in range(0,3):
            if (individual1['id'] == companies['organizations'][indexCompany]['employees'][indexPerson]['id']):

                print (individual1['id'])
                print(companies['organizations'][indexCompany]['employees'][indexPerson]['id'])
                print("Got a match for the ID of the employee's ID")
                print("Credentials Accepted")
                print("--------------------------")