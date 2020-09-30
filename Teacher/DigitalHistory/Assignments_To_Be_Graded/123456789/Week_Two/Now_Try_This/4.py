# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

d = {'simple_key':'hello'}

answer1 = d['simple_key']
print(answer1)# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

d = {'k1':{'k2':'hello'}}

answer2 = d['k1']['k2']
print(answer2)# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

d = {'k1':[{'nest_key':['this is deep',['hello']]}]}

answer3 = d['k1'][0]['nest_key'][1][0]
print(answer3)# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

d = {'k1':[1,2,{'k2':['this is tricky',{'tough':[1,2,['hello']]}]}]}

answer4 = d['k1'][2]['k2'][1]['tough'][2][0]
print(answer4)