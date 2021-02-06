'''
This validate configuration is an adaptation of the code
provided by the professors of the course AMMM
'''


# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['instances_directory', 'file_name', 'file_extension', 'num_instances',
                            'max_wr','min_wr','providers','min_available_workers','max_available_workers',
                            'min_cost_contract','max_cost_contract','min_country','max_country',
							'min_cost_workers','max_cost_workers', 'min_cost_1', 'max_cost_1', 'min_cost_2',
                            'max_cost_2', 'min_cost_3','max_cost_3']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))


		# Directories
        instances_directory = data.instances_directory
        if(len(instances_directory) == 0): raise Exception('Value for instances_directory is empty')

        file_name = data.file_name
        if(len(file_name) == 0): raise Exception('Value for file_name is empty')

        file_extension = data.file_extension
        if(len(file_extension) == 0): raise Exception('Value for file_extension is empty')

        num_instances = data.num_instances
        if(not isinstance(num_instances, (int, long)) or (num_instances <= 0)):
            raise Exception('num_instances(%s) has to be a positive integer value.' % str(num_instances))

		# workers requested
        min_wr = data.min_wr
        if(not isinstance(min_wr, (int, long)) or (min_wr <= 0)):
            raise Exception('min_wr (%s) has to be a positive integer value.' % str(min_wr))

        max_wr = data.max_wr
        if(not isinstance(max_wr, (int, long)) or (max_wr <= 0)):
            raise Exception('max_wr (%s) has to be a positive integer value.' % str(max_wr))

        #providers
        providers = data.providers
        if(not isinstance(providers, (int, long)) or (providers <= 0)):
            raise Exception('providers(%s) has to be a positive integer value.' % str(providers))

        min_available_workers = data.min_available_workers
        if(not isinstance(min_available_workers, (int, long)) or (min_available_workers <= 0)):
            raise Exception('min_available_workers(%s) has to be a positive integer value.' % str(min_available_workers))

        max_available_workers = data.max_available_workers
        if(not isinstance(max_available_workers, (int, long)) or (max_available_workers <= 0)):
            raise Exception('max_available_workers(%s) has to be a positive integer value.' % str(max_available_workers))

        min_cost_workers = data.min_cost_workers
        if(not isinstance(min_cost_workers, (int, long)) or (min_cost_workers <= 0)):
            raise Exception('min_cost_workers(%s) has to be a positive integer value.' % str(min_cost_workers))

        max_cost_workers = data.max_cost_workers
        if(not isinstance(max_cost_workers, (int, long)) or (max_cost_workers <= 0)):
            raise Exception('max_cost_workers(%s) has to be a positive integer value.' % str(max_cost_workers))

        min_cost_contract = data.min_cost_contract
        if(not isinstance(min_cost_contract, (int, long)) or (min_cost_contract <= 0)):
            raise Exception('min_cost_contract(%s) has to be a positive integer value.' % str(min_cost_contract))

        max_cost_contract = data.max_cost_contract
        if(not isinstance(max_cost_contract, (int, long)) or (max_cost_contract <= 0)):
            raise Exception('max_cost_contract(%s) has to be a positive integer value.' % str(max_cost_contract))

        min_country = data.min_country
        if(not isinstance(min_country, (int, long)) or (min_country <= 0)):
            raise Exception('min_country(%s) has to be a positive integer value.' % str(min_country))

        max_country = data.max_country
        if(not isinstance(max_country, (int, long)) or (max_country <= 0)):
            raise Exception('max_country(%s) has to be a positive integer value.' % str(max_country))

        min_cost_1 = data.min_cost_1
        if(not isinstance(min_cost_1, (int, long)) or (min_cost_1 <= 0)):
            raise Exception('min_cost_1(%s) has to be a positive integer value.' % str(min_cost_1))

        max_cost_1 = data.max_cost_1
        if(not isinstance(max_cost_1, (int, long)) or (max_cost_1 <= 0)):
            raise Exception('max_cost_1(%s) has to be a positive integer value.' % str(max_cost_1))

        min_cost_2 = data.min_cost_2
        if(not isinstance(min_cost_2, (int, long)) or (min_cost_2 <= 0)):
            raise Exception('min_cost_2(%s) has to be a positive integer value.' % str(min_cost_2))

        max_cost_2 = data.max_cost_2
        if(not isinstance(max_cost_2, (int, long)) or (max_cost_2 <= 0)):
            raise Exception('max_cost_2(%s) has to be a positive integer value.' % str(max_cost_2))

        min_cost_3 = data.min_cost_3
        if(not isinstance(min_cost_3, (int, long)) or (min_cost_3 <= 0)):
            raise Exception('min_cost_3(%s) has to be a positive integer value.' % str(min_cost_3))

        max_cost_3 = data.max_cost_3
        if(not isinstance(max_cost_3, (int, long)) or (max_cost_3 <= 0)):
            raise Exception('max_cost_3(%s) has to be a positive integer value.' % str(max_cost_3))
