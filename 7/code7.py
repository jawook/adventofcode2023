
# --------------------------
# This code is autogenerated
data = 0
while data not in [1, 2]:
    data = int(input('Which data set do you want to use? 1 = Test, 2 = Input '))
if data == 1:
    fn = 'test'+str(7)+'.txt'
elif data == 2:
    fn = 'input'+str(7)+'.txt'
f = open(fn, 'r')
raw = [j for j in f.read().splitlines()]
# --------------------------

#%% Split the bids and the hands

inp = {}

for r, ra in enumerate(raw):
    splts = ra.split(' ')
    inp[r] = {'hand': splts[0], 'bid': splts[1]}
    
# convert to dataframe
import pandas as pd
dfInp = pd.DataFrame(inp).transpose()

#%% Abandoning regex. Create a function to provide character counts in a hand.

def countChars(string):
    freq = {}
    for char in string:
        freq[char] = freq.get(char, 0) + 1
    return freq
    
#%% Create a function to categorize items based on the char counts

def catHands(countDict):
    numPairs = list(countDict.values()).count(2)
    numTrips = list(countDict.values()).count(3)
    numQuads = list(countDict.values()).count(4)
    numQuins = list(countDict.values()).count(5)
    if numQuins >= 1:
        return 7 #five of a kind
    elif numQuads >= 1:
        return 6 #four of a kind
    elif (numTrips == 1) and (numPairs == 1):
        return 5
    elif numTrips == 1:
        return 4
    elif numPairs == 2:
        return 3
    elif numPairs == 1:
        return 2
    else:
        return 1
    
#%% Create a handcount dict and a hand cat for each hand
dfInp['handCount'] = dfInp['hand'].apply(countChars)
dfInp['handCat'] = dfInp['handCount'].apply(catHands)
    
#%% Create an entry for each character for ranking purposes

def cardRank(hand, pos, rd):
    # print(hand)
    return rd[hand[pos]]

rankDict = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, 
            '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}

for j in range(1, 6):
    dfInp[str(j)] = dfInp.apply(lambda row: cardRank(row['hand'], j-1, rankDict), axis=1)
    
#%% Sort the data frame by handcat, then by sequential order

dfInp = dfInp.sort_values(by=['handCat', '1', '2', '3', '4', '5'], ascending=True)
dfInp['rank'] = range(1, len(dfInp) + 1)
dfInp['bid'] = dfInp['bid'].astype(int)
dfInp['val'] = dfInp['rank'] * dfInp['bid']

#%% Part 1 Answer

print('Part 1 Answer: ' + str(sum(dfInp['val'])))

#%% Part 2 - recreate a function for revised hand types

# THIS RANKING DOESN'T WORK FOR CASES OF MULTIPLE J's.  Need to count Js and 
# develop an approach that adjusts as needed.

def catHands2(countDict):
    numJs = countDict.get('J', 0)
    numPairs = list(countDict.values()).count(2)
    numTrips = list(countDict.values()).count(3)
    numQuads = list(countDict.values()).count(4)
    numQuins = list(countDict.values()).count(5)
    if numQuins >= 1:
        return 7 #five of a kind
    elif numQuads >= 1:
        if numJs == 1 or numJs == 4:
            return 7 #converts to quints
        else: #since there is a quad, this must mean that there is 0 jacks, this stays quads
            return 6
    elif (numTrips == 1) and (numPairs == 1): #there is either 3, 2 or 0 Js
        if numJs == 0: #stays full house
            return 5
        else: #otherwise there is 2 or 3 jacks and it converts quints
            return 7
    elif numTrips == 1: #there is either, 3, 2, 1 or 0 Js
        if numJs == 1: #converts to quads
            return 6
        elif numJs == 2: #converts to quints
            return 7
        elif numJs == 3: #converts to quads
            return 6
        else: #remains trips
            return 4
    elif numPairs == 2: #there is either 0, 1 or 2 Js
        if numJs == 1: #converts to FH
            return 5
        if numJs == 2: #converts to quads
            return 6
        else: #stays 2 pairs
            return 3
    elif numPairs == 1: #there is either 0, 1, 2 or 3 Js
        if numJs == 1: #converts to trips with the pair
            return 4
        elif numJs == 2: #js are the pair, there are no other pairs so it must flip to trips with a single card
            return 4
        elif numJs == 3: #js are all non-pair, convert to quints
            return 7
        else: #stay one pair
            return 2
    else:
        if numJs == 0:
            return 1 #stay high card
        elif numJs == 1:
            return 2 #converts to one pair

dfInp.sort_index(inplace=True)    
dfInp['newHandCat'] = dfInp['handCount'].apply(catHands2)

rankDict2 = {'A': 13, 'K': 12, 'Q': 11, 'J': 1, 'T': 10, '9': 9, 
            '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

for j in range(1, 6):
    dfInp['n'+str(j)] = dfInp.apply(lambda row: cardRank(row['hand'], j-1, rankDict2),
                                    axis=1)
    
#%% Sort the data frame by handcat, then by sequential order

dfInp = dfInp.sort_values(by=['newHandCat', 'n1', 'n2', 'n3', 'n4', 'n5'], ascending=True)
dfInp['nRank'] = range(1, len(dfInp) + 1)
dfInp['nVal'] = dfInp['nRank'] * dfInp['bid']

#%% Part 2 Answer

print('Part 2 Answer: ' + str(sum(dfInp['nVal'])))