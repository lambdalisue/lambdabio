#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""DNA Ligation calculator module

Methods:
    calculate_required_vector_weight - Calculate required Vector weight
    calculate_required_insert_weight - Calculate required Insert weight
    calculate_required_weights - Calculate required weights of Vector and Insert


Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__author__  = 'Alisue <lambdalisue@hashnote.net>'
__version__ = '1.0.0'
__date__    = '2011-05-16'

def calculate_required_vector_weight(size):
    """Calculate required weight of Vector for Ligation.

    The best weight of ligation for pUC Vector(2,700 bp) is known as 50 ng.
    According to this fact, the best weight of Vector is calculated as:

        X = <size of vector in bp> / 2,700 * 50

    Args:
        size - the size of Vector DNA in bp

    Return:
        a calculated required weight in ng (float)
    """
    # 50/2,700 = 1/54
    return size / 54.0

def calculate_required_insert_weight(weight_vector, size_vector, size_insert):
    """Calculate required weight of Insert for Ligation.

    The best molar ratio of Vector and Insert is known as 1:6
    According to this fact, the best weight of Insert is calculated as:

        X = 6 * <weight of vector in ng> * <size of insert in bp> / <size of vector in bp>

    Args:
        weight_vector - the weight of Vector DNA in ng
        size_vector - the size of Vector DNA in bp
        size_insert - the size of Insert DNA in bp

    Return:
        a calculated required weight of insert in ng (float)
    """
    if not isinstance(size_vector, float):
        size_vector = float(size_vector)
    return 6 * weight_vector * size_insert / size_vector

def calculate_required_weights(size_vector, size_insert):
    """Calculate required weights of Vector and Insert for Ligation

    Args:
        size_vector - the size of Vector DNA in bp
        size_insert - the size of Insert DNA in bp

    Return:
        a tuple of weights of Vector and Insert in ng (tuple(float, float))
    """
    weight_vector = calculate_required_vector_weight(size_vector)
    weight_insert = calculate_required_insert_weight(weight_vector, size_vector,
            size_insert)
    return weight_vector, weight_insert

# --- unittest
import unittest
class TestCase(unittest.TestCase):
    def test_calculate_required_vector_weight(self):
        size = 5400
        weight = calculate_required_vector_weight(size)
        self.assertEquals(weight, 100)
    def test_calculate_required_insert_weight(self):
        weight_vector = 100
        size_vector = 5400
        size_insert = 540
        weight_insert = calculate_required_insert_weight(weight_vector,
                size_vector, size_insert)
        self.assertEquals(weight_insert, 60)
    def test_calculate_required_weights(self):
        size_vector = 5400
        size_insert = 540
        weight_vector, weight_insert = calculate_required_weights(size_vector,
                size_insert)
        self.assertEquals(weight_vector, 100)
        self.assertEquals(weight_insert, 60)

if __name__ == '__main__':
    unittest.main()
