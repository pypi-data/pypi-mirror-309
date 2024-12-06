from wcwidth import wcswidth

def short(lst1):
    ll = lst1[0]
    for x in lst1:
        if wcswidth(x) < wcswidth(ll):
            ll = x
    return ll

def long(lst1):
    ll = lst1[0]
    for x in lst1:
        if wcswidth(x) > wcswidth(ll):
            ll = x
    return ll

def numlist(lst1):
    numspc = ' '*len(str(len(lst1)) + '. ')
    lst2 = []
    for x in range(0, len(lst1)):
        lst2.append(str(x + 1) + '. ' + numspc[len(str(x + 1) + '. '):] + lst1[x])
    return lst2

def table(lst1):
    spc = wcswidth(long(lst1) + ' ')
    lst2 = ['-'*spc]
    for x in lst1:
        lst2.append(x + (' '*spc)[wcswidth(x):] + '|')
    lst2.append('-'*spc)
    return lst2
