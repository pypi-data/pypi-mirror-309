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

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.transpiler import CouplingMap, Target, InstructionProperties, QubitProperties
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2
from qiskit.result import Result
from qiskit.circuit.controlflow import (
    IfElseOp,
    WhileLoopOp,
    ForLoopOp,
    SwitchCaseOp,
    BreakLoopOp,
    ContinueLoopOp,
    )

import QuantumRingsLib

from quantumrings.toolkit.qiskit import QrTranslator
from quantumrings.toolkit.qiskit import QrJobV1


class QrBackendV2(BackendV2):
    
    def __init__(self, *args, **kwargs) -> None:

        if ( isinstance(kwargs.get('token'), str ) ) and ( isinstance(kwargs.get('name'), str ) ):
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider(token = kwargs.get('token'), name = kwargs.get('name'))
        elif isinstance(kwargs.get('provider'), QuantumRingsLib.QuantumRingsProvider ):
            self._qr_provider = kwargs.get('provider')
        elif (len(args) > 1 ) and ( isinstance(args[0], str ) ) and ( isinstance(args[1], str ) ):
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider(token = args[0], name = args[1])
        elif (len(args) > 0 ) and ( isinstance(args[0], QuantumRingsLib.QuantumRingsProvider ) ):
            self._qr_provider = args[0]
        else:
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider()

        if ( self._qr_provider is None ):
            raise Exception ("Unable to obtain Quantum Rings Provider. Please check the arguments")
            return
        
        self._qr_backend = self._qr_provider.get_backend("scarlet_quantum_rings")
        
        if ( self._qr_backend is None ):
            raise Exception ("Unable to obtain backend. Please check the arguments")
            return
            
        super().__init__(
            provider = "Quantum Rings Provider",
            name= self._qr_backend.name,
            description = self._qr_backend.description,
            online_date = self._qr_backend.online_date,
            backend_version = self._qr_backend.backend_version,
            )

        if ( isinstance(kwargs.get('num_qubits'), int ) ):
            n = kwargs.get('num_qubits')
            if ( self._qr_backend.num_qubits >= n ):
                self._num_qubits = n
                self._coupling_map = self._qr_backend.get_coupling_map(self._num_qubits)
            else:
                raise Exception( f"Requested number of qubits {n} is more than the provisioned {self._qr_backend.num_qubits}." )
                return
        else:
             self._num_qubits = self._qr_backend.num_qubits
             self._coupling_map = self._qr_backend.coupling_map

        self._dt = self._qr_backend.dt
        self._dtm = self._qr_backend.dtm
       
        self._supported_gates = get_standard_gate_name_mapping()
        self._basis_gates = self._qr_backend._basis_gates
        
        self._build_target(self)
        return

    @staticmethod
    def _build_target(self) -> None:
        qubitproperties = []
        for i in range(self._num_qubits):
             qubitproperties.append(self._qr_backend.qubit_properties(i))
           
        self._target = Target(
            description = f"{self._qr_backend.description} with {self._num_qubits} qubits",
            num_qubits = self._num_qubits,
            dt = self._qr_backend.dt,
            qubit_properties = qubitproperties,
            concurrent_measurements = [list(range(self._num_qubits))],
            )

        for gate_name in self._basis_gates:
            if gate_name not in self._supported_gates:
                raise Exception(f"Provided basis gate {gate_name} is not valid.")
            gate = self._supported_gates[gate_name]
            if self._num_qubits < gate.num_qubits:
                raise Exception(f"Gate {gate_name} needs more qubits than the total qubits {self.num_qubits} enabled by the backend.")

            if gate.num_qubits > 1:
                qarg_set = self._coupling_map 
            else:
                qarg_set = range(self._num_qubits)
            

            props = {}
            for qarg in qarg_set:
                if isinstance(qarg, int):
                    key = (qarg,)  
                else:
                    key = (qarg[0], qarg[1])
                    
                props[key] = None

            self._target.add_instruction(gate, properties = props, name = gate_name)

        self._target.add_instruction(IfElseOp, name="if_else")
        self._target.add_instruction(WhileLoopOp, name="while_loop")
        self._target.add_instruction(ForLoopOp, name="for_loop")
        self._target.add_instruction(SwitchCaseOp, name="switch_case")
        self._target.add_instruction(BreakLoopOp, name="break")
        self._target.add_instruction(ContinueLoopOp, name="continue")
                  
        return

                    
    @property
    def target(self) -> Target:
        return self._target

    @classmethod
    def _default_options(cls) -> Options:
        op = Options(
            shots = 1024,
        	sync_mode = False,
        	performance = "HIGHESTEFFICIENCY",
        	quiet = True,
        	defaults = True,
        	generate_amplitude = False
        )
        return op


    #@classmethod
    def run(self, run_input, **run_options) -> QrJobV1:
        if not isinstance(run_input, QuantumCircuit):
            raise Exception( "Invalid argument passed for Quantum Circuit.")
            return
        # Parse the circuit and figure out the largest number of qubits required
        max_qubit = -1
        for instruction in run_input:
            for i in range (len(instruction.qubits)):
                if (instruction.qubits[i]._index > max_qubit):
                    max_qubit = instruction.qubits[i]._index
        if ( -1 == max_qubit ):
            raise Exception( "Submitted quantum circuit does not use any qubits")
            return
        max_qubit += 1        # bump this to pass as argument

        #TODO: Check control loops
        qreg = QuantumRingsLib.QuantumRegister(max_qubit, "q")
        creg = QuantumRingsLib.ClassicalRegister(max_qubit, "meas")
        qc = QuantumRingsLib.QuantumCircuit(qreg, creg, name = run_input.name,  global_phase = run_input.global_phase)

        #
        # We expect the transpiler to do a decent jobs of using required qubits and classical bits
        # for each instruction properly.
        # So they are not value checked
        #

        QrTranslator.translate_quantum_circuit(run_input, qc)
        
        
        #
        # parse the arguments and pickup the run parameters
        #
        
        if "shots" in run_options:
            shots = run_options.get("shots")
            if not isinstance(shots, int):
                raise Exception( "Invalid argument for shots")
                return
            if ( shots <= 0 ):
                raise Exception( "Invalid argument for shots")
                return
        else:
            shots = self._default_options().shots
            
        if "sync_mode" in run_options:
            sync_mode = run_options.get("sync_mode")
            if not isinstance(sync_mode, bool):
                raise Exception( "Invalid argument for sync_mode")
                return
        else:
            sync_mode = self._default_options().sync_mode

        if "performance" in run_options:
            performance = run_options.get("mperformance")
            performance = performance.upper()
            if (performance not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "LIBERAL"] ):
                raise Exception( "Invalid argument for performance")
                return
        else:
            performance = self._default_options().performance

        if "quiet" in run_options:
            quiet = run_options.get("quiet")
            if not isinstance(quiet, bool):
                raise Exception( "Invalid argument for quiet")
                return
        else:
            quiet = self._default_options().quiet

        if "generate_amplitude" in run_options:
            generate_amplitude = run_options.get("generate_amplitude")
            if not isinstance(generate_amplitude, bool):
                raise Exception( "Invalid argument for generate_amplitude")
                return
        else:
            generate_amplitude = self._default_options().generate_amplitude

        log_file = ""
        if "file" in run_options:
            log_file = run_options.get("file")

        if ("" == log_file):
            generate_amplitude = False
        
        job = self._qr_backend.run(qc, shots = shots, sync_mode = sync_mode, performance = performance, quiet = quiet, file = log_file)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        my_job = QrJobV1(self._qr_backend, job)
        return my_job

    def job_call_back(self, job_id, state, job) -> None:
        pass

    @property
    def max_circuits(self) -> int:
        return self._qr_backend.max_circuits
    
    @property
    def num_qubits(self) -> int:
        return self._num_qubits


