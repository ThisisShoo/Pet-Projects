"""Welcome to what-to-eat-decidotron (WED).
Please ensure that you've read WED's user manual.
"""
import numpy as np

class Restaurant:
    """Defines a restaurant
    """
    def __init__(self, name, dist, rating, price) -> None:
        self.name = name
        self.dist_facor = np.exp(-0.5 * float(dist)**2)
        self.rating_factor = float(rating)/5
        self.price_factor = 4/float(price)

        # Closer and higher rated restaurants are favored
        # Score = 1/dist * rating/5 * (4 - price) = dist_facor * rating_factor * price_factor
        self.favor_score = self.dist_facor * self.rating_factor * self.price_factor

# Text processor 
with open("Restaurant inputs.txt", 'r', encoding="utf-8") as restaurant_file:
    data_all = restaurant_file.readlines()

data_temp = data_all[1:]
data_header = data_all[0].strip('\n').replace(' ', '').split(',')

ROW_NUM = 0
restaurant_stats = []

for row in data_temp:
    row_temp = row.strip(' \n')
    row_temp = row_temp.strip(' \t')
    row_temp = row_temp.split(', ')

    name_temp, dist_temp, rating_temp, price_temp = row_temp

    restaurant_temp = Restaurant(name_temp, dist_temp, rating_temp, price_temp)
    globals()[f'restaurant{ROW_NUM}'] = restaurant_temp

    restaurant_stats.append(globals()[f'restaurant{ROW_NUM}'].favor_score)

    ROW_NUM += 1

restaurant_stats = np.array(restaurant_stats) / max(restaurant_stats)

# Calculates the best restaurant
final_score = []
favor_score = []
for i in range(ROW_NUM):
    restaurant_temp = globals()[f'restaurant{i}']
    RNG = np.random.rand()
    final_score.append(round(RNG * restaurant_stats[i], 2))
    favor_score.append(round(restaurant_temp.favor_score, 2))

print (favor_score)

winner_index = final_score.index(max(final_score))
winner = globals()[f'restaurant{winner_index}']

print(f'Winner is {winner.name}')
print(f'It had a final score of {round(final_score[winner_index], 2)}')
print(f'and a favorable score of {round(winner.favor_score, 2)}')
