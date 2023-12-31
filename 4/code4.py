
# --------------------------
# This code is autogenerated
data = 0
while data not in [1, 2]:
    data = int(input('Which data set do you want to use? 1 = Test, 2 = Input '))
if data == 1:
    fn = 'test'+str(4)+'.txt'
elif data == 2:
    fn = 'input'+str(4)+'.txt'
f = open(fn, 'r')
raw = [j for j in f.read().splitlines()]
# --------------------------

#%% Part 1

# Process the cards into winner set and your set
cards = {}
cNum = 1
for j in raw:
    nums = j[j.index(':') + 2:]
    nums = [i.strip() for i in nums.split('|')]
    cards[cNum] = {}
    cards[cNum]['winners'] = set(nums[0].split(' '))
    cards[cNum]['winners'].discard('')
    cards[cNum]['mine'] = set(nums[1].split(' '))
    cards[cNum]['mine'].discard('')
    cNum += 1

for j in cards:
    # get a list of all matches
    cards[j]['matches'] = cards[j]['winners'] & cards[j]['mine']
    # number of points calculation
    cards[j]['pts'] = 1 * (2 ** (len(cards[j]['matches']) - 1))
    
print('Part 1 Answer: ' + str(sum([int(cards[j]['pts']) for j in cards])))

#%% Part 2

cards = {}
cNum = 1
for j in raw:
    nums = j[j.index(':') + 2:]
    nums = [i.strip() for i in nums.split('|')]
    cards[cNum] = {}
    cards[cNum]['winners'] = set(nums[0].split(' '))
    cards[cNum]['winners'].discard('')
    cards[cNum]['mine'] = set(nums[1].split(' '))
    cards[cNum]['mine'].discard('')
    cards[cNum]['num'] = 1
    cNum += 1

for j in cards:
    newCards = len(cards[j]['winners'] & cards[j]['mine'])
    for i in range(newCards):
        cards[j + i + 1]['num'] += cards[j]['num']
    
print('Part 2 Answer: ' + str(sum([cards[j]['num'] for j in cards])))