import random
from typing import Callable, List, Sequence, Tuple
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

Gene = Tuple[int, int]
Bounds = Sequence[Tuple[int, int]]
FitnessFn = Callable[[Gene], float]


class GeneticAlgorithm:
    """
    Простой генетический алгоритм для оптимизации функции двух переменных.
    Оптимизация производится по максимуму fitness-функции.
    """

    def __init__(
        self,
        fitness_fn: FitnessFn,
        bounds: Bounds,
        pop_size: int = 50,
        mutation_rate: float = 0.1,
        elite_size: int = 2,
    ) -> None:
        self.fitness_fn: FitnessFn = fitness_fn
        self.bounds: Bounds = bounds
        self.pop_size: int = pop_size
        self.mutation_rate: float = mutation_rate
        self.elite_size: int = elite_size

        self.population: List[Gene] = self._init_population()
        self.history: List[float] = []

    # ---------- инициализация ----------
    def _init_population(self) -> List[Gene]:
        return [
            (
                random.randint(*self.bounds[0]),
                random.randint(*self.bounds[1]),
            )
            for _ in range(self.pop_size)
        ]

    # ---------- генетические операторы ----------
    def _select(self) -> Gene:
        """Турнирный отбор из двух особей."""
        a, b = random.sample(self.population, 2)
        return max((a, b), key=self.fitness_fn)

    def _crossover(self, p1: Gene, p2: Gene) -> Gene:
        """Одноточечный кроссовер."""
        return (p1[0], p2[1]) if random.random() < 0.5 else (p2[0], p1[1])

    def _mutate(self, gene: Gene) -> Gene:
        g1, g2 = gene

        if random.random() < self.mutation_rate:
            g1 += random.choice((-1, 1))
        if random.random() < self.mutation_rate:
            g2 += random.choice((-1, 1))

        # ограничение границами
        g1 = max(self.bounds[0][0], min(g1, self.bounds[0][1]))
        g2 = max(self.bounds[1][0], min(g2, self.bounds[1][1]))

        return g1, g2

    # ---------- шаг алгоритма ----------
    def step(self) -> None:
        elite = sorted(
            self.population,
            key=self.fitness_fn,
            reverse=True,
        )[: self.elite_size]

        new_population: List[Gene] = elite.copy()

        while len(new_population) < self.pop_size:
            p1 = self._select()
            p2 = self._select()

            child = self._crossover(p1, p2)
            child = self._mutate(child)
            new_population.append(child)

        self.population = new_population

        best_fit = self.fitness_fn(self.best())
        self.history.append(best_fit)

    # ---------- служебные методы ----------
    def best(self) -> Gene:
        return max(self.population, key=self.fitness_fn)

    def run(self, generations: int = 100) -> Gene:
        for _ in range(generations):
            self.step()
        return self.best()

    # ---------- визуализация популяции ----------
    def plot_population(self, filename: str = "genalg.png") -> None:
        xs = [g[0] for g in self.population]
        ys = [g[1] for g in self.population]

        plt.figure(figsize=(12, 5))

        # распределение популяции
        plt.subplot(1, 2, 1)
        plt.scatter(xs, ys)
        plt.xlabel("Gene X")
        plt.ylabel("Gene Y")
        plt.title("Population")

        # прогресс обучения
        plt.subplot(1, 2, 2)
        plt.plot(self.history)
        plt.xlabel("Generation")
        plt.ylabel("Best fitness")
        plt.title("Fitness progress")

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    # ---------- поверхность функции ----------
    def plot_surface(
        self,
        resolution: int = 100,
        filename: str = "surface.png",
        show_population: bool = True,
    ) -> None:
        """
        Визуализация поверхности функции.
        Можно наложить текущую популяцию.
        """

        x_min, x_max = self.bounds[0]
        y_min, y_max = self.bounds[1]

        xs = np.linspace(x_min, x_max, resolution)
        ys = np.linspace(y_min, y_max, resolution)
        X, Y = np.meshgrid(xs, ys)

        Z = np.vectorize(
            lambda x, y: self.fitness_fn((int(x), int(y)))
        )(X, Y)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot_surface(X, Y, Z, alpha=0.7)

        if show_population:
            pop_x = np.array([g[0] for g in self.population])
            pop_y = np.array([g[1] for g in self.population])
            pop_z = np.array(
                [self.fitness_fn(g) for g in self.population]
            )

            ax.scatter(pop_x, pop_y, pop_z, s=40)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Fitness")
        ax.set_title("Fitness Surface")

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()


# ------------------- пример -------------------
if __name__ == "__main__":

    def func(gene: Gene) -> float:
        """x ∈ [-5,5], y ∈ [-10,10]"""
        x, y = gene
        return x**3 + 2 * x * y + y**3

    alg = GeneticAlgorithm(
        fitness_fn=func,
        bounds=[(-5, 5), (-10, 10)],
    )

    alg.run(150)

    alg.plot_population()
    alg.plot_surface()
