'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''

from Solver import Solver
from Solution import Solution
from LocalSearch import LocalSearch
from Problem import Problem

# Inherits from a parent abstract solver.
class Solver_Greedy(Solver):

    #Procedure contructivePhase()
    #S <- {}           (Create the partials solutions)
    #Initialiaze C <--- Providers
    #While wr>0 && c!=0 is not a solution do
    #   c_best <-argmin{q(c)|c in C}
    #   S <- S union {c_best}
    #   C <- C/{c_best}
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

    def greedyConstruction(self, config, problem):
        #problem -> inputData(instance_1.dat) / config -> config.dat

        #-----------------create an empty solution with infinite cost)------------------------------------
        greedy_solution = Solution.createEmptySolution(config, problem)
        greedy_solution.cost = float('infinity')

        #-----------------Inicialitzar les decision variables-----------------------------------------

        greedy_solution.w = [0 for x in range(problem.inputData.providers)]         #Normal workers provided by a provider
        greedy_solution.ex = [0 for x in range(problem.inputData.providers)]        #extra workers provided by a provider
        greedy_solution.h= [0 for x in range(problem.inputData.providers)] 			#whether are picked the half of the available_workers or not
        greedy_solution.a = [0 for x in range(problem.inputData.providers)] 		#whether are picked the total of the available_workers of a provider or not
        greedy_solution.w5 = [0 for x in range(problem.inputData.providers)] 		#whether thre are hired more than 5 workers
        greedy_solution.w10 = [0 for x in range(problem.inputData.providers)]       #whether there are hired more than 10 workers or not

        # Keep track of the elapsed time and evaluated candidates
        elapsedEvalTime = 0
        evaluatedCandidates = 0

        #------------------- crear la candidate list -----------------------------------------------
        #candidatesProvider = []
        feasibleProviderAssignments, provider_elapsedEvalTime, provider_evaluatedCandidates = greedy_solution.findFeasibleProviderAssignments(problem, greedy_solution)
        #candidatesProvider.append(feasibleProviderAssignments)
        elapsedEvalTime += provider_elapsedEvalTime
        evaluatedCandidates += provider_evaluatedCandidates


        #-------------------- incialitzar el proces amb els candidats----------------

        providers_cost = 0
        ProvidersWithoutNone = [candidate for candidate in feasibleProviderAssignments if  candidate.providerId != None]
        while(len(ProvidersWithoutNone)>0 and greedy_solution.wr>0):
            minCostperworker = float('infinity')
            #choosenProviderId = None
            for candidate in feasibleProviderAssignments:  # for each candidate in candidate list
                if(candidate.providerId != None):
                    newcostsperworker, newnWorkers, newavailbleworkers = greedy_solution.getCost_provider(candidate.providerId, problem, greedy_solution, ProvidersWithoutNone)
                    for x in xrange(0,len(newcostsperworker)):
                        if (newcostsperworker[x] < minCostperworker):
                            minCostperworker=newcostsperworker[x]
                            nWorkers = newnWorkers[x]
                            availbleworkers = newavailbleworkers
                            #print('minCostperworker acutalized in solver %s.' % (str(minCostperworker)))
                            choosenProviderId = candidate.providerId

            if(choosenProviderId is None):
                greedy_solution.makeInfeasible()
                break

            # Assignar el provider obtingut
            greedy_solution.assign_provider(choosenProviderId, problem, greedy_solution )
            #print('provider assignat %s.' % (str(choosenProviderId)) )

            # ficar els valors a la solucio
            if (minCostperworker <= 0):
                minCost=minCostperworker*nWorkers+1000000
            if (minCostperworker > 0):
                minCost=minCostperworker*nWorkers
            #print('the cost of: %s is: %s .' % (str(choosenProviderId), str(minCost)))
            providers_cost += minCost
            greedy_solution.cost = round(providers_cost)
            greedy_solution.wr = greedy_solution.wr - nWorkers
            greedy_solution.w[choosenProviderId] = nWorkers
            if(nWorkers < availbleworkers):
                #print('-----------------available_workers: %s > number of workers %s .' % (str(availbleworkers),str(nWorkers)))
                greedy_solution.h[choosenProviderId] = 1
                #print('valor the h: %s .' % (greedy_solution.h[choosenProviderId]))
                greedy_solution.a[choosenProviderId] = 0
                #print('valor the a: %s .' % (greedy_solution.a[choosenProviderId]))
                greedy_solution.ex[choosenProviderId] = 0
                #print('valor the ex: %s .' % (greedy_solution.ex[choosenProviderId]))
                greedy_solution.w5[choosenProviderId] = 0
                #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                greedy_solution.w10[choosenProviderId] = 0
                #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
                if((nWorkers<11) and (nWorkers>5)):
                    greedy_solution.w5[choosenProviderId] = nWorkers-5
                    #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                    greedy_solution.w10[choosenProviderId] = 0
                    #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
                if(nWorkers>10):
                    greedy_solution.w5[choosenProviderId] = nWorkers-5
                    #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                    greedy_solution.w10[choosenProviderId] = nWorkers-10
                    #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
            if(nWorkers >= availbleworkers):
                #print('-------------------available_workers: %s <= number of workers %s .' % (str(availbleworkers),str(nWorkers)))
                greedy_solution.h[choosenProviderId] = 0
                #print('valor the h: %s .' % (greedy_solution.h[choosenProviderId]))
                greedy_solution.a[choosenProviderId] = 1
                #print('valor the a: %s .' % (greedy_solution.a[choosenProviderId]))
                greedy_solution.ex[choosenProviderId] = 0
                #print('valor the ex: %s .' % (greedy_solution.ex[choosenProviderId]))
                greedy_solution.w5[choosenProviderId] = 0
                #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                greedy_solution.w10[choosenProviderId] = 0
                #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
                if((nWorkers<11) and (nWorkers>5)):
                    greedy_solution.w5[choosenProviderId] = nWorkers-5
                    #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                    greedy_solution.w10[choosenProviderId] = 0
                    #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
                if(nWorkers>10):
                    greedy_solution.w5[choosenProviderId] = nWorkers-5
                    #print('valor the w5: %s .' % (greedy_solution.w5[choosenProviderId]))
                    greedy_solution.w10[choosenProviderId] = nWorkers-10
                    #print('valor the w10: %s .' % (greedy_solution.w10[choosenProviderId]))
                if(nWorkers > availbleworkers):
                    greedy_solution.ex[choosenProviderId] = nWorkers-availbleworkers
                    #print('%s = nWorkers: %s - availbleworkers %s .' % (str(greedy_solution.ex[choosenProviderId]),str(nWorkers),str(availbleworkers)))
            #print('provider %s added to the solution.' % (str(choosenProviderId)) )

            #check if the providers are still feasable or not
            for candidate in feasibleProviderAssignments:
                if(candidate.providerId != None):
                    #print('candidat a evaluar: %s'%(candidate.providerId))
                    if(not greedy_solution.isFeasibleToAssignProvider(candidate.providerId, problem, greedy_solution)):
                        candidate.providerId = None

            ProvidersWithoutNone = [candidate for candidate in feasibleProviderAssignments if  candidate.providerId != None]



        #make infeasible if we are out the loop and wr it's till > wr
        if(greedy_solution.wr>0):
            greedy_solution.makeInfeasible()



        return(greedy_solution, elapsedEvalTime, evaluatedCandidates)


    def solve(self, config, problem):
        self.startTimeMeasure()

        iteration = 0
        self.writeLogLine(float('infinity'), iteration)
        greedy_solution, elapsedEvalTime, evaluatedCandidates = self.greedyConstruction(config, problem)
        iteration += 1
        self.writeLogLine(greedy_solution.cost, iteration)

        if(config.localSearch and greedy_solution.isFeasible()):
            best_solution, iteration = LocalSearch(config).run(greedy_solution, problem, config, iteration)
            self.writeLogLine(best_solution.cost, iteration)
            greedy_solution = best_solution

        avg_evalTimePerCandidate = 0.0
        if (evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * elapsedEvalTime / float(evaluatedCandidates)

        print ''
        print 'Greedy Candidate Evaluation Performance:'
        print '  Num. Candidates Eval.', evaluatedCandidates
        print '  Total Eval. Time     ', elapsedEvalTime, 's'
        print '  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms'

        #LocalSearch(config).printPerformance()

        return(greedy_solution)
