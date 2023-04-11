#ON policy montecarlo
import numpy as np

class Policy():

    def __init__(self,track) -> None:
        self.track = track
        self.policy = {}
        self.position_x = 0
        self.position_y = 0

    #policy is going to be map:
    # policy = { [position_y, position_x]: [prob_up, prob_down, prob_left, prob_right], }
    # value = { [position_y, position_x]: value, }

    def init_policy(self, env):
        # first track
        if(self.track) == 0:
            for i in range (0,6):
                for j in range(0,20):
                    if env[i][j] == -1 or env[i][j]==0:
                        self.policy[i,j] = [0.2,0.1,0.1,0.6]
            for i in range(6,20):
                for j in range(0,20):
                    if env[i][j] == -1:
                        self.policy[i,j] = [0.7,0.1,0.1,0.1]
        # second track
        if(self.track) == 1:
            for i in range(0,20):
                for j in range(0,10):
                    if env[i][j] == -1 or env[i][j] == 0:
                        if i <= 10:
                            self.policy[i,j] = [0.6,0.1,0.2,0.1]
                        else:
                            self.policy[i,j] = [0.7,0.1,0.1,0.1]
                for j in range(10, 20):
                    if env[i][j] == -1 or env[i][j] == 0:
                        if i <= 10:
                            self.policy[i,j] = [0.6,0.1,0.1,0.2]
                        else:
                            self.policy[i,j] = [0.7,0.1,0.1,0.1]


                
    # follow the current policy based on probability
    def follow_policy(self):
        directions = ["UP","DOWN","LEFT","RIGHT"]
        direction = np.random.choice(a=directions,size=1,p=self.policy[self.position_y,self.position_x])
        #if x is too big just move left, 
        '''
        TO solve the issue with out of bounds errors, i force it to make certain moves
        on the borders of what is possible 
        too far left? go right
        too far right? go left
        too far down? go up
        too far up? go down
        '''
        # if(self.position_x == 19 and direction=="RIGHT"):
        #     direction = "LEFT"
        # if(self.position_x == 0 and direction=="LEFT"):
        #     direction = "RIGHT"
        # if(self.position_y == 19 and direction=="UP"):
        #     direction = "DOWN"
        # if(self.position_y == 0 and direction=="DOWN"):
        #     direction = "UP"
        return direction
    
    # move based on direction given
    def move(self,direction):
        match direction:
            case "UP":
                # if(self.position_y != 0):
                    self.position_y -= 1
            case "DOWN":
                # if(self.position_y != 19):
                    self.position_y += 1
            case "LEFT":
                # if(self.position_x != 0):
                    self.position_x -= 1
            case "RIGHT":
                # if(self.position_x != 19):
                    self.position_x += 1

    #get start position depending on track
    def get_start(self):
        if self.track == 0:
            return np.random.randint(low=1,high=3,size=1)[0]
        else:
            return np.random.randint(low=2,high=18,size=1)[0]

    # given policy generate episode
    def generate_episode(self,env):
        episode = []
        # set starting position
        self.position_x, self.position_y = self.get_start(),18

        # if position
        while env[self.position_y][self.position_x] not in [-5,1000]:
            direction = self.follow_policy()
            self.move(direction)
            state = [self.position_y,self.position_x]

            episode.append(state)

        episode.append([self.position_y,self.position_x])

        return episode

    def create_value(self,env):
        '''
        * basically for every move its -1
        * out of bounds is -5
        * finish is +20
        * generate optimal map by creating value network from monte carlo search
        * greedy search the value map
        '''
        # retruns is a dict {state, [empty list of G]}
        returns = {}
        # set the discount rate for evaluations
        discount = 0.8
        # initialize the value map
        # env is a numpy array that represents the track
        val_map = env
        # now we loop to do the monte carlo 
        for _ in range(40000):
            episode = self.generate_episode(env)
            episode = episode[:-1]
            count = len(episode)

            G = 0
            for i in reversed(range(0,count-1)):
                state = episode[i]
                state_prev = episode[i+1]
                G = (discount)*env[state_prev[0]][state_prev[1]]
                if (state[0],state[1]) in returns:

                    returns[state[0],state[1]].append(G)
                else:

                    returns[state[0],state[1]] = []
                    returns[state[0],state[1]].append(G)
                val_map[state[0]][state[1]] = (sum(returns[state[0],state[1]])/len(returns[state[0],state[1]]))


        return val_map
    
    def get_direction(self,env,i,j):
        max1 = max(env[i+1][j],env[i-1][j],env[i][j+1],env[i][j-1])
        if env[i+1][j] == max1:
            return "DOWN"
        elif env[i-1][j] == max1:
            return "UP"
        elif env[i][j+1] == max1:
            return "RIGHT"
        elif env[i][j-1] == max1:
            return "LEFT"
    
    def greedy_policy(self,env):
        path = np.zeros((20,20),dtype=object)
        for i in range(0,20):
            for j in range(0,20):
                if env[i][j] not in [-5,1000]:
                    path[i][j]= self.get_direction(env,i,j)
        return path



        

            
