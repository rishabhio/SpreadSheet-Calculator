import sys 
from calculator.graph import Graph 


class App:

    @staticmethod 
    def run():
        """
            Run the application 
        """
        # Step-1 Read Input 
        user_input = sys.stdin.read() 
        if not user_input:
            print('Error: No input found, Please provide the input and try again')
            return -1
        lines = user_input.split('\n')
        meta_data = lines[0].split(' ')
        width, height = map(int, meta_data)

        # Step-1.1 Make sure input size is correct 
        if len(lines) != width * height + 1:
            print('Error: Input size does not match the width and height specified')
            return -1

        # Step-2 Parse the Input 
        data = [ ] 
        for line in lines[1:]:
            data.append(line.split(','))
        
        # Step-3 Initialize and populate the Graph Matrix 
        matrix = [
            [ None for _ in range( width + 1 ) ]
            for _ in range( height )
        ]
        # fill in the initial values in matrix 
        for h in range( height ):
            for w in range( 1, width + 1 ):
                matrix[h][w] = data.pop(0)[0]

        # Step-4 Initialize the Graph 
        graph = Graph() 
        graph.initialize(matrix, width, height)
        graph.evaluate()

        # Step-5 Check for Cyclic Dependency 
        if graph.has_cyclic_dependency():
            print('Error: Cyclic dependency detected, Please check the input and try again')
            return -1 

        # Step-6 Print the Result 
        print(f'{width} {height}')
        graph.formatted_output() 


if __name__ == '__main__':
    App.run()