import numpy as np
import train_net

# text="abcdefghijklmnopqrstuvwxyz"
with open("alice.txt", "r") as f:
    text = f.read()


symbols=sorted(list(set(text)))
ndims=len(symbols)

net=train_net.createModel(ndims)

net.load_weights("net.weights.h5")

new_text=""+symbols[0]

out=train_net.categorize(symbols[0], symbols)
for i in range(50):
    last_out=out
    out=net.predict(np.array([last_out]))[0]
    symbol = train_net.decode(out, symbols)
    out=train_net.categorize(symbol, symbols)
    new_text+=symbol

print(new_text)

