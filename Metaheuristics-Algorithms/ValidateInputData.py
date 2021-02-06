'''
This validate input data is an adaptation of the code
provided by the professors of the course AMMM
'''

class ValidateInputData(object):
    @staticmethod

    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['wr','providers','available_workers',
                          'cost_contract','country',
						  'cost_workers', 'cost_1', 'cost_2',
                           'cost_3']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))


		# workers requested
        wr = data.wr
        if(not isinstance(wr, (int, long)) or (wr <= 0)):
            raise Exception('wr (%s) has to be a positive integer value.' % str(wr))

        #providers
        '''
        providers = data.providers
        if(not isinstance(providers, (int, long)) or (providers <= 0)):
            raise Exception('providers(%s) has to be a positive integer value.' % str(providers))

        available_workers = data.available_workers
        if(not isinstance(available_workers, (int, long)) or (available_workers <= 0)):
            raise Exception('available_workers(%s) has to be a positive integer value.' % str(available_workers))

        cost_workers = data.cost_workers
        if(not isinstance(cost_workers, (int, long)) or (cost_workers <= 0)):
            raise Exception('cost_workers(%s) has to be a positive integer value.' % str(cost_workers))

	    country = data.min_country
        if(not isinstance(min_country, (int, long)) or (min_country <= 0)):
            raise Exception('min_country(%s) has to be a positive integer value.' % str(min_country))

        country = data.country
        if(not isinstance(country, (int, long)) or (country <= 0)):
            raise Exception('country(%s) has to be a positive integer value.' % str(country))

        cost_1 = data.cost_1
        if(not isinstance(cost_1, (int, long)) or (cost_1 <= 0)):
            raise Exception('cost_1(%s) has to be a positive integer value.' % str(cost_1))

        cost_2 = data.cost_2
        if(not isinstance(cost_2, (int, long)) or (cost_2 <= 0)):
            raise Exception('cost_2(%s) has to be a positive integer value.' % str(cost_2))

        cost_3 = data.cost_3
        if(not isinstance(cost_3, (int, long)) or (cost_3 <= 0)):
            raise Exception('cost_3(%s) has to be a positive integer value.' % str(cost_3))
        '''
