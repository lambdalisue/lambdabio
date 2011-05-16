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

import sys
from calculator import calculate_unit_required
from enzyme import AVARIABLE_ENZYME_LIST, double_digestion

def _generate_single_digestion_protocol_rst(sites, size, weight, enzyme,
        required_unit):
    print "**************************************"
    print " Single Restriction Digest Protocol"
    print "**************************************"
    print
    print "Information"
    print "================================"
    print "Unit required: %f [units]" % required_unit
    print
    print "DNA"
    print "--------------------------------"
    print "Size: %d [bp]" % size
    print "Weight: %f [ng]" % weight
    print "Sites: %d [sites]" % sites
    print
    print "Enzyme"
    print "--------------------------------"
    print "Name: %s" % enzyme
    print "Site: %s" % enzyme.site
    print "Substrate name: %s" % enzyme.substrate.name
    print "Substrate size: %d [bp]" % enzyme.substrate.size
    print "Substrate sites: %d [sites]" % enzyme.substrate.sites
    print "Temperature: %f" % enzyme.temperature
    print "Heat inactivate: %(temperature)f [celcius], %(time)f [min]" \
        % enzyme.heat_inactivate
    print "Concentration: %f [U/ul]" % enzyme.concentration
    print "Buffer: %s" % enzyme.buffer
    print
    print "Material"
    print "================================="
    print "-   10x %s:\t2 [ul]" % enzyme.buffer
    print "-   TAKARA %s:\t\t %f [ul]" % (enzyme, required_unit / float(enzyme.concentration))
    print "-   DNA:\t volume to %f [ng]" % weight
    print "-   DW:\t\t volume to 20 [ul]"
    print
    print "Procedure"
    print "================================="
    print "1.  Set PCR temperature as %f [celcius] to warm up." \
        % enzyme.temperature
    print "2.  Mix materials in PCR Tube."
    print "3.  Incubate reaction mixture at %f [celcius] at least 1 hour" \
        % enzyme.temperature
    print "4.  Heat other PCR at %f [celcius] for heat inactivate duaring incubate." \
        % enzyme.heat_inactivate.temperature
    print "5.  After incubate, move PCR tube to the PCR heated and incubate %f [min] for heat inactivate." \
        % enzyme.heat_inactivate.time
    print

def _generate_double_digestion_protocol_rst(sites, size, weight, enzyme,
        enzyme2, required_unit, required_unit2, buffer):
    # Chose more restrict condition
    temperature = max(enzyme.temperature, enzyme2.temperature)
    heat_inactivate_temperature = max((enzyme.heat_inactivate.temperature,
        enzyme2.heat_inactivate.temperature))
    heat_inactivate_time = max((enzyme.heat_inactivate.time,
        enzyme2.heat_inactivate.time))

    print "**************************************"
    print " Double Restriction Digest Protocol"
    print "**************************************"
    print
    print "Information"
    print "================================"
    print "Unit required: %f [units]" % required_unit
    print "Unit required2: %f [units]" % required_unit2
    print "Recommend buffer: %s" % buffer
    print
    print "DNA"
    print "--------------------------------"
    print "Size: %d [bp]" % size
    print "Weight: %f [ng]" % weight
    print "Sites: %d [sites]" % sites
    print
    print "Enzyme"
    print "--------------------------------"
    print "Name: %s" % enzyme
    print "Site: %s" % enzyme.site
    print "Substrate name: %s" % enzyme.substrate.name
    print "Substrate size: %d [bp]" % enzyme.substrate.size
    print "Substrate sites: %d [sites]" % enzyme.substrate.sites
    print "Temperature: %f" % enzyme.temperature
    print "Heat inactivate: %(temperature)f [celcius], %(time)f [min]" \
        % enzyme.heat_inactivate
    print "Concentration: %f [U/ul]" % enzyme.concentration
    print "Buffer: %s" % enzyme.buffer
    print
    print "Enzyme2"
    print "--------------------------------"
    print "Name: %s" % enzyme2
    print "Site: %s" % enzyme2.site
    print "Substrate name: %s" % enzyme2.substrate.name
    print "Substrate size: %d [bp]" % enzyme2.substrate.size
    print "Substrate sites: %d [sites]" % enzyme2.substrate.sites
    print "Temperature: %f" % enzyme2.temperature
    print "Heat inactivate: %(temperature)f [celcius], %(time)f [min]" \
        % enzyme2.heat_inactivate
    print "Concentration: %f [U/ul]" % enzyme2.concentration
    print "Buffer: %s" % enzyme2.buffer
    print
    print "Material"
    print "================================="
    print "-   10x %s:\t2 [ul]" % buffer
    print "-   TAKARA %s:\t\t %f [ul]" % (enzyme, required_unit / float(enzyme.concentration))
    print "-   TAKARA %s:\t\t %f [ul]" % (enzyme2, required_unit2 / float(enzyme2.concentration))
    print "-   DNA:\t volume to %f [ng]" % weight
    print "-   DW:\t\t volume to 20 [ul]"
    print
    print "Procedure"
    print "================================="
    print "1.  Set PCR temperature as %f [celcius] to warm up." \
        % temperature
    print "2.  Mix materials in PCR Tube."
    print "3.  Incubate reaction mixture at %f [celcius] at least 1 hour" \
        % temperature
    print "4.  Heat other PCR at %f [celcius] for heat inactivate duaring incubate." \
        % heat_inactivate_temperature
    print "5.  After incubate, move PCR tube to the PCR heated and incubate %f [min] for heat inactivate." \
        % heat_inactivate_time
    print

