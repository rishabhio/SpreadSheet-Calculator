from collections import deque 
from calculator.utils import Utils
from calculator.rpn import RPNCalculator

class Node:

    def __init__(self, value, in_degree, cell_type):
        self.value = value
        self.in_degree = in_degree 
        self.cell_type = cell_type 
        self.dependents = [ ] 
        self.processed = False 

    def add_dependent(self, dependent_key):
        self.dependents.append(dependent_key)
    
    def reduce_indegree(self):
        self.in_degree -= 1

    def get_value(self):
        return self.value
    
    def get_indegree(self):
        return self.in_degree
    
    def get_dependents(self):
        return self.dependents
    
    def get_cell_type(self):
        return self.cell_type   

    

class Graph:

    def __init__(self):
        self.adj_list = {} 


    def initialize(self, matrix, width, height):
        for h in range(height):
            for w in range(1, width+1):
                row = chr( ord('A') + h )
                col = w 
                cell = f'{row}{col}'
                val = matrix[h][w].strip().split(' ')
                cell_type, in_degree = Utils.get_type_degree(val)
                self.adj_list[cell] = Node(val, in_degree, cell_type)

        # fill the dependents
        return self._fill_dependents()

    def _fill_dependents(self):
        for k, v in self.adj_list.items():
            if v.get_cell_type() == 'VARIABLE_EXPRESSION' or v.get_cell_type() == 'VARIABLE': 
                value = v.get_value()
                for char in value:
                    if char.startswith('-') or char.startswith('+'):
                        char = char[1:]
                    if char.isalnum() and not Utils.is_number(char):
                        parent_key = char 
                        self.adj_list[parent_key].add_dependent(k)

        return True 
    

    def get_node(self, key):
        return self.adj_list[key]
    

    def has_cyclic_dependency(self):
        for _, v in self.adj_list.items():
            if v.get_indegree() != 0:
                return True
            
    def formatted_output(self):
        for _, v in self.adj_list.items():
            print(f'{v.get_value():.5f}')

    def evaluate( self ):
        queue = deque( ) 
        for k, v in self.adj_list.items():
            if v.get_indegree() == 0:
                queue.append( k )
        
        while queue:
            cell = queue.popleft()
            cell_value = self.adj_list[cell].get_value()
            if self.adj_list[cell].processed:
                continue
            if self.adj_list[cell].get_cell_type() == 'CONSTANT':
                self.adj_list[cell].value = float(cell_value[0])
                self.adj_list[cell].processed = True


            elif self.adj_list[cell].get_cell_type() == 'VARIABLE':
                parent = self.adj_list[cell].get_value()[0]
                if parent.startswith('-'):
                    parent = parent[1:]
                    self.adj_list[cell].value = self.adj_list[parent].get_value() * -1
                else:
                    self.adj_list[cell].value = self.adj_list[parent].get_value()
                self.adj_list[cell].processed = True
            else:
                value = RPNCalculator.evaluate_rpn( cell_value, self )
                self.adj_list[cell].value = value
                self.adj_list[cell].processed = True
            
            for dependent in self.adj_list[cell].get_dependents():
                self.adj_list[dependent].reduce_indegree()
                if self.adj_list[dependent].get_indegree() == 0:
                    queue.append( dependent )
        
        return 0