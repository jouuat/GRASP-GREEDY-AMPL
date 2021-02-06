'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''

import copy, time
from Problem import Problem
import decimal



# Assignment class stores the cost when a provider is assigned
class Assignment(object):
    def __init__(self, providerId):
        self.providerId = providerId



# Build the solution
class Solution(Problem):

    @staticmethod
    def createEmptySolution(config, problem):
        solution = Solution(problem.inputData)
        solution.setVerbose(config.verbose)
        return(solution)

    def __init__(self, inputData):
        super(Solution, self).__init__(inputData)
        self.cost = 0
        self.wr=self.inputData.wr
        self.w = {}
        self.ex = {}
        self.h= {}
        self.a = {}
        self.w5 = {}
        self.w10 = {}
        self.feasible = True
        self.verbose = True


    def setVerbose(self, verbose):
        if(not isinstance(verbose, (bool)) or (verbose not in [True, False])):
            raise Exception('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose

    def makeInfeasible(self):
        self.feasible = False
        self.cost = float('infinity')
        self.wr=self.inputData.wr
        self.w = {}
        self.ex = {}
        self.h= {}
        self.a = {}
        self.w5 = {}
        self.w10 = {}

    def isFeasible(self):
        return(self.feasible)


#--------------------------------provider yes or not--------------------------------

    def findFeasibleProviderAssignments(self, problem, new_solution):
        startEvalTime = time.time()
        evaluatedCandidates = 0
        feasibleProviderAssignments = []
        for provider in self.providers:
            providerId = provider.getId()
            feasible = self.assign_provider(providerId, problem, new_solution)

            evaluatedCandidates += 1
            if(not feasible): continue

            assignment = Assignment(providerId)
            #print('already assigned.' )

            feasibleProviderAssignments.append(assignment)

        elapsedEvalTime = time.time() - startEvalTime
        return(feasibleProviderAssignments, elapsedEvalTime, evaluatedCandidates)


    def assign_provider(self, providerId, problem, new_solution):
        if(not self.isFeasibleToAssignProvider(providerId, problem, new_solution)):
            if(self.verbose):
                print('Unable to contract Provider(%s)' % (str(providerId)))
            return(False)
        return True

#--------------------------constraints for a provider--------------------------------

    #nomes s'utilitza per trobar candidats a la primera vegada
    def isFeasibleToAssignProvider(self, providerId,  problem, new_solution):
        # contraint 1: at leat the half of the available_workers from a provider
        #should be less than wr

        #no necessitem fer el for per cada provider perque ja s'ha fet abans
        availbleworkers = int(self.providers[providerId].getAvailableWorkers())
        if(availbleworkers/2 >= new_solution.wr):
            #print('we need less workers than the provided by(%s).' % (str(providerId)))
            if(self.verbose):
                print('we need less workers than the provided by(%s).' % (str(providerId)))
            return(False)



        #constraint 2: if in the solution already exist a provider form the
        #country, this one can not be assigned
        for x in xrange(0, len(self.providers)):
            if((new_solution.a[x]>=1) or (new_solution.h[x]>=1)):
                if(self.providers[providerId].getCountry() == self.providers[x].getCountry()):
                    #print('there is already a provider from this country(%s) i long. %s' % (str(providerId),str(x)))
                    if(self.verbose):
                        print('there is already a provider from this country(%s).' % (str(providerId)))
                    return(False)


        #otherewise return true
        #print('the provider %s can be assigned.' % (str(providerId)))
        return(True)


#---------------------------get the cost of a provider----------------------------


    def getCost_provider(self, providerId, problem, new_solution, ProvidersWithoutNone):
        availbleworkers = int(self.providers[providerId].getAvailableWorkers())
        costworkers = int(self.providers[providerId].getCostWorkers())
        costcontract = int(self.providers[providerId].getCostContract())
        costsperworker = []
        nworkers = []
        cost1 = int(self.providers[providerId].getCost1())
        cost2 = int(self.providers[providerId].getCost2())
        cost3 = int(self.providers[providerId].getCost3())
        if(availbleworkers>new_solution.wr):
            #print('computing the cost of provider %s.( %s > %s)' % (str(providerId),str(availbleworkers),str(new_solution.wr)))
            if(availbleworkers/2<5):
                cost = costcontract + (availbleworkers/2*cost1)+availbleworkers/2*costworkers
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
            if(availbleworkers/2<11 and availbleworkers/2>5):
                cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1))+availbleworkers/2*costworkers
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
            if(availbleworkers/2>10):
                cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1)+ (availbleworkers/2-10)*(cost3-cost2))+availbleworkers/2*costworkers
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
                #print(' (%s) / (%s) / (%s) / (%s) / (%s) / (%s) / (%s)  ' % (str(providerId), str(costcontract),str(availbleworkers),str(cost1),str(cost2),str(cost3),str(costworkers)))
            #si els treballadors d'un/ mes els extra son iguals que el wr donar-li preferencia
            #per assegurar-nos que tenim una solucio feasible
            if(availbleworkers/2<5 and availbleworkers/2==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                cost = costcontract + (availbleworkers/2*cost1)+availbleworkers/2*costworkers-1000000
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
            if(availbleworkers/2<11 and availbleworkers/2>5 and availbleworkers/2==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1))+availbleworkers/2*costworkers-1000000
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
            if(availbleworkers/2>10 and availbleworkers/2==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1)+ (availbleworkers/2-10)*(cost3-cost2))+availbleworkers/2*costworkers-1000000
                workers = availbleworkers/2
                nworkers.append(workers)
                costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                costsperworker.append(costperworker)
        if(availbleworkers<=new_solution.wr):
            #print('computing the cost of provider %s.( %s <= %s)' % (str(providerId),str(availbleworkers),str(new_solution.wr)))
            for extra in range(availbleworkers):
                if(availbleworkers+extra<=new_solution.wr):
                    if(availbleworkers/2<5):
                        cost = costcontract + (availbleworkers/2*cost1)+availbleworkers/2*costworkers
                        workers = availbleworkers/2
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers/2<11 and availbleworkers/2>5):
                        cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1))+availbleworkers/2*costworkers
                        workers = availbleworkers/2
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers/2>10):
                        cost = costcontract + (availbleworkers/2*cost1 + (availbleworkers/2-5)*(cost2-cost1)+ (availbleworkers/2-10)*(cost3-cost2))+availbleworkers/2*costworkers
                        workers = availbleworkers/2
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers+extra<5):
                        cost = costcontract + ((availbleworkers+extra)*cost1)+ (availbleworkers+extra)*costworkers
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers+extra<11 and availbleworkers+extra>5):
                        cost = costcontract + ((availbleworkers+extra)*cost1 + (availbleworkers+extra-5)*(cost2-cost1))+(availbleworkers+extra)*costworkers
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers+extra>10):
                        cost = costcontract + ((availbleworkers+extra)*cost1 + (availbleworkers+extra-5)*(cost2-cost1) + (availbleworkers+extra-10)*(cost3-cost2))+(availbleworkers+extra)*costworkers
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    #si els treballadors d'un/ mes els extra son iguals que el wr donar-li preferencia
                    #per assegurar-nos que tenim una solucio feasible
                    if(availbleworkers+extra<5 and availbleworkers+extra==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                        cost = costcontract + ((availbleworkers+extra)*cost1)+(availbleworkers+extra)*costworkers-1000000
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers+extra<11 and availbleworkers+extra>5 and availbleworkers+extra==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                        cost = costcontract + ((availbleworkers+extra)*cost1 + (availbleworkers+extra-5)*(cost2-cost1))+(availbleworkers+extra)*costworkers-1000000
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
                    if(availbleworkers+extra>10 and availbleworkers+extra==new_solution.wr and (decimal.Decimal(len(ProvidersWithoutNone))/decimal.Decimal(len(self.providers))<0.7)):
                        cost = costcontract + ((availbleworkers+extra)*cost1 + (availbleworkers+extra-5)*(cost2-cost1) + (availbleworkers+extra-10)*(cost3-cost2))+(availbleworkers+extra)*costworkers-1000000
                        workers = availbleworkers+extra
                        nworkers.append(workers)
                        costperworker=float(decimal.Decimal(cost) / decimal.Decimal(workers))
                        costsperworker.append(costperworker)
        #print('actualized in solution %s + %s of provider %s. with cost: %s costperworker: %s' % (str(availbleworkers), str(extra), str(providerId),str(cost),str(costperworker)))
        return(costsperworker,nworkers, availbleworkers)


#----------------------------obtain the cost of a given provider -------------------

    def getCostGivenProvider(self, providerId, problem, localsolution):
        costworkers = int(self.providers[providerId].getCostWorkers())
        costcontract = int(self.providers[providerId].getCostContract())
        cost1 = int(self.providers[providerId].getCost1())
        cost2 = int(self.providers[providerId].getCost2())
        cost3 = int(self.providers[providerId].getCost3())
        workers = localsolution.w[providerId]
        workers5 = localsolution.w5[providerId]
        workers10 = localsolution.w10[providerId]
        cost = costcontract + workers*costworkers + cost1*workers + (cost2-cost1)*workers5 + (cost3-cost2)*workers10
        return(cost)



#-----------------------------save the solution---------------------------------------

    def str(self, wr, w, h, a, w5, w10, ex):

        # Objective function
        strSolution = 'Cost = %s;\n' % self.cost

        #the remaining wr workers to be hired
        strSolution += 'wr = %s;\n' % str(wr)

        # workers for provider
        strSolution += 'w = [ '
        for z in w:
            strSolution += str(z) + ' '
        strSolution += '];\n'

        # extra workers
        strSolution += 'ex = [ '
        for b in ex:
            strSolution += str(b) + ' '
        strSolution += '];\n'

        # whether the half workers are choosen
        strSolution += ' h= [ '
        for c in h:
            strSolution += str(c) + ' '
        strSolution += '];\n'

        # whether if an workers are choosen
        strSolution += 'a = [ '
        for d in a:
            strSolution += str(d) + ' '
        strSolution += '];\n'

        # plus workers than 5
        strSolution += 'w5 = [ '
        for e in w5:
            strSolution += str(e) + ' '
        strSolution += '];\n'

        # plus workers than 10
        strSolution += 'w10 = [ '
        for f in w10:
            strSolution += str(f) + ' '
        strSolution += '];\n'

        return(strSolution)



    def saveToFile(self, filePath, wr, w, h, a, w5, w10, ex):
        f = open(filePath, 'w')
        f.write(self.str( wr, w, h, a, w5, w10, ex))
        f.close()
