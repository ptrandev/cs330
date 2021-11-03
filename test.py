import numpy as np 
from random import randint
from collections import Counter

redeem = [0, 1] # 0 = don't redeem, 1 = redeem

redemptions = [] # keep track of how many people redeem in each trial

# run 10000 trials
for _ in range(10000):
  trial = [] # array of 12 binary values

  # 12 students make decision
  for _ in range(12):
    # 0 if student redeems, 1 if student doesn't redeem
    isRedeemed = np.random.choice(redeem, p=[0.15, 0.85])

    trial.append(isRedeemed) # append result of decision to array

  redemptions.append(sum(trial)) # sum results of trial and add to redemptions

results = Counter(redemptions) # find occurrences of # of redemptions

print(results)
print((results[11] + results[12]) / len(redemptions))
print(results[11] / len(redemptions))
print(results[12] / len(redemptions))