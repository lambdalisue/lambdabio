#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""The short module explanation.

the long module explanation.
the long module explanation.

Methods:
    foobar - the explanation of the method.

Data:
    hogehoge - the explanation of the data.


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

#
# Recovery Tables below is for Promega Wizard SV Gel and PCR Clean-Up system
# Ref: http://www.promega.co.jp/Cre_Html.php?pGMPID=0504003
#
RECOVERY_ON_SIZE_TABLE = (
    (55,    0.26),
    (70,    0.39),
    (85,    0.55),
    (100,   0.84),
    (500,   0.89),
    (1000,  0.92),
    (3199,  0.95),
    (9416,  0.95),
    (23130, 0.47),
)
RECOVERY_ON_VOLUME_TABLE = (
    (10,    0.35),
    (15,    0.98),
    (25,    0.98),
    (50,    1.00),
    (75,    1.00),
    (100,   1.00),
)

def _find(value, table):
    if value < table[0][0]:
        return table[0][1]
    elif value > table[-1][0]:
        return table[-1][1]
    else:
        for i in xrange(len(table)-1):
            lhs = table[i][0]
            rhs = table[i+1][0]
            if lhs <= value <= rhs:
                if value - lhs < rhs - value:
                    return table[i][1]
                else:
                    return table[i+1][1]

def find_recovery_on_size(size):
    """Find recovery depend on size"""
    return _find(size, RECOVERY_ON_SIZE_TABLE)
def find_recovery_on_volume(volume):
    """Find recovery depend on volume"""
    return _find(volume, RECOVERY_ON_VOLUME_TABLE)

def calculate_prep_weight(weight, size):
    """Calculate prep weight before Gel Extraction

    Args:
        weight - the desired weight of DNA in [g]
        size - the size of DNA in bp

    Return:
        a prep weight of DNA in [g] (float)
    """
    r = find_recovery_on_size(size)
    return weight / r

def calculate_last_weight(weight, size, volume=None):
    """Calculate last weight after Gel Extraction

    Args:
        weight - the weight of DNA in [g]
        size - the size of DNA in bp
        volume - the volume of Gel Extraction Mix solution

    Return:
        a last weight of DNA in [g] (float)
    """
    size_r = find_recovery_on_size(size)
    volume_r = find_recovery_on_volume(volume)
    return weight * size_r * volume_r
