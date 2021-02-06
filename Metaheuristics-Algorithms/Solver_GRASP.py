'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''

import random, time, copy
from Solver import Solver
from Solution import Solution
from LocalSearch import LocalSearch


# Inherits from a parent abstract solver.
class Solver_GRASP(Solver):

    #Procedure contructivePhase()
    #S <- {}           (Create the partials solutions)
    #Initialiaze C <--- Providers
    #While wr>0 && c!=0 is not a solution do
    #   evaluate the incremental cost of q(c) forall c in C
    #   q_min <-argmin{q(c)|c in C}
    #   q_max <-argmax{q(c), q(c)<infinite|c in C}
    #   RCL <- {c in C| q(c)<=q_min+alpha*(q_max-q_min)}
    #   select c that belongs in RCL randomly
    #   S <- S union {c_best}
    #   C <- C/{c_best}
    #   reevaluate the incremental cost q(c) forall c in C
    #   if availbleworkers[c_best]>wr then wr<--wr-1/2*availbleworkers[c_best]
    #   else availbleworkers[c_best]<wr then wr<--wr-availbleworkers[c_best]
    #end while
    #if wr>0 return infeasible;
    #return S

    #q(c)-->(inifnite->if infesasblecandidate(p, S(p) || 1/2*availbleworkers[c_best]>wr, (cost_contract+c*cost_worker)/num_workers->if not infesasblecandidate(p, S(p))

    #infesasblecandidate(c, C pertany C){
    #   foreach(c' in C){
    #       if country[c][c`]=1 retrun true
    #       otherwise return false
    #   }
    #}

    def greedyRandomizedConstruction(self, config, problem):

        #-----------------create an empty solution with infinite cost)------------------------------------
        grasp_solution = Solution.createEmptySolution(config, problem)
        grasp_solution.cost = float('infinity')

        #-----------------Inicialitzar les decision variables-----------------------------------------

        grasp_solution.w = [0 for x in range(problem.inputData.providers)]         #Normal workers provided by a provider
        grasp_solution.ex = [0 for x in range(problem.inputData.providers)]        #extra workers provided by a provider
        grasp_solution.h= [0 for x in range(problem.inputData.providers)] 			#whether are picked the half of the available_workers or not
        grasp_solution.a = [0 for x in range(problem.inputData.providers)] 		#whether are picked the total of the available_workers of a provider or not
        grasp_solution.w5 = [0 for x in range(problem.inputData.providers)] 		#whether thre are hired more than 5 workers
        grasp_solution.w10 = [0 for x in range(problem.inputData.providers)]       #whether there are hired more than 10 workers or not

        # Keep track of the elapsed time and evaluated candidates
        elapsedEvalTime = 0
        evaluatedCandidates = 0

        #------------------- crear la candidate list -----------------------------------------------
        #candidatesProvider = []
        feasibleProviderAssignments, provider_elapsedEvalTime, provider_evaluatedCandidates = grasp_solution.findFeasibleProviderAssignments(problem, grasp_solution)
        #candidatesProvider.append(feasibleProviderAssignments)
        elapsedEvalTime += provider_elapsedEvalTime
        evaluatedCandidates += provider_evaluatedCandidates


        #-------------------- incialitzar el proces amb els candidats----------------

        ProvidersWithoutNone = [candidate for candidate in feasibleProviderAssignments if  candidate.providerId != None]

        providers_cost = 0
        while(len(ProvidersWithoutNone)>0 and grasp_solution.wr>0):
            candidateListSorted = []
            choosenProviderId = None
            #ordenar els candidats
            #print(' feasibleProviderAssignments: %s' %(len(feasibleProviderAssignments)))
            for candidate in feasibleProviderAssignments:
                if(candidate.providerId != None):
                    newcostsperworker, newnWorkers, newavailbleworkers = grasp_solution.getCost_provider(candidate.providerId, problem, grasp_solution, ProvidersWithoutNone)
                    for x in xrange(0,len(newcostsperworker)):
                        candidateListSorted.append([candidate.providerId, newcostsperworker[x], newnWorkers[x], newavailbleworkers])
                        #print( 'id %s, newcost %s, newworkers %s, newavailbleworkers %s'%(candidate.providerId, newcostsperworker[x], newnWorkers[x], newavailbleworkers))
            candidateListSorted.sort(key=lambda x:x[1])

            #calcular el min i max cost per limitar el RCL
            alpha = config.alpha
            if(len(candidateListSorted) == 0):
                provider_cost = float('infinity')
                grasp_solution.makeInfeasible()
                break
            firstcandidate = candidateListSorted[0]
            lastcandidate = candidateListSorted[len(candidateListSorted)-1]
            #firstcandidatetupple = firstcandidate[1]
            #lastcandidatetupple = lastcandidate[1]
            min_cost_Provider = firstcandidate[1]
            max_cost_Provider = lastcandidate[1]
            #print('min cost porvider %s' %(min_cost_Provider))
            #print( 'max cost: %s min cost: %s' %(min_cost_Provider, max_cost_Provider))
            boundaryCost = min_cost_Provider + (max_cost_Provider - min_cost_Provider) * alpha
            # agafar els elements amb cost menor que el boundary
            maxIndex = 0
            for x in candidateListSorted:
                #print('candidate(0): %s' %(candidate[0]))
                if(x[1] > boundaryCost):
                    break
                maxIndex += 1
            # creem la RCL
            rcl = candidateListSorted[0:maxIndex]
            #agafem un randoml
            if(len(rcl) == 0):
                choosenProviderId = None
            else:
                choosenProvider = random.choice(rcl)
                choosenProviderId = choosenProvider[0]
                minCostperworker = choosenProvider[1]
                nWorkers = choosenProvider[2]
                availbleworkers = choosenProvider[3]
                #print( 'providerId: %s, minCostperworker: %s, nworkers: %s, availbleworkers: %s' %(choosenProviderId, minCostperworker, nWorkers, availbleworkers))
            if(choosenProviderId is None):
                grasp_solution.makeInfeasible()
                break

            # Assignar el provider obtingut
            grasp_solution.assign_provider(choosenProviderId, problem, grasp_solution )
            #print('provider assignat %s.' % (str(choosenProviderId)) )

            # ficar els valors a la solucio
            if (minCostperworker <= 0):
                minCost=minCostperworker*nWorkers+1000000
            if (minCostperworker > 0):
                minCost=minCostperworker*nWorkers
            #print('the cost of: %s is: %s .' % (str(choosenProviderId), str(minCost)))
            providers_cost += minCost
            #print('and the total cost is: %s .' % (str(providers_cost)))
            grasp_solution.cost = round(providers_cost)
            grasp_solution.wr = grasp_solution.wr - nWorkers
            grasp_solution.w[choosenProviderId] = nWorkers
            if(nWorkers < availbleworkers):
                grasp_solution.h[choosenProviderId] = 1
                grasp_solution.a[choosenProviderId] = 0
                grasp_solution.ex[choosenProviderId] = 0
                grasp_solution.w5[choosenProviderId] = 0
                grasp_solution.w10[choosenProviderId] = 0
                if((nWorkers<11) and (nWorkers>5)):
                    grasp_solution.w5[choosenProviderId] = nWorkers-5
                    grasp_solution.w10[choosenProviderId] = 0
                if(nWorkers>10):
                    grasp_solution.w5[choosenProviderId] = nWorkers-5
                    grasp_solution.w10[choosenProviderId] = nWorkers-10
            if(nWorkers >= availbleworkers):
                grasp_solution.h[choosenProviderId] = 0
                grasp_solution.a[choosenProviderId] = 1
                grasp_solution.ex[choosenProviderId] = 0
                grasp_solution.w5[choosenProviderId] = 0
                grasp_solution.w10[choosenProviderId] = 0
                if((nWorkers<11) and (nWorkers>5)):
                    grasp_solution.w5[choosenProviderId] = nWorkers-5
                    grasp_solution.w10[choosenProviderId] = 0
                if(nWorkers>10):
                    grasp_solution.w5[choosenProviderId] = nWorkers-5
                    grasp_solution.w10[choosenProviderId] = nWorkers-10
                if(nWorkers > availbleworkers):
                    grasp_solution.ex[choosenProviderId] = nWorkers-availbleworkers


            #check if the providers are still feasable or not
            for candidate in feasibleProviderAssignments:
                if(candidate.providerId != None):
                    if(not grasp_solution.isFeasibleToAssignProvider(candidate.providerId, problem, grasp_solution)):
                        candidate.providerId = None

            ProvidersWithoutNone = [candidate for candidate in feasibleProviderAssignments if  candidate.providerId != None]



            #for candidate in feasibleProviderAssignments:
                #if(candidate.providerId == None):
                    #feasibleProviderAssignments.pop(0)

            #for candidate in feasibleProviderAssignments:
                #if(candidate.providerId == None):
                    #print('this message shouldnt appear')



        #make infeasible if we are out the loop and wr it's till > wr
        if(grasp_solution.wr>0):
            grasp_solution.makeInfeasible()


        return(grasp_solution, elapsedEvalTime, evaluatedCandidates)



    def solve(self, config, problem):
        bestSolution = Solution.createEmptySolution(config, problem)
        bestSolution.makeInfeasible()
        bestSolution_cost = bestSolution.cost   # infinity
        self.startTimeMeasure()
        self.writeLogLine(bestSolution_cost, 0)

        iteration = 0

        total_elapsedEvalTime = 0
        total_evaluatedCandidates = 0
        startEvalTime = time.time()

        while(time.time() - startEvalTime < config.maxExecTime):
            grasp_solution, it_elapsedEvalTime, it_evaluatedCandidates = self.greedyRandomizedConstruction(config, problem)
            total_elapsedEvalTime += it_elapsedEvalTime
            total_evaluatedCandidates += it_evaluatedCandidates
            iteration += 1

            if(not grasp_solution.isFeasible()): continue

            if(config.localSearch):
                grasp_solution, iteration = LocalSearch(config).run(grasp_solution, problem, config, iteration)

            solution_cost = grasp_solution.cost
            if(solution_cost < bestSolution_cost):
                #print('----------------------------SOL UPDATED -------------------------------')
                bestSolution = copy.deepcopy(grasp_solution)
                bestSolution_cost = bestSolution.cost
                self.writeLogLine(bestSolution_cost, iteration)

        self.writeLogLine(bestSolution.cost, iteration)

        avg_evalTimePerCandidate = 0.0
        if (total_evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * total_elapsedEvalTime / float(total_evaluatedCandidates)

        print ''
        print 'Greedy Candidate Evaluation Performance:'
        print '  Num. Candidates Eval.', total_evaluatedCandidates
        print '  Total Eval. Time     ', total_elapsedEvalTime, 's'
        print '  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms'

        #LocalSearch(config).printPerformance()

        return(bestSolution)
