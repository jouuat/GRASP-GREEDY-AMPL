'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''


import copy, time
from Solution import Solution
from Solver import Solver

class LocalSearch(object):
    def __init__(self, config):
        self.enabled = config.localSearch
        self.elapsedTime = 0
        self.iterations = 0


    #Given a solution S
    #foreach provider in solution
    #   remove that provider from the solution
    #   while len(Providers)>0 and wr>0)
    #       foreach provider in Candidates
    #       if provider from candidates != provider removed from the solution
    #             fer tots els passos del Greedy(calcularcost/assignar/recalcular els candidats)
    #    if (cost<sol)
    #        canviar SOLUCIO S = S'
    # if (cost<sol or wr!=0)
    #    no canviar solucio  return S
    

    #Decide which strategy use Best-improving or First-improving

    #comencar a iterar amb algun provider que no estigui agafat per la solucio
    #a partir d'aquest escollir candidats com de normal

    #---------------------------- run startup for the local search ------------------------------------

    def run(self, greedy_solution, problem, config, iteration):
        bestSolution = greedy_solution
        bestCost = greedy_solution.cost

        startEvalTime = time.time()

        #-----------------Inicialitzar les decision variables-----------------------------------------
        candidateNeighbor = Solution.createEmptySolution(config, problem)

        candidateNeighbor.w = [0 for x in range(problem.inputData.providers)]         #Normal workers provided by a provider
        candidateNeighbor.ex = [0 for x in range(problem.inputData.providers)]        #extra workers provided by a provider
        candidateNeighbor.h= [0 for x in range(problem.inputData.providers)] 			#whether are picked the half of the available_workers or not
        candidateNeighbor.a = [0 for x in range(problem.inputData.providers)] 		#whether are picked the total of the available_workers of a provider or not
        candidateNeighbor.w5 = [0 for x in range(problem.inputData.providers)] 		#whether thre are hired more than 5 workers
        candidateNeighbor.w10 = [0 for x in range(problem.inputData.providers)]       #whether there are hired more than 10 workers or not

        # Keep track of the elapsed time and evaluated candidates
        elapsedEvalTime = 0
        evaluatedCandidates = 0

        #------------------- crear la candidate list -----------------------------------------------
        #newcandidates = []
        newcandidates, provider_elapsedEvalTime, provider_evaluatedCandidates = candidateNeighbor.findFeasibleProviderAssignments(problem, candidateNeighbor)
        #candidatesProvider.append(feasibleProviderAssignments)
        elapsedEvalTime += provider_elapsedEvalTime
        evaluatedCandidates += provider_evaluatedCandidates


        # iterar mentres keep iterating es true i el elapsedTime is menor que el maxExecTime
        keepIterating = True
        startEvalTime = time.time()
        elapsedTime = 0
        iterations = 0
        #print('--------------Begins the Local Search------------')
        while(keepIterating and elapsedTime < config.maxExecTime):
            keepIterating = False
            iterations += 1
            neighbor_solution, newcandidates = self.exploreNeighborhood(bestSolution, problem, config, candidateNeighbor, newcandidates)
            if(bestCost > neighbor_solution.cost):
                #print('ive beeen hereeeee')
                bestSolution = copy.deepcopy(neighbor_solution)
                bestCost = bestSolution.cost
                keepIterating = True
            iteration += 1
            elapsedTime = time.time() - startEvalTime
            #print('ive beeen hereeeee')

        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime

        return(bestSolution, iteration)

    #nota mental a tenir en compte, ara la solucio no semmagatzemara a la greedy_solution sino
    #que semmagatzemara al candidateNeighbor, i ara no tindrem feasibleProviderAssignments sino
    # que tindrem newcandidates
    #-------------------------------- explore the neighboorhood defined ----------------------------------------

    def exploreNeighborhood(self, bestSolution, problem, config, candidateNeighbor, allcandidates):
        providers = bestSolution.getProviders()
        #AGAFEM EL PRIMER CANDIDAT DIFERENT

        #copiar la solucio al candidatesNeighbor
        candidateNeighbor.w = list(bestSolution.w)
        candidateNeighbor.ex = list(bestSolution.ex)
        candidateNeighbor.h= list(bestSolution.h)
        candidateNeighbor.a = list(bestSolution.a)
        candidateNeighbor.w5 = list(bestSolution.w5)
        candidateNeighbor.w10 =list(bestSolution.w10)
        candidateNeighbor.cost = copy.deepcopy(bestSolution.cost)
        candidateNeighbor.wr = copy.deepcopy(bestSolution.wr)


        #TODOOOO aconseguir eliminar candidats none type i
        #aconseguir que agafi tambe els valors de dles que primers estan assignats coma  possibles candidags

        for x in xrange(0, len(candidateNeighbor.w)):
            curCost = bestSolution.cost


            '''#copiar la solucio al candidatesNeighbor
            #si em trobat una solucio millor es modificara, sino no
            candidateNeighbor.w = list(bestSolution.w)
            candidateNeighbor.ex = list(bestSolution.ex)
            candidateNeighbor.h= list(bestSolution.h)
            candidateNeighbor.a = list(bestSolution.a)
            candidateNeighbor.w5 = list(bestSolution.w5)
            candidateNeighbor.w10 =list(bestSolution.w10)
            candidateNeighbor.cost = copy.deepcopy(bestSolution.cost)
            candidateNeighbor.wr = copy.deepcopy(bestSolution.wr)'''

            #print('candidateNeighbor.w %s'%(candidateNeighbor.w))
            #print('candidateNeighbor.h %s'%(candidateNeighbor.h))
            #print('candidateNeighbor.a %s'%(candidateNeighbor.a))
            #print('bestSolution.w %s'%(bestSolution.w))

            if((candidateNeighbor.a[x]>=1) or (candidateNeighbor.h[x]>=1)):
                cost = candidateNeighbor.getCostGivenProvider(x, problem, candidateNeighbor)
                candidateNeighbor.cost -= cost
                candidateNeighbor.wr += candidateNeighbor.w[x]
                candidateNeighbor.w[x] = 0
                candidateNeighbor.ex[x] = 0
                candidateNeighbor.h[x]= 0
                candidateNeighbor.a[x] = 0
                candidateNeighbor.w5[x] = 0
                candidateNeighbor.w10[x] = 0
                #print('candidateNeighbor %s,candidateNeighbor.wr %s, candidateNeighbor.cost %s, candidateNeighborId %s' %(candidateNeighbor.w,candidateNeighbor.wr,candidateNeighbor.cost,x))
                #print('-------------------------------------------')

                #print('REMAINING wr(%s) COST(%s)'%(candidateNeighbor.wr,candidateNeighbor.cost))
                newcandidates = copy.deepcopy(allcandidates)
                ProvidersWithoutNone = [candidate for candidate in newcandidates if  candidate.providerId != None]
                while(len(ProvidersWithoutNone)>0 and candidateNeighbor.wr>0):
                    minCostperworker = float('infinity')
                    choosenProviderId = None

                    newcandidates = copy.deepcopy(allcandidates)
                    minCostperworker = float('infinity')
                    for candidate in newcandidates:
                        #print('candidatesevaluated %s'%(candidate.providerId))
                        if(candidate.providerId != None):
                            if(not candidateNeighbor.isFeasibleToAssignProvider(candidate.providerId, problem, candidateNeighbor)):
                                candidate.providerId = None

                    ProvidersWithoutNone = [candidate for candidate in newcandidates if candidate.providerId != None]
                    #print('quants candidats ens queden %s' %(len(ProvidersWithoutNone)))
                    #TODO: arreglar que s'eliminin els candidats amb id none
                    #for candidate in newcandidates:
                        #if(candidate.providerId == None):
                            #newcandidates.pop(0)

                    for candidate in newcandidates:
                        #print('quins candidats volten per aqui(%s)'%candidate.providerId)
                        if(candidate.providerId != None and candidate.providerId != x):
                            #print('quins evaluem realment(%s)'%candidate.providerId)
                            newcostsperworker, newnWorkers, newavailbleworkers = candidateNeighbor.getCost_provider(candidate.providerId, problem, bestSolution, ProvidersWithoutNone)
                            for x in xrange(0,len(newcostsperworker)):
                                if (newcostsperworker[x] < minCostperworker):
                                    minCostperworker=newcostsperworker[x]
                                    nWorkers = newnWorkers[x]
                                    availbleworkers =  newavailbleworkers
                                    #print('minCostperworker acutalized in solver %s.' % (str(minCostperworker)))
                                    choosenProviderId = candidate.providerId

                    if(choosenProviderId is None):
                        break
                    # Assignar el provider obtingut
                    candidateNeighbor.assign_provider(choosenProviderId, problem, candidateNeighbor )
                    #print('candidate selected(%s)'%(choosenProviderId))
                    # ficar els valors a la solucio
                    if (minCostperworker <= 0):
                        minCost=minCostperworker*nWorkers+1000000
                    if (minCostperworker > 0):
                        minCost=minCostperworker*nWorkers
                    candidateNeighbor.cost += round(minCost)
                    candidateNeighbor.wr = candidateNeighbor.wr - nWorkers
                    #print('REMAINING wr(%s) COST(%s)'%(candidateNeighbor.wr,candidateNeighbor.cost))
                    candidateNeighbor.w[choosenProviderId] = nWorkers
                    if(nWorkers < availbleworkers):
                        candidateNeighbor.h[choosenProviderId] = 1
                        candidateNeighbor.a[choosenProviderId] = 0
                        candidateNeighbor.ex[choosenProviderId] = 0
                        candidateNeighbor.w5[choosenProviderId] = 0
                        candidateNeighbor.w10[choosenProviderId] = 0
                    if((nWorkers<11) and (nWorkers>5)):
                        candidateNeighbor.w5[choosenProviderId] = nWorkers-5
                        candidateNeighbor.w10[choosenProviderId] = 0
                        if(nWorkers>10):
                            candidateNeighbor.w5[choosenProviderId] = nWorkers-5
                            candidateNeighbor.w10[choosenProviderId] = nWorkers-10
                    if(nWorkers >= availbleworkers):
                        candidateNeighbor.h[choosenProviderId] = 0
                        candidateNeighbor.a[choosenProviderId] = 1
                        candidateNeighbor.ex[choosenProviderId] = 0
                        candidateNeighbor.w5[choosenProviderId] = 0
                        candidateNeighbor.w10[choosenProviderId] = 0
                        if((nWorkers<11) and (nWorkers>5)):
                            candidateNeighbor.w5[choosenProviderId] = nWorkers-5
                            candidateNeighbor.w10[choosenProviderId] = 0
                        if(nWorkers>10):
                            candidateNeighbor.w5[choosenProviderId] = nWorkers-5
                            candidateNeighbor.w10[choosenProviderId] = nWorkers-10
                        if(nWorkers > availbleworkers):
                            candidateNeighbor.ex[choosenProviderId] = nWorkers-availbleworkers
                    #si per cada canvi el cost que obtenim es millor assignar el nou cost
                    #per a cada for comprovar si es menor o no
                    if(candidateNeighbor.cost < curCost and candidateNeighbor.wr==0):
                        bestSolution = candidateNeighbor
                        #print('EL PUTO LOCAL SEARCH A TROBAT UNA SOLUCIO MILLOR %s'%(bestSolution.cost))
                        return(bestSolution, newcandidates)
                        #un cop acabat el for per cada candidat retornar el resultat


        #si sortim del for i no tenim solucio una solucio millor
        if(candidateNeighbor.cost > curCost or candidateNeighbor.wr!=0):
            candidateNeighbor = copy.deepcopy(bestSolution)
            #print('AQUESTA SOLUCIO ES UNA PORQUERIA: %s'%(bestSolution.cost))
            return(bestSolution, newcandidates)
            #return(bestSolution, newcandidates)


#------------------------ print Performance ------------------------------

    def printPerformance(self):
        if(not self.enabled): return

        avg_evalTimePerIteration = 0.0
        if(self.iterations != 0):
            avg_evalTimePerIteration = 1000.0 * self.elapsedTime / float(self.iterations)

        print ''
        print 'Local Search Performance:'
        print '  Num. Iterations Eval.', self.iterations
        print '  Total Eval. Time     ', self.elapsedTime, 's'
        print '  Avg. Time / Iteration', avg_evalTimePerIteration, 'ms'
