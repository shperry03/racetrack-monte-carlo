import numpy as np

class environment():
    def __init__(self) -> None:
        self.environment = 0

    def create_environment(self,num):
        env = np.zeros((20,20),dtype=int)
        for i in range(0,20):
            for j in range(0,20):
                env[i][j] = -1

        # track 1
        if num == 0:
            for i in range(1,6):
                for j in range(0,20):
                    env[i][j] = 0
            #design track pattern
            for i in range (0,20):
                env[i][0],env[0][i], env[i][19],env[19][i]= -5,-5,-5,-5
            # setting reward for finish line
            for i in range(1,6):
                env[i][19] = 1000
            for i in range(6,20):
                for j in range(3,20):
                    env[i][j] = -5
            # #setting small obstacle
            # env[4][9], env[5][9] = -5,-5
                

        # track 2    
        else:
            # design the track pattern
            for i in range(0,20):
                if i <= 10:
                    for j in range(0,i):
                        env[i][j], env[i][-(j+1)] = -5,-5
                else:
                    for j in range(0, 20-i):
                        env[i][j], env[i][-(j+1)] = -5,-5
                env[19][i] = -5
            #clear hole in middle
            env[10][9], env[10][10] = -1,-1
            env[11][9], env[11][10] = -1,-1
            
            # setting reward for finish line
            for i in range(0,20):
                env[0][i] = 1000

        self.environment = env

env = environment()
env.create_environment(0)
print(env.environment)
env.create_environment(1)
print(env.environment)


        