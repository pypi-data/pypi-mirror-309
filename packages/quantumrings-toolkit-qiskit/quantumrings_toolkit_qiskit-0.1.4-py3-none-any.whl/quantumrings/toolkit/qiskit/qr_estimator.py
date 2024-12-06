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

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2

from qiskit.primitives import BackendEstimatorV2
from qiskit.result import Result
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit.primitives.containers import EstimatorPubLike

import QuantumRingsLib

from qiskit.primitives import DataBin
from qiskit.primitives import PubResult
from qiskit.primitives import PrimitiveResult
from qiskit.primitives import PrimitiveJob

from dataclasses import dataclass
from quantumrings.toolkit.qiskit import QrTranslator
from quantumrings.toolkit.qiskit import QrBackendV2

from qiskit.quantum_info.operators.symplectic.sparse_pauli_op import SparsePauliOp as SparsePauliOp
import numpy

class QrEstimatorV2(BackendEstimatorV2):
    def __init__(
        self,
        *,
        backend: QrBackendV2 = None,
        options: dict | None = None,
        run_options: dict | None = None
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
        
        shots_ = 1024
        if ( options is not None):
            if ("shots" in options ):
                shots_ = options["shots"]

        if ( run_options is not None):
            if ("shots" in run_options ):
                shots_ = run_options["shots"]

        self._default_options.shots = 1024
        self._default_options.sync_mode = False
        self._default_options.performance = backend.options.performance
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

    def run_estimator(self, circuits, observables,  params, **run_options):
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

        # Confirm we have the right number of params
        if (isinstance(params, numpy.float64)):
            if (circuits.num_parameters != 1 ):
                raise Exception ("The given number of parameters is less than the parameters in the circuit.")
                return
        elif (circuits.num_parameters > len(params)):
            raise Exception ("The given number of parameters is less than the parameters in the circuit.")
            return

        #Assign parameters
        if (circuits.num_parameters):
            if (isinstance(params, numpy.float64)):
                subs_params = []
                subs_params.append(params)
                run_input = circuits.assign_parameters(subs_params)
            else:
                run_input = circuits.assign_parameters(params)
        else:
            run_input = circuits

        self._max_qubits = run_input.num_qubits
        self._max_clbits = run_input.num_clbits
        
        # check whether the Pauli operator sizes match  max_qubit
        if (self._max_qubits != len(observables.paulis[0])):
            raise Exception( "The Pauli operator length is not matching number of qubits")
            return
        
        # Check sanity of the measurement instructions
        # There shouldn't be any other instruction after the last measurement instruction
        ins_found = False
        for instruction in reversed(run_input):
            if ( instruction.operation.name == "measure" ):
                if ( False == ins_found ):
                    continue
                else:
                    raise Exception( "Invalid Instruction sequence. Measurement preceeds a gate operation")
                    return
            elif ( instruction.operation.name == "barrier" ):
                continue
            else:
               ins_found = True 
                    
        # if we get here, the measurement instructions, if any, are at the end of the circuit
        # create the quantum circuit now
        
        #TODO: Check control loops
        qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
        creg = QuantumRingsLib.ClassicalRegister(self._max_qubits, "meas")
        qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = run_input.name,  global_phase = run_input.global_phase)

        # export the measurements to QuantumRings Structure
        QrTranslator.translate_quantum_circuit(run_input, qc)

        
        # We must setup the Pauli operator now.
        # for each Pauli operator
        avg = 0.0

        pauli_list = observables.to_list()
        

        for p in range(len(pauli_list)):
            weight = pauli_list[p][1].real
            pauli  = pauli_list[p][0]

            # clone the quantum circuit
            qc_estimator = qc.copy() 
    
            # Apply the Pauli operators.
            # no actions for "I" or "Z"
            for i in range(self._max_qubits):
                if (pauli[i] == "Y"):
                    qc_estimator.sdg(i)
                    qc_estimator.h(i)
                    
                elif (pauli[i] == "X"):
                    qc_estimator.h(i)
                elif ((pauli[i] == "I") or (pauli[i] == "Z")):
                    pass
                else:
                    raise Exception(f"Error. Illegal Pauli {p} operator {pauli}")
                    return
    
            # We should measure this circuit in the computation basis now
            qc_estimator.measure_all()

            job = self._qr_backend.run(qc_estimator, shots= self._shots, sync_mode = self._sync_mode, performance = self._default_options.performance, quiet = True)
            job.wait_for_final_state(0.0, 5.0, self.job_call_back)
            results = job.result()
            result_dict = results.get_counts()
            self._job_id = job.job_id   # Store the last used job ID as the reference job id.
            
            # perform the pauli measurement
            # convert the operator into binary
            measurement = 0.0
            try:
                pauli_int = int (pauli.__str__().replace("I","0").replace("Z","1").replace("X","1").replace("Y","1"),2)
            except Exception as ex:
                raise Exception(f"Exception {ex} occured")
                return
    
            for key, value in result_dict.items():
                sign = -1.0 if ( bin(int(key,2) & pauli_int).count("1") & 1 ) else 1.0
                measurement += sign * value
            measurement /= self._shots
    
            measurement = measurement * weight
            avg = avg + measurement

        
        return avg
        
   
    def _process_pub_two(self, circuit, observable, param_, pub_data):
        if (isinstance(param_, numpy.ndarray)):
            params = param_
            pub_data.append(self.run_estimator(circuit, observable, params))
        elif (isinstance(param_, list)):
            avg_exp = []
            for params in param_:
                avg_exp.append(self.run_estimator(circuit, observable, params))
            pub_data.append(avg_exp)

    
    def _run(self, pubs: list[EstimatorPub]) -> PrimitiveResult[PubResult]:
      
        results = [None] * len(pubs)
        metadata = [None] * len(pubs)

        for i, pub in enumerate(pubs):
            pub_data = []
            circuit = pub[0]
            if (isinstance(pub[1], list)):
                  for observable_list in pub[1]:
                    if (isinstance(observable_list, list)):
                        for observ in observable_list:
                            observable = observ
                            # check what's up with pub[2]
                            self._process_pub_two(circuit, observable, pub[2], pub_data)
                    elif (isinstance(pub[1][0], SparsePauliOp)):
                        observable = pub[1][0]
                        self._process_pub_two(circuit, observable, pub[2], pub_data)
                    else:
                        raise Exception("Ill formed pub[1]")
                        return
            elif (isinstance(pub[1], SparsePauliOp)):
                # QAOA type sample
                observable = pub[1]
                self._process_pub_two(circuit, observable, pub[2], pub_data)
            else:
                raise Exception("Ill formed pub[1]")
                return
    
            pub_result = DataBin(evs = pub_data,)
            results[i] = PubResult(pub_result)
            metadata[i] = {"version": 2}
        
        return PrimitiveResult(results, metadata=metadata)

    def run(
        self, pubs: Iterable[EstimatorPubLike], *, precision: float | None = None
        ) -> PrimitiveJob[PrimitiveResult[PubResult]]:

        my_estimator_job = PrimitiveJob(self._run, pubs)
        my_estimator_job._submit()
        return  my_estimator_job

