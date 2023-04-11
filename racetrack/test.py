import policy
import environment
import csv

track = 1

env = environment.environment()
env.create_environment(track)


pol = policy.Policy(track=track)
pol.init_policy(env=env.environment)
val_map = pol.create_value(env=env.environment)

print(val_map)
path = pol.greedy_policy(val_map)
print(path)
with open("val_map_fixed5.csv","w",newline='') as file:
    writer = csv.writer(file)
    for i in range(0,20):
        writer.writerow(val_map[i])

with open("greedy_path1.csv","w") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        writer.writerow(path[i])
