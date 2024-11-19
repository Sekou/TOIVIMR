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


def randchoice(probs):
    r=np.random.random()*sum(probs)
    s=0
    for i in range(len(probs)):
        s+=probs[i]
        if s>r: return i
    return len(probs)



out=train_net.categorize(symbols[0], symbols)
for i in range(50):
    last_out=out
    # out=net.predict(np.array([last_out]))[0]
    out=net.predict(np.array([[last_out]]))[0]
    ind = randchoice(out)
    v=np.zeros(len(out))
    v[ind]=1
    symbol = train_net.decode(v, symbols)
    out=train_net.categorize(symbol, symbols)
    new_text+=symbol

print(new_text)

