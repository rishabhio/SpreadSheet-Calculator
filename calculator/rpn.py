from calculator.utils import Utils 

class RPNCalculator:

    @staticmethod
    def evaluate_rpn( expression, graph ):
        stack = [ ] 
        for token in expression:
            if token.startswith('-') and Utils.is_variable( token[1:] ):
                _val = graph.get_node(token[1:]).get_value() * -1 
                stack.append(_val)
            elif Utils.is_variable( token ):
                stack.append( graph.get_node(token).get_value() )
            elif Utils.is_number( token ):
                stack.append( float(token) )
            elif token == '++':
                operand = stack.pop()
                stack.append(operand + 1)
            elif token == '--':
                operand = stack.pop()
                stack.append(operand - 1)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        raise ZeroDivisionError('Division by zero')
                    result = int(operand1 / operand2)
                stack.append(result)
        return stack[0]
