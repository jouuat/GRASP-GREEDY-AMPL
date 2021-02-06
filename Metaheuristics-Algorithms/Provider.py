'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''

#Constuct the object provider + give methods to query the data inside of it

class Provider(object):
    def __init__(self, pId, available_workers, cost_contract, country, cost_workers, cost_1, cost_2, cost_3):

        self._pId = pId
        self._available_workers = available_workers
        self._cost_contract = cost_contract
        self._country = country
        self._cost_workers = cost_workers
        self._cost_1 = cost_1
        self._cost_2 = cost_2
        self._cost_3 = cost_3

    def getId(self):
        return(self._pId)

    def getAvailableWorkers(self):
        return(self._available_workers)

    def getCostContract(self):
        return(self._cost_contract)

    def getCountry(self):
        return(self._country)

    def getCostWorkers(self):
        return(self._cost_workers)

    def getCost1(self):
        return(self._cost_1)

    def getCost2(self):
        return(self._cost_2)

    def getCost3(self):
        return(self._cost_3)
