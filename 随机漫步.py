from random import choice
import matplotlib.pyplot as plt

class RandomWalk:
    def __init__(self,num_points=5000):
        self.num_points=num_points
        self.x_values=[0]
        self.y_values=[0]

    def get_step(self):

        direction=choice([1,-1])
        distence=choice([0,1,2,3,4,5,6])
        step=direction * distence

        return step

    def fill_walk(self):
        
        while len(self.x_values) < self.num_points:

            x_step=self.get_step()
            y_step=self.get_step()
            
            if x_step==0 and y_step==0:
                continue

            next_x=self.x_values[-1]+x_step
            next_y=self.y_values[-1]+y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)

rw=RandomWalk()
rw.fill_walk()

plt.scatter(rw.x_values,rw.y_values,cmap=plt.cm.Blues,edgecolor='none',s=2)
plt.scatter(0,0,c='green',edgecolors='none',s=10)
plt.scatter(rw.x_values[-1],rw.y_values[-1],c='red',edgecolors='none',s=10)
plt.show()

