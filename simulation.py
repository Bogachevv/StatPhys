import itertools

import numpy as np
from numpy import ndarray
from typing import Self, Tuple, List


class Simulation:
    def __init__(self, gamma: float, k: float, l_0: float, R: float, R_spring: float,
                 r: ndarray, r_spring: ndarray,
                 v: ndarray, v_spring: ndarray,
                 m: ndarray, m_spring: ndarray):
        self._gamma = gamma
        self._k = k
        self._l_0 = l_0
        self._R = R
        self._R_spring = R_spring
        self._r = np.hstack([r_spring, r])
        # self._r_spring = r_spring
        self._v = np.hstack([v_spring, v])
        # self._v_spring = v_spring
        self._m = np.hstack([m_spring, m])
        # self._m_spring = m_spring
        self._n_particles = r.shape[1]
        self._n_spring = r_spring.shape[1]

        # ids = np.arange(self._n_particles + self._n_spring)
        # self._ids_pairs = np.asarray(list(itertools.combinations(ids, 2)))

        spring_ids = np.arange(self._n_spring)
        self._spring_ids_pairs = np.asarray(list(itertools.combinations(spring_ids, 2)))

        particles_ids = np.arange(self._n_particles) + self._n_spring
        self._particles_ids_pairs = np.asarray(list(itertools.combinations(particles_ids, 2)))

        self._spring_particles_ids_paris = np.asarray(list(itertools.product(spring_ids, particles_ids)))

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Tuple[ndarray, ndarray, ndarray, ndarray, float]:
        # n_particles = self._n_particles
        # n_spring = self._n_spring
        #
        # new_r = np.random.uniform(size=(2, n_particles))
        # new_v = np.random.uniform(size=(2, n_particles))
        # new_r_spr = np.random.uniform(size=(2, n_spring))
        # new_v_spr = np.random.uniform(size=(2, n_spring))
        # new_f = np.random.uniform()
        #
        # return new_r, new_r_spr, new_v, new_v_spr, new_f

        f = self.motion(dt=0.000008)

        return self.r, self.r_spring, self.v, self.v_spring, f

    @property
    def T(self) -> float:
        # raise NotImplemented
        # return self._T
        k_boltz = 1.380 * (10 ** (-23))
        return np.mean(((np.linalg.norm(self._v, axis=0) ** 2) * self._m)) / (2 * k_boltz)

    @T.setter
    def T(self, val: float):
        raise NotImplemented
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
    def R(self) -> float:
        return self._R

    @R.setter
    def R(self, val: float):
        self._R = val

    @property
    def R_spring(self) -> float:
        return self._R_spring

    @R_spring.setter
    def R_spring(self, val: float):
        self._R_spring = val

    @property
    def r(self) -> ndarray:
        return self._r[:, self._n_spring:]

    @property
    def r_spring(self) -> ndarray:
        return self._r[:, :self._n_spring]

    @property
    def v(self) -> ndarray:
        return self._v[:, self._n_spring:]

    @property
    def v_spring(self) -> ndarray:
        return self._v[:, :self._n_spring]

    @property
    def m(self) -> ndarray:
        return self._m[self._n_spring:]

    @property
    def m_spring(self) -> ndarray:
        return self._m[:self._n_spring]

    def calc_kinetic_energy(self) -> float:
        return np.mean((np.linalg.norm(self.v_spring, axis=0) ** 2) * self.m_spring) / 2

    def calc_potential_energy(self) -> float:
        dr = self.r_spring[:, 0] - self.r_spring[:, 1]
        dr_sc = np.linalg.norm(dr)
        dx_norm = np.abs(dr_sc - self.l_0)
        return self._k * (dx_norm ** (self._gamma + 1)) / (self._gamma + 1)

    @staticmethod
    def get_deltad2_pairs(r, ids_pairs):
        dx = np.diff(np.stack([r[0][ids_pairs[:, 0]], r[0][ids_pairs[:, 1]]]).T).squeeze()
        dy = np.diff(np.stack([r[1][ids_pairs[:, 0]], r[1][ids_pairs[:, 1]]]).T).squeeze()
        return dx ** 2 + dy ** 2

    @staticmethod
    def compute_new_v(v1, v2, r1, r2, m1, m2) -> Tuple[ndarray, ndarray]:
        m_s = m1 + m2
        dr = r1 - r2
        dr_norm_sq = np.linalg.norm(dr, axis=0) ** 2

        v1new = v1 - (np.sum((2 * m2 / m_s) * (v1 - v2) * dr, axis=0) * dr) / dr_norm_sq
        v2new = v2 - (np.sum((2 * m1 / m_s) * (v2 - v1) * dr, axis=0) * dr) / dr_norm_sq

        return v1new, v2new

    def motion(self, dt) -> float:
        # ic = self._ids_pairs[self.get_deltad2_pairs(self._r, self._ids_pairs) < self.R ** 2]

        ic_spring = self._spring_ids_pairs[
            np.asarray(self.get_deltad2_pairs(self._r, self._spring_ids_pairs)).reshape((1, ))
            < (2 * self.R_spring) ** 2]

        ic_particles = self._particles_ids_pairs[
            self.get_deltad2_pairs(self._r, self._particles_ids_pairs) < (2 * self.R) ** 2]

        ic_spring_particles = self._spring_particles_ids_paris[
            self.get_deltad2_pairs(self._r, self._spring_particles_ids_paris) < (self.R + self.R_spring) ** 2]

        ic = np.vstack([
            ic_spring,
            ic_particles,
            ic_spring_particles
        ])

        self._v[:, ic[:, 0]], self._v[:, ic[:, 1]] = self.compute_new_v(
            self._v[:, ic[:, 0]], self._v[:, ic[:, 1]],
            self._r[:, ic[:, 0]], self._r[:, ic[:, 1]],
            self._m[ic[:, 0]], self._m[ic[:, 1]]
        )

        dr = self.r_spring[:, 0] - self.r_spring[:, 1]
        # dr_sc = dr.norm()
        dr_sc = np.linalg.norm(dr)
        dx = dr * (1 - self.l_0 / dr_sc)
        dx_norm = np.abs(dr_sc - self.l_0)
        f = (self._k * (dx_norm ** (self._gamma - 1))) * dx
        self.v_spring[:, 0] -= f * (dt / self.m_spring[0])
        self.v_spring[:, 1] += f * (dt / self.m_spring[1])

        self._v[0, self._r[0] > 1] = -np.abs(self._v[0, self._r[0] > 1])
        self._v[0, self._r[0] < 0] = np.abs(self._v[0, self._r[0] < 0])
        self._v[1, self._r[1] > 1] = -np.abs(self._v[1, self._r[1] > 1])
        self._v[1, self._r[1] < 0] = np.abs(self._v[1, self._r[1] < 0])

        self._r = self._r + self._v * dt

        return f @ dr


# TODO:
#   1) rewrite get_deltad2_pairs
#   2) modify index colides (ic) for 2 types of particles
#   3) think about data layout

# video:
# https://youtu.be/iSEAidM-DDI?si=TdfkNox4gglKLRd3
