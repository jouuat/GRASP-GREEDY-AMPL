'''
This instance generator is an adaptation of the code
provided by the professors of the course AMMM
'''

import os, random

# Generate instances based on read configuration.
class InstanceGenerator(object):
    def __init__(self, config):
        self.config = config

    def generate(self):
		# set the directories and names
        instances_directory = self.config.instances_directory
        file_name = self.config.file_name
        file_extension = self.config.file_extension
        num_instances = self.config.num_instances

		# Requested Workers
        min_wr = self.config.min_wr
        max_wr = self.config.max_wr

		# Providers
        providers = self.config.providers
        min_available_workers = self.config.min_available_workers
        max_available_workers = self.config.max_available_workers
        min_cost_contract = self.config.min_cost_contract
        max_cost_contract = self.config.max_cost_contract
        min_country = self.config.min_country
        max_country = self.config.max_country
        min_cost_workers = self.config.min_cost_workers
        max_cost_workers = self.config.max_cost_workers
        min_cost_1 = self.config.min_cost_1
        max_cost_1 = self.config.max_cost_1
        min_cost_2 = self.config.min_cost_2
        max_cost_2 = self.config.max_cost_2
        min_cost_3 = self.config.min_cost_3
        max_cost_3 = self.config.min_cost_3


		# Generate the instances
        for i in xrange(1, num_instances + 1):
            # directories
            instancePath = os.path.join(instances_directory, '%s_%d.%s' % (file_name, i, file_extension))
            file_instance = open(instancePath, 'w')

            # Requested Workers

            wr = random.randint(min_wr, max_wr)

            # Providers

            cost_1=random.randint(min_cost_1, max_cost_1)
            cost_2=random.randint(min_cost_2, max_cost_2)
            cost_3=random.randint(min_cost_3, max_cost_3)


            available_workers=[]
            cost_contract=[]
            country=[]
            cost_workers=[]



            for service in xrange(0, providers):
                available_workers.append(2*random.randint(min_available_workers, max_available_workers))
                cost_contract.append(random.randint(min_cost_contract, max_cost_contract)) # random between min and max values
                country.append(random.randint(min_country, max_country)) # random between min and max values
                cost_workers.append(random.randint(min_cost_workers, max_cost_workers)) # random between min and max values


			# Write the output
            file_instance.write('//	Requested Workers;\n')
            file_instance.write('wr = %d;\n' % wr)


            file_instance.write('//	Providers;\n')
            file_instance.write('providers = %d;\n' % providers)
            file_instance.write('available_workers = [%s];\n' % (' '.join(map(str, available_workers))))
            file_instance.write('cost_contract = [%s];\n' % (' '.join(map(str, cost_contract))))
            file_instance.write('country = [%s];\n' % (' '.join(map(str, country))))
            file_instance.write('cost_workers = [%s];\n' % (' '.join(map(str, cost_workers))))
            file_instance.write('cost_1 = %d;\n' % cost_1)
            file_instance.write('cost_2 = %d;\n' % cost_2)
            file_instance.write('cost_3 = %d;\n' % cost_3)



            file_instance.close()
