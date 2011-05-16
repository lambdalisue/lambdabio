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

from calculator import calculate_required_weights

def _generate_protocol_rst(size_vector, size_insert, weight_vector,
        weight_insert):

    print "***********************************"
    print " Ligation Protocols"
    print "***********************************"
    print
    print "Information"
    print "===================="
    print "Vector DNA size: %d [bp]" % size_vector
    print "Insert DNA size: %d [bp]" % size_insert
    print "Required Vector DNA weight: %f [ng]" % weight_vector
    print "Required Insert DNA weight: %f [ng]" % weight_insert
    print
    print "Material"
    print "===================="
    print "*   Purified, linearized Vector (likely in DW or EB):\tvolume adjust to %f [ng]" % weight_vector
    print "*   Purified, linearized Insert (likely in DW or EB):\tvolume adjust to %f [ng]" % weight_insert
    print "*   TAKARA DNA Ligation Kit <Mighty Mix>:\t\tvolume same as Vector and Insert DNA mix"
    print
    print "Procedure"
    print "===================="
    print "1.  Cool down PCR matchine to 16 [celsius]."
    print "2.  Mix purified DNAs in 500 [ul] Tube."
    print "3.  Add appropriate volume (usually the same volume as DNA mix) of Mighty Mix."
    print "4.  Incubate 30 [min] at 16 [celcius] in PCR cool downed."
    print "    .. NOTE:: In harry, use 5 [min] at 25 [celsius] for incubation."
    print

def generate_protocol(size_vector, size_insert, format='rst'):
    """Generate protocol for Ligation of Vector and Insert

    A protocol generated is assumed to use TAKARA DNA Ligation
    Kit <Mighty Mix>. 
    See http://catalog.takara-bio.co.jp/product/basic_info.asp?unitid=U100004426
    for more detail.

    Args:
        size_vector - the size of Vector DNA in bp
        size_insert - the size of Insert DNA in bp
    """
    FORMAT_TABLE = {
        'rst': _generate_protocol_rst,
    }
    weights = calculate_required_weights(size_vector, size_insert)
    FORMAT_TABLE[format](size_vector, size_insert, *weights)
    

def main():
    def _to_num(x):
        try:
            return float(x)
        except ValueError:
            return None
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-v', '--vector', dest='vector', default=None, type='int',
            help="the size of Vector in [bp] for ligation.")
    parser.add_option('-i', '--insert', dest='insert', default=None, type='int',
            help="the size of Insert in [bp] for ligation.")
    parser.add_option('-f', '--format', dest='format', default='rst',
            help="the format of protocol. currentry support 'rst' only.")
    opts, args = parser.parse_args()

    while opts.vector is None:
        opts.vector = raw_input("Please input the size of Vector in [bp]> ")
        opts.vector = _to_num(opts.vector)
    while opts.insert is None:
        opts.insert = raw_input("Please input the size of Insert in [bp]> ")
        opts.insert = _to_num(opts.insert)

    generate_protocol(opts.vector, opts.insert, opts.format)

if __name__ == '__main__':
    main()
