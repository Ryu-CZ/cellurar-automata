from typing import _T_co

import numpy as np
import collections

universe = np.zeros((6, 6))
beacon = [[1, 1, 0, 0],
          [1, 1, 0, 0],
          [0, 0, 1, 1],
          [0, 0, 1, 1]]
universe[1:5, 1:5] = beacon
new_universe = np.zeros((6, 6))


class Universe(collections.Iterator):

    def __init__(self, width: int, height: int = None) -> None:
        self.generation = 0
        self.width = width
        self.height = height or width
        self.space = np.zeros((self.height, self.width))

    @property
    def x_size(self) -> int:
        return self.width

    @property
    def y_size(self) -> int:
        return self.height

    def empty(self) -> None:
        self.space = np.zeros((6, 6))

    def count_neighbours(self, x: int, y: int) -> int:
        return self.space[
               max(x - 1, 0):min(x + 2, self.height),
               max(y - 1, 0):min(y + 2, self.width)
               ].sum() - self.space[x, y]

    def survival(self, x: int, y: int) -> int:
        neighbours = self.count_neighbours(x, y)
        if self.space[x, y] and not 2 <= neighbours <= 3:
            return 0
        elif neighbours == 3:
            return 1
        else:
            return self.space[x, y]

    def new_generation(self) -> None:
        tmp_space = np.zeros(self.space.shape)
        for x, y in np.ndindex(self.space.shape):
            tmp_space[x, y] = self.survival(x, y)
        np.copyto(self.space, tmp_space)
        self.generation += 1


universe = Universe(6)
universe.space[1:5, 1:5] = beacon
universe.new_generation()
universe.new_generation()

import matplotlib.pyplot as plt


plt.imshow(universe.space, cmap='binary')
plt.show()
# import matplotlib.animation as animation
# ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
#                               repeat=False, init_func=init)
# plt.show()