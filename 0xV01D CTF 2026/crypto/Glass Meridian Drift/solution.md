# Glass Meridian Drift

## Description

A quiet RSA key was generated at noon and corrected by a tiny offset. The correction was smaller than the operator thought.

## Solution Walkthrough

In RSA we have

$$n = p\cdot q$$

The problem states that the difference between p and q is less than $2^{25}$, which means p and q are very close. Therefore I used Fermat's factorization method.

Let

$$a=\frac{p+q}{2},\qquad b=\frac{q-p}{2}$$

Then

$$n=a^2-b^2=(a-b)(a+b).$$

To factor n, find an integer a greater than $\sqrt{n}$ and check whether

$$a^2-n=b^2$$

is a perfect square. If so, the prime factors are

$$p=a-b,\qquad q=a+b.$$

Because p and q are very close, a will be very close to $\sqrt{n}$, so I rounded $\sqrt{n}$ up and succeeded, obtaining the following p and q:

$$p = 30781960399176818588848237874504350891261490762280592662378670237356982853595044454492776283649913589684358691506813$$

$$q = 30781960399176818588848237874504350891261490762280592662378670237356982853595044454492776283649913589684358702733033$$

Then I used these to solve and retrieve the flag.

## Flag

```text
0xV01D{nearby_primes_make_lattices_louder}
```
