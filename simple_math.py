#def fibonacci(n, fib_catch = {1:1, 0:0}):
#    if n not in fib_catch:
#        fib_catch[n] = fibonacci(n - 1, fib_catch) + fibonacci(n - 2, fib_catch)
#    return fib_catch[n]
import sys

from functools import lru_cache

sys.setrecursionlimit(5000)

def fibonacci_s(n):
    """
    >>> fibonacci_s(15)
    610
    >>> fibonacci_s(25)
    75025
    >>> fibonacci_s(35)
    9227465
    """
    n1, n2 = 0, 1
    result = 1
    for _ in range(2, n):
        n1, n2 = n2, result
        result =  n1 + n2
    return result

def factorial_s(n):
    """
    >>> factorial_s(5)
    120
    >>> factorial_s(15)
    1307674368000
    >>> factorial_s(25)
    15511210043330985984000000
    """
    if n != int(n):
        raise ValueError("factorial() only accepts integral values")
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    result = 1
    for _ in range(1, n+1):
        result *= _
    return result

@lru_cache(maxsize=None, typed=False)
def ackermann(m, n):
    """A(0,n) = n+1, A(m,0) = A(m-1,1), A(m,n) = A(m-1, A(m, n- 1))
    >>> ackermann(3, 4)
    125
    >>> ackermann(3, 3)
    61
    """
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m-1, 1)
    else:
        return ackermann(m-1, ackermann(m, n-1))


#def ackermann_catch(m, n, acker_catch={(1, 1) :3, (0, 0): 1, (0,1):2, (1,0):2}):
#    """A(0,n) = n+1, A(m,0) = A(m-1,1), A(m,n) = A(m-1, A(m, n- 1))
#    >>> ackermann_catch(3, 4)
#    125
#    >>> ackermann_catch(4, 1)
#    65533
#    """
#    print(acker_catch)
#    if (m, n) in acker_catch:
#        return acker_catch[(m, n)]
#    if m == 0:
#        acker_catch[(m, n)]  = n + 1
#        return acker_catch[(m, n)]
#    if n == 0:
#        acker_catch[(m, n)]  = ackermann_catch(m-1, 1, acker_catch)
#        return acker_catch[(m, n)]
#    else:
#        acker_catch[(m, n)] = ackermann_catch(m-1, ackermann_catch(m, n-1, acker_catch), acker_catch)
#        return acker_catch[(m, n)]
#
#def ackermann_s(m, n):
#    """A(0,n) = n+1, A(m,0) = A(m-1,1), A(m,n) = A(m-1, A(m, n- 1))
#    >>> ackermann(3, 4)
#    125
#    >>> ackermann(4, 1)
#    65533
#    """
#    stack = [m]
#    while stack:
#        m = stack.pop()
#        if m == 0:
#            n+=m+1
#        elif n == 0:
#            n+=1
#            stack.append(m-1)
#        else:
#            stack.append(m-1)
#            stack.append(m+1)
#            n -= 1
#    return n
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

