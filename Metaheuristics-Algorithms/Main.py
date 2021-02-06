'''
This file is an adaptation of the code
provided by the professors of the course AMMM
'''
#encoding: utf-8

import argparse
import sys

from DATParser import DATParser
from ValidateInputData import ValidateInputData
from ValidateConfig import ValidateConfig
from Solver_Greedy import Solver_Greedy
from Solver_GRASP import Solver_GRASP
from Problem import Problem



def run():
    try:
        #des del terminal agafara l'argument com  a configFile
        argp = argparse.ArgumentParser(description='AMMM Lab Heuristics')
        argp.add_argument('configFile', help='configuration file path')
        args = argp.parse_args()

        print 'AMMM Lab Heuristics'
        print '-------------------'

        print 'Reading Config file %s...' % args.configFile
        config = DATParser.parse(args.configFile)
        ValidateConfig.validate(config)
        print 'Config validated'

        print 'Reading Input Data file %s...' % config.inputDataFile
        inputData = DATParser.parse(config.inputDataFile)
        ValidateInputData.validate(inputData)
        print 'Input validated'

        print 'Creating Problem...'
        problem = Problem(inputData)
        print 'Problem created'


        #f(problem.checkInstance()):
        #    print 'Solving Problem...'
        #    solver = None
        #    solution = None
        #    if(config.solver == 'Greedy'):
        #        solver = Solver_Greedy()
        #        solution = solver.solve(config, problem)
        #    elif(config.solver == 'GRASP'):
        #        solver = Solver_GRASP()
        #        solution = solver.solve(config, problem)
        #
        #    solution.saveToFile(config.solutionFile)
        #else:
        #    print 'Instance is infeasible.'
        #    solution = Solution.createEmptySolution(config, problem)
        #    solution.makeInfeasible()
        #    solution.saveToFile(config.solutionFile)


        print 'Solving Problem...'
        solver = None
        solution = None
        if(config.solver == 'Greedy'):
            solution = Solver_Greedy().solve(config, problem)
        elif(config.solver == 'GRASP'):
            solution = Solver_GRASP().solve(config, problem)
        #for f in solution.ex:
            #print('extra %s.' % (str(f)) )
        solution.saveToFile(config.solutionFile, solution.wr ,solution.w, solution.h, solution.a, solution.w5, solution.w10, solution.ex)
        print 'Problem solved'
        return(0)


    except Exception as e:
        print
        print 'Exception:', e
        import traceback
        traceback.print_exc(file=sys.stdout)
        print
        return(1)

if __name__ == '__main__':
    sys.exit(run())