def _generate_single_digestion_protocol(sites, size, weight, enzyme, format='rst'):
    FORMAT_TABLE = {
        'rst': _generate_single_digestion_protocol_rst,
    }
    # Convert weight [ng] -> [ug]
    weight = weight / 1000.0

    # Calculate required units for enzyme
    required_unit = calculate_unit_required(sites, size, weight, enzyme)
    # assume 3-fold excess is required
    required_unit = required_unit * 3

    return FORMAT_TABLE[format](sites, size, weight, enzyme, required_unit)
def _generate_double_digestion_protocol(sites, size, weight, enzyme, enzyme2, format='rst'):
    FORMAT_TABLE = {
        'rst': _generate_double_digestion_protocol_rst,
    }
    # Convert weight [ng] -> [ug]
    weight = weight / 1000.0

    # Calculate required units for enzyme
    required_unit = calculate_unit_required(sites, size, weight, enzyme)
    # assume 3-fold excess is required
    required_unit = required_unit * 3
    
    # Calculate required units for enzyme2
    required_unit2 = calculate_unit_required(sites, size, weight, enzyme2)
    # assume 3-fold excess is required
    required_unit2 = required_unit2 * 3

    # Find the best buffer
    buffer, recommend, warning = double_digestion(enzyme, enzyme2)
    if not recommend:
        print
        print ".. WARNING::"
        print "    %s" % warning
        print
    return FORMAT_TABLE[format](sites, size, weight, enzyme, enzyme2,
            required_unit, required_unit2, buffer)

def _to_num(x):
    try:
        return float(x)
    except ValueError:
        return None
def _to_enzyme(x):
    try:
        return AVARIABLE_ENZYME_LIST[int(x)-1][1]()
    except KeyError:
        return None
    except ValueError:
        return None

def _print_enzyme_list():
    for i, (name, instance) in enumerate(AVARIABLE_ENZYME_LIST):
        sys.stdout.write("%02d. %s\t" % (i+1, name))
        if (i+1) % 5 == 0:
            print
    print

def generate_single_digestion_protocol(opts):
    # Gather required data
    while opts.size is None:
        opts.size = _to_num(raw_input("Please input the size of DNA in [bp]> "))
    while opts.sites is None:
        opts.sites = _to_num(raw_input("Please input the sites of DNA> "))
    while opts.weight is None:
        opts.weight = _to_num(raw_input("Please input the weight of DNA in [ng]> "))
    while opts.enzyme is None:
        print "Please select index of enzyme from list below:"
        _print_enzyme_list()
        opts.enzyme = _to_enzyme(raw_input("> "))
    _generate_single_digestion_protocol(
        opts.sites, opts.size, opts.weight, opts.enzyme,
    )

def generate_double_digestion_protocol(opts):
    # Gather required data
    while opts.size is None:
        opts.size = _to_num(raw_input("Please input the size of DNA in [bp]> "))
    while opts.sites is None:
        opts.sites = _to_num(raw_input("Please input the sites of DNA> "))
    while opts.weight is None:
        opts.weight = _to_num(raw_input("Please input the weight of DNA in [ng]> "))
    while opts.enzyme is None:
        print "Please select index of enzyme from list below:"
        _print_enzyme_list()
        opts.enzyme = _to_enzyme(raw_input("> "))
    while opts.enzyme2 is None:
        print "Please select index of enzyme2 from list below:"
        _print_enzyme_list()
        opts.enzyme2 = _to_enzyme(raw_input("> "))
    _generate_double_digestion_protocol(
        opts.sites, opts.size, opts.weight, opts.enzyme, opts.enzyme2,
    )

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog [options] [enzymes|single|double]
    
    - enzymes:
        print list of enzymes avariable

    - single:
        run as single digestion mode

    - double:
        run as double digestion mode
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-l', '--size', dest='size', type="int",
            help="the size of DNA in [bp]")
    parser.add_option('-s', '--sites', dest='sites', type="int",
            help="the number of sites in DNA")
    parser.add_option('-w', '--weight', dest='weight', type="float",
            help="the weight of DNA in [ng]")
    parser.add_option('-e', '--enzyme', dest='enzyme', type="int",
            help="the index of enzyme")
    parser.add_option('-f', '--enzyme2', dest='enzyme2', type="int",
            help="the index of enzyme2")
    opts, args = parser.parse_args()

    if opts.enzyme:
        opts.enzyme = _to_enzyme(opts.enzyme)
    if opts.enzyme2:
        opts.enzyme2 = _to_enzyme(opts.enzyme2)

    if len(args) == 0:
        parser.print_help()
    else:
        if args[0] == 'enzymes':
            _print_enzyme_list()
        elif args[0] == 'single':
            generate_single_digestion_protocol(opts)
        elif args[0] == 'double':
            generate_double_digestion_protocol(opts)
        else:
            raise Exception("Invalid mode flag is selected")
