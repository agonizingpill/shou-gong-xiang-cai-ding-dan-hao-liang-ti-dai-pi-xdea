from hashlib import sha256
import json
from math import ceil
from random import Random

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

def historic():
    rng = Random(1095)
    for _ in range(360):
        grams = rng.randint(80,1200)
        moisture = rng.uniform(4,20)
        rack,scent = rng.randint(0,1),rng.randint(0,1)
        loss = grams*(0.03+.011*moisture+.012*rack+.018*scent)
        loss += max(0.0,moisture-13)*2.2+rng.uniform(-4,4)
        yield grams,moisture,rack,scent,max(0.0,loss)

def calculate(data):
    records = np.asarray(list(historic()))
    train,check = records[:280],records[280:]
    model = HistGradientBoostingRegressor(max_iter=120,max_bins=48,max_leaf_nodes=15,
        min_samples_leaf=9,l2_regularization=0.1,early_stopping=False,random_state=1095).fit(train[:,:4],train[:,4])
    estimated = float(model.predict([[data['target'],data['moisture'],int(data['dryer']=='rack-b'),int(data['scent']=='PAPER')]])[0])
    loss = round(max(0.0,estimated),3)
    return {'algorithm':'HistGradientBoostingRegressor','training':len(train),'holdout':len(check),
            'trees':model.n_iter_,'seed':1095,'loss_g':loss,'need_g':data['target']+ceil(max(0.0,estimated)),
            'manual_baseline_mae_g':round(mean_absolute_error(check[:,4],.15*check[:,0]),3),
            'holdout_mae_g':round(mean_absolute_error(check[:,4],model.predict(check[:,:4])),3),
            'input_hash':sha256(json.dumps([data,records.tolist()],sort_keys=True).encode()).hexdigest()}
