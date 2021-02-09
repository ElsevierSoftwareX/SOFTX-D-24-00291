# -*- coding: utf-8 -*-

# Contributors:
#    Antonio López Martínez-Carrasco <antoniolopezmc1995@gmail.com>

"""This file contains the implementation of a 'Subgroup'. A 'Subgroup' has a condition (Pattern) and a target variable of interest (Selector).
"""

from subgroups.core.selector import Selector
from subgroups.core.pattern import Pattern
from pandas import DataFrame

class Subgroup(object):
    """This class represents a 'Subgroup'. A 'Subgroup' has a condition (Pattern) and a target variable of interest (Selector).
    
    :type condition: Pattern
    :param condition: a Pattern.
    :type target: Selector
    :param target: a Selector.
    """
    
    __slots__ = "_condition", "_target" 
    
    def __init__(self, condition, target):
        if not isinstance(condition, Pattern):
            raise TypeError("The type of the parameter 'condition' must be 'Pattern'.")
        if not isinstance(target, Selector):
            raise TypeError("The type of the parameter 'target' must be 'Selector'.")
        self._condition = condition
        self._target = target
    
    def copy(self):
        """Method to copy the Subgroup.
        :rtype: Subgroup
        :return: the copy of the Subgroup.
        """
        # We create a copy of the pattern to avoid aliasing between subgroups.
        return Subgroup(self._condition.copy(), self._target)
    
    def _get_condition(self):
        return self._condition
    
    condition = property(_get_condition, None, None, "The condition.")
    
    def _get_target(self):
        return self._target
    
    target = property(_get_target, None, None, "The target variable of interest.")
    
    def filter(self, pandas_dataframe, use_condition=True, use_target=True):
        """Method to filter a pandas DataFrame, retrieving only the rows covered by the subgroup.
        
        :type pandas_dataframe: pandas.DataFrame
        :param pandas_dataframe: the DataFrame which is filtered.
        :type use_condition: bool
        :param use_condition: whether the subgroup condition is used in the filtering process. By default, True.
        :type use_target: bool
        :param use_target: whether the subgroup target is used in the filtering process. By default, True.
        :rtype: tuple
        :return: a tuple of the form: (DataFrame, tp, fp, TP, FP). The first element is the DataFrame obtained after the filtering process. The other elements are the true positives tp (rows covered by the condition and the target), the false positives fp (rows covered by the condition but not by the target), the True Positives TP (rows covered by the target) and the False Positives FP (rows not covered by the target). IMPORTANT: These values are computed with the complete subgroup (condition and target). This means that, for a given DataFrame, they are always the same no matter the values of the parameters 'use_condition' and 'use_target'.
        """
        if not isinstance(pandas_dataframe, DataFrame):
            raise TypeError("The type of the parameter 'pandas_dataframe' must be 'pandas.Dataframe'.")
        if type(use_condition) is not bool:
            raise TypeError("The type of the parameter 'use_condition' must be 'bool'.")
        if type(use_target) is not bool:
            raise TypeError("The type of the parameter 'use_target' must be 'bool'.")
        pandas_DataFrame__all_except_the_target_attribute = pandas_dataframe[pandas_dataframe.columns.drop(self._target._attribute_name)]
        pandas_Series__target_attribute = pandas_dataframe[self._target._attribute_name]
        condition_is_contained = self._condition.is_contained(pandas_DataFrame__all_except_the_target_attribute)
        target_match = self._target.match(self._target._attribute_name, pandas_Series__target_attribute)
        bool_Series_condition_is_contained_AND_target_match = condition_is_contained & target_match
        tp = (bool_Series_condition_is_contained_AND_target_match).sum()
        fp = (condition_is_contained & (~ target_match)).sum()
        TP = target_match.sum()
        FP = len(pandas_dataframe) - TP
        if (use_condition) and (use_target):
            return (pandas_dataframe[bool_Series_condition_is_contained_AND_target_match], tp, fp, TP, FP)
        elif (use_condition) and (not use_target):
            return (pandas_dataframe[condition_is_contained], tp, fp, TP, FP)
        elif (not use_condition) and (use_target):
            return (pandas_dataframe[target_match], tp, fp, TP, FP)
        else:
            return (pandas_dataframe, tp, fp, TP, FP)
    
    @staticmethod
    def generate_from_str(input_str):
        """Static method to generate a Subgroup from a str.
        
        :type input_str: str
        :param input_str: the str from which to generate the Subgroup. We assume the format defined by the following regular expressions: 'Condition: <pattern>, Target: <selector>'. The format of <selector> and <pattern> is defined by their corresponding 'generate_from_str' methods.
        :rtype: Subgroup
        :return: the Subgroup generated from the str.
        """
        if type(input_str) is not str:
            raise TypeError("The type of the parameter 'input_str' must be 'str'.")
        input_str_split = input_str.split(", Target: ")
        target = Selector.generate_from_str(input_str_split[1])
        condition = Pattern.generate_from_str(input_str_split[0][11:]) # [11:] -> Delete the initial string "Condition: ".
        return Subgroup(condition, target)
    
    def __eq__(self, other):
        if not isinstance(other, Subgroup):
            raise TypeError("The type of the parameter must be 'Subgroup'.")
        return (self._condition == other._condition) and (self._target == other._target)
    
    def __ne__(self, other):
        if not isinstance(other, Subgroup):
            raise TypeError("The type of the parameter must be 'Subgroup'.")
        return (self._condition != other._condition) or (self._target != other._target)
    
    def __str__(self):
        return "Condition: " + str(self.condition) + ", Target: " + str(self.target)
