class Utils:

    @staticmethod 
    def is_number(value):
        try:
            float( value ) 
            return True
        except ValueError:
            return False
        
    @staticmethod
    def is_variable(value):
        if value.isalnum() and not Utils.is_number(value):
            return True
        return False 
    
    @staticmethod
    def get_type_degree( cell ):
        """
            Available types:
            - constant ( mathematical number with a sign )
            - variable ( cell reference, alphabet + number )
            - expression with constants ( mathematical number with a sign + mathematical symbols )
            - expression with variables ( cell reference ( alphabet + number ) + mathematical symbols )
            - symbols considered: ( +, -, *, /, ++, -- )
        """
        count_of_alnums = 0 
        count_of_literals = 0 
        for char in cell:
            if char.startswith('-') or char.startswith('+'):
                char = char[1:]
            if char.isalnum() and Utils.is_number(char):
                count_of_literals += 1 
            elif char.isalnum() and not Utils.is_number(char):
                count_of_alnums += 1
        
        if count_of_literals == len(cell) == 1:
            return 'CONSTANT', 0
        elif count_of_alnums == len(cell) == 1:
            return 'VARIABLE', 1
        elif count_of_literals > 0 and count_of_alnums == 0:
            return 'CONSTANT_EXPRESSION', 0
        else:
            return 'VARIABLE_EXPRESSION', count_of_alnums