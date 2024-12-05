from .confparser import *
from .vrtg import *
from .init_data_generator import *


def generator_test(configs, use_addr):
    operator_seq = generate_operator_sequence(configs)
    main_text_seq = add_operands(operator_seq, configs)
    main_text_seq = insert_vm_change_placeholders(main_text_seq, configs)
    vregs2init, xreg2init, vms2init = trace_uninitialzed_operands(main_text_seq)
    data_section, init_text_seq = init_data(vregs2init, xreg2init, vms2init, configs, use_addr)
    main_text_seq = replace_vm_change_placeholders(main_text_seq, data_section, use_addr)
    
    return data_section, init_text_seq, main_text_seq

