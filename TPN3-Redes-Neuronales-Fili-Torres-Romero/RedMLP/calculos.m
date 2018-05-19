e = 0.3
a = tanh(-0.072 * 1 + 0.84 * 1 + -0.63 * 1 + 0.936)
b = tanh(-0.033 * 1 + 0.738 * 1 + 0.893 * 1 + 0.37)
c = tanh(0.101 * a - 0.35 * b - 0.33)
delta = (- 1 - c ) * (1 - c)
ds = e * delta * -1
dw1 = e * delta * a
dw2 = e * delta * b
sesgo = ds + 0.33
w1 = dw1 + 0.101
w2 = dw2 - 0.35

% #Todo bien hasta aca
delta = delta  * 0.101* (1 - a)
ds = e * delta * -1
dw1 = e * delta
dw2 = e * delta
dw3 = e * delta
sesgo = ds - 0.9397
w1 = dw1 - 0.072
w2 = dw2  + 0.84
w3 = dw3 -0.6392
