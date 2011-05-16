#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""Restriction Enzyme Calculation module

Methods:
    convert_weight_to_molar - Convert weight in [g] to molar
    calculate_molecular_weight - Calculate DNA molecular weight via size
    calculate_site_molar - Calculate site molar in solution
    calculate_unit_activity - Calculate enzyme unit activity
    calculate_unit_required - Calculate unit required to cut DNA


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

# The average molecular weight of base pair in double strand DNA
BASE_PAIR_MOLECULAR_WEIGHT = 660

def convert_weight_to_molar(mw, weight=1):
    """Convert weight to molar
    
    The conversion is calculated as:

        1 [mol] : mw [g] = x [mol] : weight [g]
                       x = 1 * weight / mw

    Args:
        mw - the molecular weight
        weight - the weight in [g]

    Returns:
        converted molar (float)
    """
    if not isinstance(mw, float):
        mw = float(mw)
    return weight / mw

def calculate_molecular_weight(size):
    """"Calculate molecular weight of DNA via DNA size in [bp]
    
    Args:
        size - the size of a DNA in [bp]

    Return:
        Mw (float) - the calculated molecular weight
    """
    return size * BASE_PAIR_MOLECULAR_WEIGHT

def calculate_site_molar(n, weight, size):
    """Calculate restriction site molar in solution.
    
    Args:
        n - the number of restriction sites per DNA
        weight - the total DNA mass in solution.
        size - the size of DNA in bp.

    Return:
        molar (float) - the molar of restriction site in soltion
    """
    mw = calculate_molecular_weight(size)
    molar = convert_weight_to_molar(mw, weight)
    return n * molar

def calculate_unit_activity(enzyme):
    """Calculate a unit activity of Enzyme
    
    Args:
        enzyme - the instance of enzyme or path of

    Return:
        molar (float) - the molar of restriction site which the
            enzyme can cut per hour at 37 celcius.
    """
    return calculate_site_molar(enzyme.substrate.sites, 1,
            enzyme.substrate.size)

def calculate_unit_required(sites, size, weight, enzyme):
    """Calculate unit required to cut all restriction sites in DNA
    
    Calculate unit required to cut all restriction sites in DNA
    for hour at 37 celcius(the temperature is depend on the enzyme 
    temperature. generally most of enzyme act with 37 celcius)

    The calculation is followed formular below:

        X = molar of DNA(t) / unit activity(u)
          = {nt * wt / (lt * A)} / {nu / (lu * A)}
          = nt * wt * lu / (nu * lt)
        
        n* - the number of sites of
        w* - the weight of
        l* - the size of
        A  - molecular weight of base pair

    Args:
        n - the number of sites in DNA
        size - the size of DNA in bp
        weight - the weight of DNA in [ug]
        enzyme - the instance of enzyme or path of

    Return:
        units (float) - the units required to cut all restriction sites in DNA
    """
    return sites * weight * enzyme.substrate.size / \
        float(enzyme.substrate.sites * size)

# --- unittest
import unittest
class TestCase(unittest.TestCase):
    def test_convert_weight_to_molar(self):
        mw = 100
        weight = 50
        molar = convert_weight_to_molar(mw, weight)
        self.assertEquals(molar, 0.5)
    def test_calculate_molecular_weight(self):
        size = 100
        mw = calculate_molecular_weight(size)
        self.assertEquals(mw, size * BASE_PAIR_MOLECULAR_WEIGHT)
    def test_calculate_site_molar(self):
        n = 1
        weight = 100
        size = 100
        mw = calculate_molecular_weight(size)
        molar = convert_weight_to_molar(mw, weight)
        site_molar = calculate_site_molar(n, weight, size)
        self.assertEquals(site_molar, n * molar)
    def test_calculate_unit_activity(self):
        import enzyme
        # EcoR I(self): 5 sites in lambda DNA(48,502)
        site_molar = calculate_site_molar(5, 1, 48502)
        unit_activity = calculate_unit_activity(enzyme.EcoRI)
        self.assertEquals(unit_activity, site_molar)
    def test_calculate_unit_required(self):
        import enzyme
        n = 1
        weight = 100
        size = 100
        site_molar = calculate_site_molar(n, weight, size)
        unit_activity = calculate_unit_activity(enzyme.EcoRI)
        unit_required = calculate_unit_required(n, weight, size, enzyme.EcoRI)
        self.assertEquals(unit_required, site_molar / unit_activity)

if __name__ == '__main__':
    unittest.main()
