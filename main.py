from instrucoes import *


def main():
    
    # add $s0, $s2, $s3
    # add $s1, $s0, $s4
    # sub $t1, $t3, $s7
    # beq $t3, $t5, 4 
    # mult $s8, $t2, $t5
    # add $s2, $s2, $s3
    # sub $t3, $t4, $t5

    #Declaração das instruções.
    add_1 = Instrucoes("add", ["$s0", None], ["$s2", 5], ["$s3", 2], 0)
    add_2 = Instrucoes("mult", ["$s1", None], ["$s0", None], ["$s3", 2], 1)
    sub_1 = Instrucoes("sub", ["$t1", None], ["$t3", 2], ["$s7", 2], 2)
    beq_1 = Instrucoes("beq", ["$t1", None], ["$t5", 0], 2, 3)
    mult_1 = Instrucoes("mult", ["$s8", None], ["$t2", 5], ["$s3", 2], 4)
    add_3 = Instrucoes("add", ["$s0", None], ["$s2", 5], ["$s3", 2], 5)
    sub_2 = Instrucoes("sub", ["$t3", None], ["$t4", 5], ["$t5", 2], 6)
    sub_3 = Instrucoes("sub", ["$t3", None], ["$t4", 5], ["$t5", 2], 7)

    core = Core_HazardControl() 
    if(core.init_datapath([add_1, add_2, sub_1, beq_1, mult_1, add_3, sub_2, sub_3])):
        print("Execução finalizada com sucesso.")
        print(f"Quantidade de ciclos: {core.ciclo_counter}")
        print(f"Tempo de execução de {core.clock_cycle_time*core.ciclo_counter}ps")
    else:
        print("Falha na execução!")
    
 
    

if __name__ == "__main__":
    main()



