'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''

# Get the data from the input data and create the provider object + preparate data if necessary

#from Workers import Workers
from Provider import Provider

class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData

        #Requested Workers
        wr = self.inputData.wr

        #Providers
        nproviders = self.inputData.providers
        available_workers = self.inputData.available_workers
        cost_contract = self.inputData.cost_contract
        country = self.inputData.country
        cost_workers = self.inputData.cost_workers
        cost_1 = self.inputData.cost_1
        cost_2 = self.inputData.cost_2
        cost_3 = self.inputData.cost_3


		# ONCE THE INPUT DATA IS IMPORTED, WE GENERATE NEW DATA:

		# Create vector with Providers, with all the data of each provider
        self.providers = []
        for pId in xrange(0, nproviders):  # sId = 0..(nproviders-1)
            provider = Provider(pId, available_workers[pId], cost_contract[pId], country[pId], cost_workers[pId], cost_1, cost_2,cost_3)
            self.providers.append(provider)


    def getWorkers(self):
        return(self.wr)

    def getProviders(self):
        return(self.providers)
