import torch


class Simulation:
    def __init__(self, T, gamma, k, l_0, r, r_spring, v, v_spring, m, m_spring):
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

    def __iter__(self):
        return self

    def __next__(self):
        n_particles = self._r.shape[1]
        n_spring = self._r_spring.shape[1]

        new_r = torch.rand((2, n_particles))
        new_v = torch.rand((2, n_particles))
        new_r_spr = torch.rand((2, n_spring))
        new_v_spr = torch.rand((2, n_spring))
        new_f = torch.rand((1, ))

        return new_r, new_r_spr, new_v, new_v_spr, new_f

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, val):
        self._T = val

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, val):
        self._gamma = val

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, val):
        self._k = val

    @property
    def l_0(self):
        return self._l_0

    @l_0.setter
    def l_0(self, val):
        self._l_0 = val

    @property
    def r(self):
        return self._r

    @property
    def r_spring(self):
        return self._r_spring

    @property
    def v(self):
        return self.v

    @property
    def v_spring(self):
        return self._v_spring

    @property
    def m(self):
        return self._m

    @property
    def m_spring(self):
        return self._m_spring
