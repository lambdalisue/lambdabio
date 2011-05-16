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

class Singleton(object):
    """Singleton Mixin Class

    Inherit this class and make the subclass Singleton.

    Usage:
        >>> class A(object):
        ...     pass
        >>> class B(Singleton):
        ...     pass
        >>> a1 = A()
        >>> a2 = A()
        >>> b1 = B()    # Create instance as usual
        >>> b2 = B()
        >>> a1 == a2    # a1, a2 are not singleton
        False
        >>> b1 == b2    # b1, b2 are singleton
        True

    Reference:
        http://d.hatena.ne.jp/BetaNews/20090607/1244358178
    """
    def __new__(cls, *args, **kwargs):
        # Store instance on cls._instance_dict with cls hash
        key = str(hash(cls))
        if not hasattr(cls, '_instance_dict'):
            cls._instance_dict = {}
        if key not in cls._instance_dict:
            cls._instance_dict[key] = \
                super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance_dict[key]

class Attrdict(dict):
    """Attribute accessible dictionary class
    
    Usage:
        >>> attrdict = Attrdict(alice='in the wonderland')
        >>> attrdict.alice
        'in the wonderland'
        >>> attrdict['hello'] = 'world'
        >>> attrdict['hello']
        'world'
        >>> attrdict.hello
        'world'
        >>> attrdict.hello = 'madam'
        >>> attrdict.hello
        'madam'
        >>> attrdict.foobar = 'hogehoge'
        >>> attrdict.foobar
        'hogehoge'

    Reference:
        http://code.activestate.com/recipes/389916-example-setattr-getattr-overloading/
    """
    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        if key in self:
            super(Attrdict, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)

class RestrictionEnzymeBase(Singleton):
    """Restriction Enzyme Base class"""
    def __str__(self):
        return self._name

class EcoRI(RestrictionEnzymeBase):
    # Ref: http://catalog.takara-bio.co.jp/product/basic_info.asp?catcd=B1000359&subcatcd=B1000364&unitid=U100003069
    _name = 'EcoR I'
    site = r"G'AATTC"
    substrate = Attrdict(name='lambda', size=48502, sites=5)
    temperature = 37
    heat_inactivate = Attrdict(temperature=60, time=15)
    concentration = 14
    buffer = 'TAKARA Universal Buffer H'
class PstI(RestrictionEnzymeBase):
    # Ref: http://catalog.takara-bio.co.jp/product/basic_info.asp?catcd=B1000359&subcatcd=B1000367&unitid=U100003104
    _name = 'Pst I'
    site = r"CTGCA'G"
    substrate = Attrdict(name='lambda', size=48502, sites=28)
    temperature = 37
    heat_inactivate = Attrdict(temperature=60, time=15)
    concentration = 15
    buffer = 'TAKARA Universal Buffer H'
class SpeI(RestrictionEnzymeBase):
    # Ref: http://catalog.takara-bio.co.jp/product/basic_info.asp?catcd=B1000359&subcatcd=B1000368&unitid=U100003114
    _name = 'Spe I'
    site = r"A'CTAGT"
    substrate = Attrdict(name='Adenovirus-2', size=35937, sites=3)
    temperature = 37
    heat_inactivate = Attrdict(temperature=60, time=15)
    concentration = 8
    buffer = 'TAKARA Universal Buffer M'
class XbaI(RestrictionEnzymeBase):
    # Ref: http://catalog.takara-bio.co.jp/product/basic_info.asp?catcd=B1000359&subcatcd=B1000369&unitid=U100003122
    _name = 'Xba I'
    site = r"T'CTAGA"
    substrate = Attrdict(name='lambda', size=48502, sites=1)
    temperature = 37
    heat_inactivate = Attrdict(temperature=60, time=15)
    concentration = 14
    buffer = 'TAKARA Universal Buffer M + 0.01% BSA'

AVARIABLE_ENZYME_LIST = (
    ('EcoRI',   EcoRI),
    ('PstI',    PstI),
    ('SpeI',    SpeI),
    ('XbaI',    XbaI),
)
"""Avariable enzyme list"""

