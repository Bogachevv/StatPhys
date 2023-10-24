import numpy as np
from numpy import ndarray
from typing import Self, Tuple, List


class Simulation:
    def __init__(self, T: float, gamma: float, k: float, l_0: float,
                 r: ndarray, r_spring: ndarray,
                 v: ndarray, v_spring: ndarray,
                 m: ndarray, m_spring: ndarray):
        self._T = T
        self._gamma = gamma
        self._k = k
        self._l_0 = l_0
        self._r = r
        self._r_spring = r_spring
        self._v = v
        self._v_spring = v_spring
        self._m = m
        self._m_spring = m_spring

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Tuple[ndarray, ndarray, ndarray, ndarray, float]:
        n_particles = self._r.shape[1]
        n_spring = self._r_spring.shape[1]

        new_r = np.random.uniform(size=(2, n_particles))
        new_v = np.random.uniform(size=(2, n_particles))
        new_r_spr = np.random.uniform(size=(2, n_spring))
        new_v_spr = np.random.uniform(size=(2, n_spring))
        new_f = np.random.uniform()

        return new_r, new_r_spr, new_v, new_v_spr, new_f

    @property
    def T(self) -> float:
        return self._T

    @T.setter
    def T(self, val: float):
        self._T = val

    @property
    def gamma(self) -> float:
        return self._gamma

    @gamma.setter
    def gamma(self, val: float):
        self._gamma = val

    @property
    def k(self) -> float:
        return self._k

    @k.setter
    def k(self, val: float):
        self._k = val

    @property
    def l_0(self) -> float:
        return self._l_0

    @l_0.setter
    def l_0(self, val: float):
        self._l_0 = val

    @property
    def r(self) -> ndarray:
        return self._r

    @property
    def r_spring(self) -> ndarray:
        return self._r_spring

    @property
    def v(self) -> ndarray:
        return self.v

    @property
    def v_spring(self) -> ndarray:
        return self._v_spring

    @property
    def m(self) -> ndarray:
        return self._m

    @property
    def m_spring(self) -> ndarray:
        return self._m_spring

    def calc_kinetic_energy(self) -> ndarray:
        return np.random.uniform(size=(self.r_spring.shape[1],))

    def calc_potential_energy(self) -> ndarray:
        return np.random.uniform(size=(self.r_spring.shape[1],))
