# -*- coding: utf-8 -*-
# Legacy billing configuration. All amounts are integer cents.
# Python 2.7 -- do not run under Python 3.

RATES = {
    'CONSULT': 5000,
    'XRAY': 12000,
    'LABPANEL': 3550,
    'VACCINE': 2799,
    'BANDAGE': 325,
}

# Items that carry no sales tax.
TAX_EXEMPT = ['VACCINE', 'LABPANEL']

TAX_PERCENT = 7
INSURANCE_COVERAGE_PERCENT = 80

DEBUG = True
