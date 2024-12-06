# This code is part of Quantum Rings SDK.
#
# (C) Copyright Quantum Rings Inc, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=wrong-import-position,wrong-import-order

from typing import List, Union, Iterable, Tuple

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2
from qiskit.primitives import BackendSamplerV2
from qiskit.result import Result
from qiskit.primitives.containers import SamplerPubLike,  SamplerPubResult
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit.result import QuasiDistribution

import QuantumRingsLib

from qiskit.primitives import DataBin
from qiskit.primitives import PubResult
from qiskit.primitives import PrimitiveResult
from qiskit.primitives import PrimitiveJob
from qiskit.primitives import SamplerResult


from quantumrings.toolkit.qiskit import meas
from quantumrings.toolkit.qiskit import QrTranslator
from quantumrings.toolkit.qiskit import QrBackendV2

        
class QrSamplerV2(BackendSamplerV2):
    def __init__(
        self,
        *, 
        backend: QrBackendV2 = None,
        **kwargs
        ):
        if (backend is None):
            qr_provider = QuantumRingsLib.QuantumRingsProvider()
            backend = QrBackendV2(qr_provider)
            if (backend._qr_backend.num_qubits == 0):
                raise Exception("Either provide a valid QrBackendV2 object as a parameter or save your account credentials using QuantumRingsLib.QuantumRingsProvider.save_account method")
                return
        elif (False == isinstance(backend, QrBackendV2)):
            raise Exception ("The backend for this class should be a Quantum Rings Backend.")
            return
        self._qr_backend = backend._qr_backend
        self._num_circuits = 1
        self._default_options = Options()
        
        # Dynamical decoupling options
        self._default_options.dynamical_decoupling = Options()
        self._default_options.dynamical_decoupling.enable = False
        self._default_options.dynamical_decoupling.sequence_type = "XY4"
        
        # Twirling options
        self._default_options.twirling = Options()
        self._default_options.twirling.enable_gates = False
        self._default_options.twirling.num_randomizations = 1
        
        self._default_options.shots = 1024
        self._default_options.sync_mode = False
        self._default_options.performance = "HIGHESTACCURACY"
        self._default_options.quiet = True
        self._default_options.defaults = True
        self._default_options.generate_amplitude = False

        super().__init__(backend = backend)

    @property
    def options(self) -> Options:
        """Return the options"""
        return self._default_options
        
       
    def job_call_back(self, job_id, state, job) -> None:
        pass

    def run_sampler(self, circuits, **run_options):
        results = []

        # Validate the circuits parameter.
        if not isinstance(circuits, QuantumCircuit):
            raise Exception( "Invalid argument passed for Quantum Circuit.")
            return

        # Fetch run time options
        if "shots" in run_options:
            self._shots = run_options.get("shots")
            if not isinstance(self._shots, int):
                raise Exception( "Invalid argument for shots")
                return
            if ( self._shots <= 0 ):
                raise Exception( "Invalid argument for shots")
                return
        else:
            self._shots = self._default_options.shots
            
        if "sync_mode" in run_options:
            self._sync_mode = run_options.get("sync_mode")
            if not isinstance(self._sync_mode, bool):
                raise Exception( "Invalid argument for sync_mode")
                return
        else:
            self._sync_mode = self._default_options.sync_mode

        # We need to figure out the number of qubits required.
        # Parse the circuit and figure out the largest number of qubits required
        #max_qubit = -1
        #for instruction in circuits:
        #    for i in range (len(instruction.qubits)):
        #        if (instruction.qubits[i]._index > max_qubit):
        #            max_qubit = instruction.qubits[i]._index
        #if ( -1 == max_qubit ):
        #    raise Exception( "Submitted quantum circuit does not use any qubits")
        #    return
        #max_qubit += 1        # bump this to pass as argument

        max_qubit = 0
        for j in range (len(circuits.qregs)):
            max_qubit += circuits.qregs[0].size

        if ( max_qubit <= 0 ):
            raise Exception( "Submitted quantum circuit does not use any qubits")
            return

        
        self._max_qubits = max_qubit
        self._max_clbits = max_qubit
        
                   
        # if we get here, the measurement instructions, if any, are at the end of the circuit
        # create the quantum circuit now
        
        #TODO: Check control loops
        qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
        creg = QuantumRingsLib.ClassicalRegister(self._max_qubits, "meas")
        qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = circuits.name,  global_phase = circuits.global_phase)

        # export the measurements to QuantumRings Structure
        QrTranslator.translate_quantum_circuit(circuits, qc)

        job = self._qr_backend.run(qc, shots= self._shots, sync_mode = self._sync_mode, performance = "HighestAccuracy", quiet = True)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        results = job.result()
        result_dict = results.get_counts()
        self._job_id = job.job_id
        
        my_sampler_meas = meas(result_dict)
        
        return my_sampler_meas
                
       
    def _run(self, pubs: list[SamplerPub], *, shots: int | None = None) -> PrimitiveResult[SamplerPubResult]:
        results = []
        metadata = []

        for pub in pubs:
            
            if ( isinstance(pub, tuple)):
                    circuit = pub[0]
            elif (isinstance(pub, QuantumCircuit)):
                    circuit = pub
            else:
                raise Exception (f"Unsupported data element {type(pub)} in the run method")
                return

            if (shots is None):
                pub_data = self.run_sampler(circuit, shots = self._default_options.shots)
            else:
                pub_data = self.run_sampler(circuit, shots = shots)
        
            pub_result = DataBin(meas = pub_data,)
            results.append(SamplerPubResult(pub_result))
            metadata.append([{"version": 2}, {"shots": shots}])

        return PrimitiveResult(results, metadata=metadata)

    def run(
        self, pubs: Iterable[SamplerPubLike], *, shots: int | None = None
    ) -> PrimitiveJob[PrimitiveResult[SamplerPubResult]]:
        my_sampler_job = PrimitiveJob(self._run, pubs, shots=shots)
        my_sampler_job._submit()
        return  my_sampler_job
    