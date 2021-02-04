# -*- coding: utf-8 -*-

# Contributors:
#    Antonio López Martínez-Carrasco <antoniolopezmc1995@gmail.com>

"""This file contains the avaible operators which can be used by the selectors.
"""

from enum import Enum
from subgroups import exceptions

class Operator(Enum):
    
    """This enumerator provides the available operators which can be used by the selectors.
    """
    
    EQUAL = 1
    NOT_EQUAL = 2
    LESS = 3
    GREATER = 4
    LESS_OR_EQUAL = 5
    GREATER_OR_EQUAL = 6
    
    def evaluate(self, left_element, right_element):
        """Method to evaluate whether the expression (left_element self right_element) is True.
        
        :type left_element: str, int or float
        :param left_element: the left element of the expression.
        :type right_element: str, int or float
        :param right_element: the right element of the expression.
        :rtype: bool
        :return: whether the expression (left_element self right_element) is True.
        """
        try:
            if self == Operator.EQUAL:
                return left_element == right_element
            elif self == Operator.NOT_EQUAL:
                return left_element != right_element
            elif self == Operator.LESS:
                return left_element < right_element
            elif self == Operator.GREATER:
                return left_element > right_element
            elif self == Operator.LESS_OR_EQUAL:
                return left_element <= right_element
            elif self == Operator.GREATER_OR_EQUAL:
                return left_element >= right_element
            else:
                raise exceptions.OperatorNotSupportedError("This operator has not been added to the method 'evaluate'.")
        except TypeError: # If the operator is not supported between the two values, a TypeError exception is raised. In this case, the evaluation is always False.
            return False
    
    @staticmethod
    def generate_from_str(input_str):
        """Static method to generate an Operator from a str.
        
        :type input_str: str
        :param input_str: the str from which to generate the Operator.
        :rtype: Operator
        :return: the operator generated from the str.
        """
        if type(input_str) is not str:
            raise TypeError("The type of the parameter 'input_str' must be 'str'.")
        if input_str == "=":
            return Operator.EQUAL
        elif input_str == "!=":
            return Operator.NOT_EQUAL
        elif input_str == "<":
            return Operator.LESS
        elif input_str == ">":
            return Operator.GREATER
        elif input_str == "<=":
            return Operator.LESS_OR_EQUAL
        elif input_str == ">=":
            return Operator.GREATER_OR_EQUAL
        else:
            raise AttributeError("The parameter 'input_str' (with the value '" + input_str + "') does not match with any operator.")
    
    def __eq__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value == other.value
    
    def __ne__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value != other.value
    
    def __lt__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value < other.value
    
    def __gt__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value > other.value
    
    def __le__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value <= other.value
    
    def __ge__(self, other):
        if not isinstance(other, Operator):
            raise TypeError("The type of the parameter must be 'Operator'.")
        return self.value >= other.value
    
    def __str__(self):
        if self == Operator.EQUAL:
            return "="
        elif self == Operator.NOT_EQUAL:
            return "!="
        elif self == Operator.LESS:
            return "<"
        elif self == Operator.GREATER:
            return ">"
        elif self == Operator.LESS_OR_EQUAL:
            return "<="
        elif self == Operator.GREATER_OR_EQUAL:
            return ">="
        else:
            raise exceptions.OperatorNotSupportedError("This operator does not have a string representation (method '__str__').")
    
    def __hash__(self):
        return hash(self.value)
