# -*- coding: utf-8 -*-
# Entry point: python2 run_legacy.py fixtures/visits.json
import json
import sys

import billing


def main():
    path = sys.argv[1]
    visits = json.load(open(path))
    results = billing.compute_all(visits)
    for vid in sorted(results.keys()):
        r = results[vid]
        print "%s %s subtotal=%d tax=%d total=%d owes=%d" % (
            vid, r['invoice_no'], r['subtotal'], r['tax'], r['total'], r['patient_owes'])


if __name__ == '__main__':
    main()
