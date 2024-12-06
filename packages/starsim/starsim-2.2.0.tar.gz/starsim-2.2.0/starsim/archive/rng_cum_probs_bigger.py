import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.util import hash_pandas_object
import hashlib
import sciris as sc
from pathlib import Path

# PARAMETERS
n = 12 # Number of nodes
n_sources = 2 # Number of sources (seed infections)
reps = 100_000
edge_prob = 0.5 # Edge probability
trans_prob = 0.4
seed = 3

lbl = f'n{n}_s{n_sources}_r{reps}_ep{edge_prob}_tp{trans_prob}_seed{seed}'
figdir = os.path.join('figs', 'TransExploration', lbl)
Path(figdir).mkdir(parents=True, exist_ok=True)

sc.options(dpi=200)

def hash(df):
    #return int(hashlib.sha256(hash_pandas_object(df, index=True).values).hexdigest(), 16)
    return hashlib.sha256(hash_pandas_object(df, index=True).values).hexdigest()[:6]

def random(G):
    src = nx.get_node_attributes(G, 'infected')
    infected = []
    tx = []

    # Randomize in case a node is infected multiple times
    el = list(G.edges())
    np.random.shuffle(el)

    for (n1,n2) in el:
        # n1 --> n2
        if src[n1] and (not src[n2]) and (n2 not in infected) and (np.random.rand() < trans_prob):
            tx.append((n1, n2))
            infected.append(n2)
        # n2 --> n1
        if src[n2] and (not src[n1]) and (n1 not in infected) and (np.random.rand() < trans_prob):
            tx.append((n2, n1))
            infected.append(n1)
    return tx


def modulo(G):
    src = nx.get_node_attributes(G, 'infected')
    infected = []
    tx = []
    r1 = np.random.rand(n)
    r2 = np.random.rand(n)
    el = list(G.edges())
    np.random.shuffle(el)
    for (n1,n2) in el:
        # n1 --> n2
        if (src[n1]) and (not src[n2]) and (n2 not in infected) and (((r1[n1]+r2[n2])%1) < trans_prob):
            tx.append((n1, n2))
            infected.append(n2)
        # n2 --> n1
        if (src[n2]) and (not src[n1]) and (n1 not in infected) and (((r1[n2]+r2[n1])%1) < trans_prob):
            tx.append((n2, n1))
            infected.append(n1)
    return tx


def roulette(G):
    src = nx.get_node_attributes(G, 'infected')
    tx = []
    for n2 in G.nodes():
        # All nodes --> n2
        if not src[n2]:
            srcs = [n for n in G.neighbors(n2) if src[n]] #[src[n] for n in G.neighbors(n2)] # Count infected neighbors
            cnt = len(srcs)
            if np.random.rand() < 1-(1-trans_prob)**cnt:
                n1 = np.random.choice(srcs)
                tx.append((n1, n2))
    return tx
 

def transmit(G, trans_fn):
    # Align transmissions from tx_in if provided
    txs = {}
    counts = {}
 
    for _ in np.arange(reps):
        txl = trans_fn(G)
        tx = pd.DataFrame(txl, columns=['src', 'dst']).sort_values(['src', 'dst']).reset_index(drop=True)
        
        h = hash(tx)

        if h not in txs:
            txs[h] = tx

        counts[h] = counts.get(h, 0) + 1

    df = pd.DataFrame(counts.values(), index=pd.Index(counts.keys(), name='Hash'), columns=['Counts'])
    return txs, df

T = sc.timer()

# Build the graph
G = nx.random_graphs.erdos_renyi_graph(n=n, p=edge_prob, seed=seed)

# Seed infections
infected = {i:False for i in range(n)}
sources = np.random.choice(a=range(n), size=n_sources, replace=False)
for source in sources:
    infected[source] = True
nx.set_node_attributes(G, infected, 'infected')
 
# Do transmissions via each method in parallel
results = sc.parallelize(transmit, iterkwargs=[{'trans_fn':random}, {'trans_fn':modulo}, {'trans_fn':roulette}], kwargs={'G':G}, die=True, serial=False)
tx, cnt = zip(*results)

df = pd.concat(cnt, axis=1) \
    .fillna(0) \
    .astype(int)
df.columns = ['Random', 'Modulo', 'Roulette']

# Manipulate results
df.reset_index(inplace=True)
dfm = df.melt(id_vars='Hash', var_name='Method', value_name='Count')

# Alternate plotting
keys = ['Random', 'Modulo', 'Roulette']
colors = {'Random':'k', 'Modulo':'slategray', 'Roulette':'red'}
z = sc.objdict()
for k in keys:
    z[k] = dfm[dfm.Method==k].Count.values

order = np.argsort(z.Random)

fig = plt.figure()
for k in keys:
    plt.plot(z[k][order], 'o-', alpha=0.7, label=k, c=colors[k])
plt.legend()

# Plot
# g = sns.barplot(data=dfm, x='Hash', y='Count', hue='Method')
# plt.xticks(rotation=90)
# g.figure.tight_layout()
# sc.savefig(os.path.join(figdir, 'Bar.png'), g.figure)

# txc = tx[0].copy()
# for i in range(1, len(tx)):
#     txc.update(tx[i])
# for h, v in txc.items():
#     print(f'\nUnique transmission tree #{h}')
#     print(v)
# sc.savejson(os.path.join(figdir, 'Transmissions.json'), txc)

f = plt.figure(figsize=(12,8))
pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
ec = nx.draw_networkx_edges(G, pos, alpha=0.2)
colors = ['red' if infected else 'blue' for infected in nx.get_node_attributes(G, 'infected').values()]
nc = nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color=colors, node_size=100)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(G, pos)
sc.savefig(os.path.join(figdir, 'Network.png'), f)

T.toc()
plt.show()