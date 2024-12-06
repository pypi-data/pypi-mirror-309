from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.providers import JobStatus


import QuantumRingsLib


class QrTranslator:
    def __init__(self):
        pass

    def check_add_if_condition (
            gate, 
            operation
            ) -> None:
        if (None != operation.condition):
            creg_bit = operation.condition[0]._index
            creg_condition = operation.condition[1]
            gate.c_if(creg_bit, creg_condition)
        return
    
    
    def translate_qiskit_instruction(qc: QuantumRingsLib.QuantumCircuit, 
                        instruction,
                        qregs : list[QuantumRegister],
                        qubit_lookup_vector,
                        clbit_lookup_vector,
                        is_controlled : bool = False,
                        number_of_control_qubits = 0,
                        ignore_meas : bool = False,
                        is_at_root : bool = True, 
                        ) -> None:
        
        name = instruction.operation.name
        opn = instruction.operation
        remapped_qubit_list = []

        root_qubit_count = 0
        for j in range (len(qregs)):
            root_qubit_count += qregs[j].size
        root_qubit_list = [i for i in range(0, root_qubit_count)]

        if ( True == is_controlled ):
            for i in range (len(instruction.qubits)):
                if (instruction.qubits[i]._register.name == "control"):
                    remapped_qubit_list.append(qubit_lookup_vector[instruction.qubits[i]._index])
                elif (instruction.qubits[i]._register.name == "target"):
                    remapped_qubit_list.append(qubit_lookup_vector[number_of_control_qubits + instruction.qubits[i]._index])
                else:
                    remapped_qubit_list.append(qubit_lookup_vector[instruction.qubits[i]._index])
        else:
            if ( True == is_at_root ): #root_qubit_list == qubit_lookup_vector):
                # if we get here, we are probably placed directly on the root of the circuit (not inside or as a sub circuit)
                # try to fill the remap vector based on the qubit register names
                for i in range (len(instruction.qubits)):
                    reg_base = 0
                    for j in range (len(qregs)):
                        if ( instruction.qubits[i]._register.name == qregs[j].name ):
                            remapped_qubit_list.append(reg_base + instruction.qubits[i]._index)
                        reg_base += qregs[j].size

            # check if we were able to fill in the remap vector based on the above logic. If not, just fill from the lookup vector sent through the function
            if (len(instruction.qubits) != len(remapped_qubit_list)):
                remapped_qubit_list = []    # I dont know, if there will be partial fills from the above step.
                for i in range (len(instruction.qubits)):
                    remapped_qubit_list.append(qubit_lookup_vector[instruction.qubits[i]._index])

        # when we get here the remapped_qubit_list contains the list of qubits remapped in the order they appear in the instructions.
        
        # Now, the control qubits
        remapped_clbit_list = []
        for i in range (len(instruction.clbits)):
                remapped_clbit_list.append(clbit_lookup_vector[instruction.clbits[i]._index])

        
        #QrTranslator.print_instruction(instruction, qubit_lookup_vector, remapped_qubit_list)

        #
        # Instructions dispatcher
        #
    
        if (name == "h"):
            gate = qc.h(remapped_qubit_list[0])
        elif (name == "x"):
            gate = qc.x(remapped_qubit_list[0])
        elif (name == "id"):
            gate = qc.id(remapped_qubit_list[0])
        elif (name == "t"):
            gate = qc.t(remapped_qubit_list[0]) 
        elif (name == "s"):
            gate = qc.s(remapped_qubit_list[0]) 
        elif (name == "tdg"):
            gate = qc.tdg(remapped_qubit_list[0])
        elif (name == "sdg"):
            gate = qc.sdg(remapped_qubit_list[0])
        elif (name == "sx"):
            gate = qc.sx(remapped_qubit_list[0])
        elif (name == "sxdg"):
            gate = qc.sxdg(remapped_qubit_list[0])                  
        elif (name == "p"):
            gate = qc.p(instruction.params[0], remapped_qubit_list[0])   
        elif (name == "r"):
            gate = qc.r(instruction.params[0], instruction.params[1], remapped_qubit_list[0])   
        elif (name == "rx"):
            gate = qc.rx(instruction.params[0], remapped_qubit_list[0])   
        elif (name == "ry"):
            gate = qc.ry(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "rz"):
            gate = qc.rz(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "u"):
            gate = qc.u(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0])   
        elif (name == "y"):
            gate = qc.y(remapped_qubit_list[0])  
        elif (name == "z"):
            gate = qc.z(remapped_qubit_list[0])  
        elif (name == "delay"):
            gate = qc.delay(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "cx"):
            gate = qc.cx(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cy"):
            gate = qc.cy(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cz"):
            gate = qc.cz(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "ch"):
            gate = qc.ch(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cp"):
            gate = qc.cp(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "crx"):
            gate = qc.crx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])            
        elif (name == "cry"):
            gate = qc.cry(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])        
        elif (name == "crz"):
            gate = qc.crz(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "cs"):
            gate = qc.cs(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "csdg"):
            gate = qc.csdg(remapped_qubit_list[0], remapped_qubit_list[1])           
        elif (name == "csx"):
            gate = qc.csx(remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "cu"):
            gate = qc.cu(instruction.params[0], instruction.params[1], instruction.params[2], instruction.params[3], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "dcx"):
            gate = qc.dcx(remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "ecr"):
            gate = qc.ecr(remapped_qubit_list[0], remapped_qubit_list[1])                
        elif (name == "iswap"):
            gate = qc.iswap(remapped_qubit_list[0], remapped_qubit_list[1])   
        elif (name == "rxx"):
            gate = qc.rxx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "ryy"):
            gate = qc.ryy(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "rzx"):
            gate = qc.rzx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "rzz"):
            gate = qc.rzz(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "swap"):
            gate = qc.swap(remapped_qubit_list[0], remapped_qubit_list[1])   
        elif (name == "measure"):
            if ( False == ignore_meas):
                gate = qc.measure(remapped_qubit_list[0], instruction.clbits[0]._index)
        elif (name == "reset"):
            gate = qc.reset(remapped_qubit_list[0])   
        elif (name == "cu1"):
            gate = qc.cu1(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "cu3"):
            gate = qc.cu3(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "u1"):
            gate = qc.u1(instruction.params[0], remapped_qubit_list[0])
        elif (name == "u2"):
            gate = qc.u2(instruction.params[0], instruction.params[1], remapped_qubit_list[0])                
        elif (name == "barrier"):
            gate = qc.barrier(remapped_qubit_list)
        elif (name == "ms"):
            gate = qc.ms(instruction.params[0], remapped_qubit_list)
        elif (name == "rv"):
            gate = qc.rv(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0])
        elif (name == "mcp"):
            gate = qc.mcp(instruction.params[0], remapped_qubit_list[:-1], remapped_qubit_list[-1])
        elif (name == "rccx"):
            gate = qc.rccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "rcccx"):
            gate = qc.rcccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2], remapped_qubit_list[3])
        elif (name == "cswap"):
            gate = qc.cswap(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "ccx"):
            gate = qc.ccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "ccz"):
            gate = qc.ccz(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "mcx"):
            gate = qc.mcx(remapped_qubit_list[:-1], remapped_qubit_list[-1])
        else:
            #print(f"Gate: {name} is not dispatched.")
            return False
                
        QrTranslator.check_add_if_condition(gate, opn)
        return True


    def emit_quantum_circuit_(run_input : QuantumCircuit, 
                              qc: QuantumRingsLib.QuantumCircuit,
                              qregs : list[QuantumRegister],
                              qubit_lookup_vector,
                              clbit_lookup_vector,
                              is_controlled : bool = False,
                              number_of_control_qubits = 0,
                              ignore_meas : bool = False,
                              is_at_root : bool = True 
                              ) -> None:
        for instruction in run_input:
            
            if ( True == QrTranslator.translate_qiskit_instruction( qc, instruction, qregs, qubit_lookup_vector, clbit_lookup_vector, is_controlled, number_of_control_qubits, ignore_meas, is_at_root) ):
                continue

            # check if it is a non-standard gate
            if instruction.operation._standard_gate is None:
                gate_name_ = instruction.name
                is_this_gate_controlled_ = instruction.is_controlled_gate()
                if (True == is_this_gate_controlled_):
                    number_of_controls_in_this_gate_ = instruction.operation.num_ctrl_qubits
                else:
                    number_of_controls_in_this_gate_ = 0
                
                qubits_in_the_gate = []
                clbits_in_the_gate = []

                root_qubit_count = 0
                for j in range (len(qregs)):
                    root_qubit_count += qregs[j].size

                #
                # Construct the instructions under this gate into it
                #
                if ( True == is_this_gate_controlled_):

                    full_range_qubit = [i for i in range(0, root_qubit_count)]
                    full_range_clbit = [i for i in range(0, run_input.num_clbits)]

                    if ( True == is_at_root):
                        for i in range (len(instruction.qubits)):
                            qubits_in_the_gate.append(full_range_qubit[instruction.qubits[i]._index])
                    else:
                        for i in range (len(instruction.qubits)):
                            if (instruction.qubits[i]._register.name == "control"):
                                qubits_in_the_gate.append(qubit_lookup_vector[instruction.qubits[i]._index])
                            elif (instruction.qubits[i]._register.name == "target"):
                                qubits_in_the_gate.append(qubit_lookup_vector[number_of_control_qubits + instruction.qubits[i]._index])
                            else:
                                qubits_in_the_gate.append(qubit_lookup_vector[instruction.qubits[i]._index])
                
                    for i in range (len(instruction.clbits)):
                        clbits_in_the_gate.append(full_range_clbit[instruction.clbits[i]._index])

                    #print(f"gate_ ({gate_name_}) controlled: {is_this_gate_controlled_} Total Controls: {number_of_controls_in_this_gate_} Qubits: {qubits_in_the_gate} Clbits: {clbits_in_the_gate}")

                    QrTranslator.emit_quantum_circuit_(instruction.operation.definition,
                                              qc,
                                              qregs,
                                              qubits_in_the_gate,
                                              clbits_in_the_gate,
                                              is_this_gate_controlled_,
                                              number_of_controls_in_this_gate_,
                                              ignore_meas,
                                              False
                                             )
                else:
                    
                    full_range_qubit = [i for i in range(0, root_qubit_count)]
                    super_gate = ""

                    if ( full_range_qubit == qubit_lookup_vector):
                        super_gate = "SUPER"
                        for i in range (len(instruction.qubits)):
                            reg_base = 0
                            for j in range (len(qregs)):
                                if ( instruction.qubits[i]._register.name == qregs[j].name ):
                                    qubits_in_the_gate.append(reg_base + instruction.qubits[i]._index)
                                reg_base += qregs[j].size

                        for i in range (len(instruction.clbits)):
                            clbits_in_the_gate.append(clbit_lookup_vector[instruction.clbits[i]._index])
                        
                    else:   

                        for i in range (len(instruction.qubits)):
                            qubits_in_the_gate.append(qubit_lookup_vector[instruction.qubits[i]._index])
                    
                        for i in range (len(instruction.clbits)):
                            clbits_in_the_gate.append(clbit_lookup_vector[instruction.clbits[i]._index])

                    #print(f"{super_gate} gate_ ({gate_name_}) controlled: {is_this_gate_controlled_} Total Controls: {number_of_controls_in_this_gate_} Qubits: {qubits_in_the_gate} Clbits: {clbits_in_the_gate}")
   

                    QrTranslator.emit_quantum_circuit_(instruction.operation.definition,
                                              qc,
                                              qregs,
                                              qubits_in_the_gate, 
                                              clbits_in_the_gate, 
                                              is_this_gate_controlled_,
                                              number_of_controls_in_this_gate_,
                                              ignore_meas,
                                              False
                                             )
            else:
                raise Exception( f"Instruction {gate_name_} is not supported.")
        return
        
    def translate_quantum_circuit(run_input : QuantumCircuit, 
                                   qc: QuantumRingsLib.QuantumCircuit,
                                   ) -> None:
        qubit_lookup_vector = [i for i in range(0, run_input.num_qubits)]
        clbit_lookup_vector = [i for i in range(0, run_input.num_clbits)]

        QrTranslator.emit_quantum_circuit_(run_input,
                              qc,
                              run_input.qregs,
                              qubit_lookup_vector,
                              clbit_lookup_vector,
                              False,
                              0,
                              False,
                              True 
                              )
        return

    
    def translate_job_status(
            qr_status : QuantumRingsLib.JobStatus
            ) -> JobStatus:
        if (qr_status == QuantumRingsLib.JobStatus.INITIALIZING):
            return JobStatus.INITIALIZING
        elif (qr_status == QuantumRingsLib.JobStatus.QUEUED):
            return JobStatus.QUEUED
        elif (qr_status == QuantumRingsLib.JobStatus.VALIDATING):
            return JobStatus.VALIDATING
        elif (qr_status == QuantumRingsLib.JobStatus.RUNNING):
            return JobStatus.RUNNING
        elif (qr_status == QuantumRingsLib.JobStatus.CANCELLED):
            return JobStatus.CANCELLED
        elif (qr_status == QuantumRingsLib.JobStatus.DONE):
            return JobStatus.DONE
        elif (qr_status == QuantumRingsLib.JobStatus.ERROR):
            return JobStatus.ERROR
        else:
            return qr_status

    def print_instruction(instruction, 
                          lookup_vector=[],
                          remap_vector=[]
                          ) -> None:
        name = "\t" + instruction.operation.name
        name += '('
        for i in range (len(instruction.params)):
            name += '__,'
        name += ') '
        
        for i in range (len(instruction.qubits)):
            name += instruction.qubits[i]._register.name + '[' + str(instruction.qubits[i]._index) + '],'

        name = name[:-1]
        
        if ( len(instruction.clbits)):
            name += " -> "

            for i in range (len(instruction.clbits)):
                name += instruction.clbits[i]._register.name + '[' + str(instruction.clbits[i]._index) + '],'

            name = name[:-1]

        print(f"Instruction: {name} Lookup Vector: {lookup_vector} Remap Vector: {remap_vector}")
    
    def analyze_instructions(run_input) -> None:
        for instruction in run_input:
            QrTranslator.print_instruction(instruction) 