def double_digestion(enzyme1, enzyme2):
    """Return recommends buffer for double digestion.

    Args:
        enzyme1 - the instance of Enzyme
        enzyme2 - the instance of Enzyme

    Return:
        a name of recommends buffer (string)
    """
    RECOMMEND_TABLE = (
        (EcoRI, PstI, 'TAKARA Universal Buffer H', True, None),
        (EcoRI, SpeI, 'TAKARA Universal Buffer H', True, None),
        (EcoRI, XbaI, 'TAKARA Universal Buffer M', False,
            "Double digestion of EcoR I and Xba I is not recommends."
            " It will exhibits significant star activity for EcoR I"),
        (PstI, SpeI, 'TAKARA Universal Buffer H', True, None),
        (PstI, XbaI, 'TAKARA Universal Buffer M', False,
            "Double digestion of Pst I and Xba I is not recommends."
            " It will exhibits star activity for Pst I."),
        (SpeI, XbaI, 'TAKARA Universal Buffer M', True, None),
    )
    for recommend in RECOMMEND_TABLE:
        enzymeset = frozenset(recommend[0:2])
        if enzymeset == frozenset((enzyme1.__class__,enzyme2.__class__)):
            return recommend[2:]
    raise KeyError("No avariable combination of %s and %s is found." \
            % (enzyme1, enzyme2))

import unittest
class TestCase(unittest.TestCase):
    def test_restriction_enzymes(self):
        e1 = EcoRI()
        e2 = EcoRI()
        self.assertEquals(e1, e2)
        e1 = PstI()
        e2 = PstI()
        self.assertEquals(e1, e2)
        e1 = SpeI()
        e2 = SpeI()
        self.assertEquals(e1, e2)
        e1 = XbaI()
        e2 = XbaI()
        self.assertEquals(e1, e2)
    def test_EcoRI(self):
        e = EcoRI()
        self.assertEquals(str(e), 'EcoR I')
        self.assertEquals(e.site, r"G'AATTC")
        self.assertEquals(e.substrate.name, 'lambda')
        self.assertEquals(e.substrate.size, 48502)
        self.assertEquals(e.substrate.sites, 5)
        self.assertEquals(e.temperature, 37)
        self.assertEquals(e.heat_inactivate.temperature, 60)
        self.assertEquals(e.heat_inactivate.time, 15)
        self.assertEquals(e.buffer, 'TAKARA Universal Buffer H')
    def test_PstI(self):
        e = PstI()
        self.assertEquals(str(e), 'Pst I')
        self.assertEquals(e.site, r"CTGCA'G")
        self.assertEquals(e.substrate.name, 'lambda')
        self.assertEquals(e.substrate.size, 48502)
        self.assertEquals(e.substrate.sites, 28)
        self.assertEquals(e.temperature, 37)
        self.assertEquals(e.heat_inactivate.temperature, 60)
        self.assertEquals(e.heat_inactivate.time, 15)
        self.assertEquals(e.buffer, 'TAKARA Universal Buffer H')
    def test_SpeI(self):
        e = SpeI()
        self.assertEquals(str(e), 'Spe I')
        self.assertEquals(e.site, r"A'CTAGT")
        self.assertEquals(e.substrate.name, 'Adenovirus-2')
        self.assertEquals(e.substrate.size, 35937)
        self.assertEquals(e.substrate.sites, 3)
        self.assertEquals(e.temperature, 37)
        self.assertEquals(e.heat_inactivate.temperature, 60)
        self.assertEquals(e.heat_inactivate.time, 15)
        self.assertEquals(e.buffer, 'TAKARA Universal Buffer M')
    def test_XbaI(self):
        e = XbaI()
        self.assertEquals(str(e), 'Xba I')
        self.assertEquals(e.site, r"T'CTAGA")
        self.assertEquals(e.substrate.name, 'lambda')
        self.assertEquals(e.substrate.size, 48502)
        self.assertEquals(e.substrate.sites, 1)
        self.assertEquals(e.temperature, 37)
        self.assertEquals(e.heat_inactivate.temperature, 60)
        self.assertEquals(e.heat_inactivate.time, 15)
        self.assertEquals(e.buffer, 'TAKARA Universal Buffer M + 0.01% BSA')
    def test_double_digestion(self):
        COMBINATION_TABLE = (
            (EcoRI(), PstI(), 'TAKARA Universal Buffer H'),
            (EcoRI(), SpeI(), 'TAKARA Universal Buffer H'),
            (EcoRI(), XbaI(), 'TAKARA Universal Buffer M'),
            (PstI(), SpeI(), 'TAKARA Universal Buffer H'),
            (PstI(), XbaI(), 'TAKARA Universal Buffer M'),
            (SpeI(), XbaI(), 'TAKARA Universal Buffer M'),
        )
        for e1, e2, expected in COMBINATION_TABLE:
            buffer, recommend, warning = double_digestion(e1, e2)
            #print "%s x %s: %s" % (e1, e2, buffer)
            self.assertEquals(buffer, expected)


if __name__ == '__main__':
    unittest.main()
