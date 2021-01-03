# large Scale Computing project

### Installing
For this project Python 3.8 was used. The project is divided into 3 steps: 
## Step 1:  a secure messaging functionality is implemented
  1. go to folder Step 1 > run main.py > run client.py 
  2. you need to run client.py while main.py is running. you can run client.py multiple times depending on how many clients you want. 
  3. Each client models one participant in the communication network.  A client is started using a configuration file in JSON-format from the data folder
  
## Step 2:  Roles and Communication Relations
  1. Cloud instances that incorporate several Personas using a configuration file in JSON-format is set up.
  2. go to folder Step 2 > run testPersonas.py > you can view this phase as a simulation of a bank's database containing information about its employees and clients
## Step 3: a Banking Scenario is implemented.
  1. go to folder Step 3 > run bank_server.py > run bank_client.py 
  2. you need to run bank_client.py while bank_server.py is running.
  3. Class bank_bank.py which you need to run either before or after bank_client.py. Also, bank_bank.py is a class representing the bank that gets client's commands    from the main server
  4. the data for this step is in the corresponding data folder


## Authors

<li>Wafaa Aljbawi</li>
<li>Paula Gitu</li>
<li>Iga Skorupska</li>
<li>Mihai Tudor</li>
<li>Mateusz Wiza</li>

