import numpy as np
from pydantic import BaseModel
from typing import Optional, Callable, Union
from priceforge.pricing.models.ode_solver import OdeSolution, RootSign
from priceforge.pricing.models.parameters import (
    CorrelationParameters,
    RateParameters,
    SpotParameters,
    VolatilityParameters,
)
from priceforge.pricing.models.protocol import (
    CharacteristicFunctionODEs,
    PricingModel,
    SimulatableModel,
    StochasticProcess,
)


class OrnsteinUhlenbeckProcess(StochasticProcess):
    def __init__(
        self,
        initial_variance: float,
        mean_reversion_rate: float,
        long_term_mean: float,
        vol_of_vol: float,
    ):
        self.initial_variance = initial_variance
        self.mean_reversion_rate = mean_reversion_rate
        self.long_term_mean = long_term_mean
        self.vol_of_vol = vol_of_vol

    def correlation_matrix(self) -> np.ndarray:
        return np.array([1])

    def initial_state(self) -> np.ndarray:
        return np.array(self.initial_variance)

    def drift(self, time: float, current_state: np.ndarray) -> Union[float, np.ndarray]:
        return self.mean_reversion_rate * (self.long_term_mean - current_state)

    def volatility(
        self, time: float, current_state: np.ndarray
    ) -> Union[float, np.ndarray]:
        return self.vol_of_vol * np.sqrt(current_state)


class HestonSpotProcess(StochasticProcess):
    def __init__(self, spot: float, rate: float, vol: float = 1.0):
        self.spot = spot
        self.vol = vol
        self.rate = rate

    def correlation_matrix(self) -> np.ndarray:
        return np.array([1])

    def initial_state(self) -> np.ndarray:
        return np.array(np.log(self.spot))

    def drift(self, time: float, current_state: np.ndarray) -> Union[float, np.ndarray]:
        return self.rate - 0.5 * current_state * self.vol**2

    def volatility(
        self, time: float, current_state: np.ndarray
    ) -> Union[float, np.ndarray]:
        current_var = current_state
        return self.vol * np.sqrt(current_var)


class HestonCompositeProcess(StochasticProcess):
    def __init__(
        self,
        spot: HestonSpotProcess,
        vol: OrnsteinUhlenbeckProcess,
        spot_vol_corr: float,
    ):
        self.spot_process = spot
        self.vol_process = vol
        self._correlation_matrix = np.array(
            [[1.0, spot_vol_corr], [spot_vol_corr, 1.0]]
        )

    def correlation_matrix(self) -> np.ndarray:
        return self._correlation_matrix

    def initial_state(self) -> np.ndarray:
        return np.array(
            [self.spot_process.initial_state(), self.vol_process.initial_state()]
        )

    def drift(self, time: float, current_state: np.ndarray) -> Union[float, np.ndarray]:
        current_vol = np.abs(current_state[:, 1])
        spot_drift = self.spot_process.drift(time, current_state=current_vol)
        vol_drift = self.vol_process.drift(time, current_state=current_vol)
        return np.array([spot_drift, vol_drift]).T

    def volatility(
        self, time: float, current_state: np.ndarray
    ) -> Union[float, np.ndarray]:
        current_vol = np.abs(current_state[:, 1])
        spot_vol = self.spot_process.volatility(time, current_state=current_vol)
        vol_of_vol = self.vol_process.volatility(time, current_state=current_vol)
        return np.array([spot_vol, vol_of_vol]).T


class SolverParameters(BaseModel):
    d_root_sign: RootSign = RootSign.MINUS


class HestonParameters(BaseModel):
    spot: SpotParameters = SpotParameters()
    rate: RateParameters = RateParameters()
    volatility: VolatilityParameters = VolatilityParameters()
    correlation: CorrelationParameters = CorrelationParameters()
    ode_solution: OdeSolution = OdeSolution.ANALYTICAL
    analytical_soluton: SolverParameters = SolverParameters()


