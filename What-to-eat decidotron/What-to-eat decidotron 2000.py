options = ['中餐', '日料', '印度菜', '烧烤', '火锅', '越南米粉', '法餐']
#options = ['Green Truck', 'Red Truck', 'Pink Truck', 'Blue Truck', 'Brown Truck', 'White Truck', 'Fat Basterd', 'Sushi']
weights = [1, 1, 1, 1, 1, 1, 1, 1]

import numpy as np
class food_options:

    def __init__(self, namestr, weight, sequence_num):
        self.sequence_num = sequence_num
        self.name = namestr
        self.weight = weight
    
        self.RNG = np.random.rand()
        self.val = self.RNG * self.weight

output = []

for i in range(len(options)):
    item = food_options(options[i], weights[i], i)
    output.append(item.val)

result_index = output.index(max(output))

print (f'今晚上吃{options[result_index]}')
#print (f"Let's have {options[result_index]} for lunch")