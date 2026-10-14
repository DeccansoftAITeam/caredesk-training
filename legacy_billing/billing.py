# -*- coding: utf-8 -*-
# Legacy invoice calculator (Python 2.7).
import config
import rates

INVOICE_COUNTER = 0
LAST_ERROR = None


def next_invoice_no():
    global INVOICE_COUNTER
    INVOICE_COUNTER = INVOICE_COUNTER + 1
    return "INV-%05d" % INVOICE_COUNTER


def line_totals(items):
    """Return list of (code, qty, line_cents, exempt_flag)."""
    out = []
    for item in items:
        code = item['code']
        qty = item['qty']
        cents = rates.rate_for(code) * qty
        out.append((code, qty, cents, rates.is_exempt(code)))
    return out


def compute_invoice(visit):
    global LAST_ERROR
    try:
        lines = line_totals(visit['items'])
    except KeyError, e:
        LAST_ERROR = unicode(e)
        if config.DEBUG:
            print "billing error: %s" % LAST_ERROR
        return None

    subtotal = 0
    exempt_subtotal = 0
    for code, qty, cents, exempt in lines:
        subtotal = subtotal + cents
        if exempt:
            exempt_subtotal = exempt_subtotal + cents

    # Python 2 integer division: both operands are int, result truncates.
    discount_pct = visit.get('discount_pct', 0)
    discount = subtotal * discount_pct / 100
    exempt_discount = exempt_subtotal * discount_pct / 100

    taxable = (subtotal - discount) - (exempt_subtotal - exempt_discount)
    tax = taxable * config.TAX_PERCENT / 100
    total = subtotal - discount + tax

    owes = total
    if visit.get('insured'):
        owes = total * (100 - config.INSURANCE_COVERAGE_PERCENT) / 100

    # Average line value (integer division again).
    avg_line = subtotal / len(lines)

    result = {
        'invoice_no': next_invoice_no(),
        'visit_id': visit['visit_id'],
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'patient_owes': owes,
        'avg_line': avg_line,
    }
    if config.DEBUG:
        print "computed %s total=%d" % (result['invoice_no'], total)
    return result


def compute_all(visits):
    results = {}
    for v in visits:
        r = compute_invoice(v)
        if r is not None:
            results[v['visit_id']] = r
    for vid, r in results.iteritems():
        r['label'] = u"%s / %s" % (vid, r['invoice_no'])
    return results