class HestonODEs(CharacteristicFunctionODEs):
    def __init__(
        self,
        params: HestonParameters,
    ):
        self.params = params

    def odes(
        self,
        u: complex,
        time_to_option_expiry: float,
        time_to_underlying_expiry: Optional[float],
    ) -> Callable[[float, float], tuple[complex, complex]]:
        assert isinstance(time_to_underlying_expiry, type(None))
        rate = self.params.rate
        volatility = self.params.volatility
        correlation = self.params.correlation

        def y_prime(tau, state):
            _, upper_d = state

            upper_c_prime = (
                volatility.mean_reversion_rate * volatility.long_term_mean**2 * upper_d
                + 1j * u * rate.value
            )
            upper_d_prime = (
                -0.5 * (u**2 + 1j * u)
                + upper_d
                * (
                    -volatility.mean_reversion_rate
                    + 1j * u * volatility.volatility * correlation.spot_vol
                )
                + 0.5 * volatility.volatility**2 * upper_d**2
            )

            return (upper_c_prime, upper_d_prime)

        return y_prime

    def analytical_soluton(
        self,
        u: complex,
        time_to_option_expiry: float,
        time_to_underlying_expiry: Optional[float],
    ) -> tuple[complex, complex]:
        assert isinstance(time_to_underlying_expiry, type(None))
        d_term, g_term, kappa_rho_sigma = self._compute_intermediate_terms(u)
        upper_d = self._compute_upper_d(
            time_to_option_expiry, d_term, g_term, kappa_rho_sigma
        )
        upper_c = self._compute_upper_c(
            u, time_to_option_expiry, d_term, g_term, kappa_rho_sigma
        )

        return (upper_c, upper_d)

    def _compute_intermediate_terms(
        self, u: complex
    ) -> tuple[complex, complex, complex]:
        vol = self.params.volatility
        corr = self.params.correlation

        kappa_rho_sigma = (
            vol.mean_reversion_rate - 1j * u * vol.volatility * corr.spot_vol
        )

        d_term = self.params.analytical_soluton.d_root_sign * (
            (kappa_rho_sigma**2 + vol.volatility**2 * (u**2 + 1j * u)) ** 0.5
        )
        g_term = (kappa_rho_sigma + d_term) / (kappa_rho_sigma - d_term)

        return (d_term, g_term, kappa_rho_sigma)

    def _compute_upper_d(
        self, tau: float, d_term: complex, g_term: complex, kappa_rho_sigma: complex
    ) -> complex:
        vol = self.params.volatility
        exp_dt = np.exp(d_term * tau)

        numerator = (kappa_rho_sigma + d_term) * (1 - exp_dt)
        denominator = vol.volatility**2 * (1 - g_term * exp_dt)

        return numerator / denominator

    def _compute_upper_c(
        self,
        u: complex,
        tau: complex,
        d_term: complex,
        g_term: complex,
        kappa_rho_sigma: complex,
    ) -> complex:
        vol = self.params.volatility
        exp_dt = np.exp(d_term * tau)

        rate_term = self.params.rate.value * 1j * u * tau

        kappa_theta_term = (
            vol.mean_reversion_rate * vol.long_term_mean**2 / vol.volatility**2
        )

        log_term = -2 * np.log((1 - g_term * exp_dt) / (1 - g_term))

        return rate_term + kappa_theta_term * (
            (kappa_rho_sigma + d_term) * tau + log_term
        )


class HestonModel(PricingModel, SimulatableModel):
    params_class = HestonParameters
    characteristic_function_odes: HestonODEs

    def __init__(self, params: HestonParameters):
        self.params = params

        self.characteristic_function_odes = HestonODEs(params)

        heston_process = HestonSpotProcess(
            spot=params.spot.value, rate=params.rate.value, vol=params.spot.volatility
        )

        vol_process = OrnsteinUhlenbeckProcess(
            initial_variance=params.volatility.value**2,
            mean_reversion_rate=params.volatility.mean_reversion_rate,
            long_term_mean=params.volatility.long_term_mean**2,
            vol_of_vol=params.volatility.volatility,
        )

        self.process = HestonCompositeProcess(
            spot=heston_process,
            vol=vol_process,
            spot_vol_corr=params.correlation.spot_vol,
        )

    def zero_coupon_bond(self, time_to_expiry) -> float:
        return np.exp(-self.params.rate.value * time_to_expiry)

    def forward(self, time_to_expiry) -> float:
        return self.params.spot.value / self.zero_coupon_bond(time_to_expiry)

    def characteristic_function(
        self,
        u: complex,
        time_to_option_expiry: float,
        time_to_underlying_expiry: Optional[float],
    ) -> complex:
        if u == 0.0 + 0.0j:
            return 1.0 + 0.0j

        match self.params.ode_solution:
            case OdeSolution.ANALYTICAL:
                upper_c, upper_d = self.characteristic_function_odes.analytical_soluton(
                    u, time_to_option_expiry, time_to_underlying_expiry
                )
            case OdeSolution.NUMERICAL:
                upper_c, upper_d = self.characteristic_function_odes.numerical_solution(
                    u, time_to_option_expiry, time_to_underlying_expiry
                )
        psi = np.exp(
            upper_c
            + upper_d * self.params.volatility.value**2
            + 1j * u * np.log(self.params.spot.value)
        )
        return psi
