# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      https://mit-license.org/
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import NamedTuple, Optional, cast

import numpy as np
import numpy.typing as npt
from quri_parts.core.estimator import Estimate
from quri_parts.qulacs.simulator import evaluate_state_to_vector

from quri_algo.core.estimator import State
from quri_algo.problem import HamiltonianInput

from .interface import TimeEvolutionExpectationValueEstimator


class _Estimate(NamedTuple):
    value: complex
    error: float = np.nan


@dataclass
class ExactTimeEvolutionExpectationValueEstimator(
    TimeEvolutionExpectationValueEstimator[HamiltonianInput, State]
):
    """Estimate with matrix multiplication."""

    eigenvalues: npt.NDArray[np.complex128]
    eigenvectors: npt.NDArray[np.complex128]

    def __call__(
        self, state: State, evolution_time: float, n_shots: Optional[int] = None
    ) -> Estimate[complex]:
        vector = evaluate_state_to_vector(state).vector
        pi = np.abs(vector.conj() @ self.eigenvectors) ** 2
        exp = np.exp(-1j * evolution_time * self.eigenvalues)
        return _Estimate(value=cast(complex, pi @ exp))
