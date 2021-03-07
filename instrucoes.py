class Instrucoes:
    def __init__(self, tipo, registrador_destino, input_1, input_2,pc_counter):
        self.tipo = tipo
        self.registrador_destino = registrador_destino
        self.input_1 = input_1
        self.input_2 = input_2
        self.estagio = 0
        self.pc_counter=pc_counter



class Core_HazardControl:
    def __init__(self):
        self.tempoTotal = 0
        self.clock_cycle_time = 200
        self.pipeline = [None, None, None, None, None]
        self.isBranchTaken = 0
        self.ciclo_counter = 0
        self.pipelineIsNotEmpty = 1
        self.pc_counter_global = 0

        

    def branchIsNotTaken(self, i):
        print(f"{self.pipeline[i].registrador_destino[1]} e {self.pipeline[i].input_1[1]}")
        if self.pipeline[i].registrador_destino[1] == self.pipeline[i].input_1[1]:
            self.isBranchTaken = 1
            self.pipeline[0] = "FLUSH" 
            self.pipeline[1] = "FLUSH"
            self.pc_counter_global = self.pipeline[i].input_2 + self.pipeline[i].pc_counter
            print("FALHA CRITICA! O BRANCH FOI TOMADO")
            print("LIMPANDO O PIPELINE")
        else:
            self.isBranchTaken = 0


    def execution(self, i, dependencia):
        if self.pipeline[i].tipo == "add":
            self.pipeline[i].registrador_destino[1] = self.pipeline[i].input_1[1] + self.pipeline[i].input_2[1]
        elif self.pipeline[i].tipo == "sub":
            self.pipeline[i].registrador_destino[1] = self.pipeline[i].input_1[1] - self.pipeline[i].input_2[1]
        elif self.pipeline[i].tipo == "mult":
            self.pipeline[i].registrador_destino[1] = self.pipeline[i].input_1[1] * self.pipeline[i].input_2[1]  
        self.bypass(i, dependencia)
        

    def bypass(self, i, dependencia):
        print("DEPENDENCIA DETECTADA! BYPASSING")
        print(f"BYPASS DO RESULTADO DO REGISTRADOR {self.pipeline[i].registrador_destino[0]} DA INSTRUÇÃO {self.pipeline[i].tipo} PARA A ORIGEM DA PROXIMA INSTRUÇÃO A SER EXECUTADA {self.pipeline[i-1].tipo}")
        if dependencia == 0:
            self.pipeline[i-1].input_1[1] = self.pipeline[i].registrador_destino[1]
        elif dependencia == 1:
            self.pipeline[i-1].input_2[1] = self.pipeline[i].registrador_destino[1]
        elif dependencia == 2:
            self.pipeline[i-1].registrador_destino[1] = self.pipeline[i].registrador_destino[1]
            print(self.pipeline[i].registrador_destino[1])
        



    #Coloca a primeira instrução no "IF" do pipeline
    def init_datapath(self, memoria_de_instrucoes):
        try:
            while self.pipelineIsNotEmpty != 0:
                self.ciclo_counter += 1
                if self.pc_counter_global < len(memoria_de_instrucoes):
                    self.pipeline[0] = memoria_de_instrucoes[self.pc_counter_global]
                    self.pc_counter_global+=1
                    self.printEstagioAtual()
                    self.dataHazardControl()
                else:
                    self.printEstagioAtual()
                    self.dataHazardControl()
                for i in self.pipeline:
                    if i != None:
                        self.pipelineIsNotEmpty = 1
                        break
                    else:
                        self.pipelineIsNotEmpty = 0
            return 1
        except:
            return 2


        
        
    def dataHazardControl(self):
        for i in range (len(self.pipeline)-1, -1, -1):
            if i == 2 and self.pipeline[i] != None and self.pipeline[i] != "FLUSH" and self.pipeline[i].tipo == "beq":
                self.branchIsNotTaken(i)
            elif i == 2 and self.pipeline[i] != None and self.pipeline[i-1] != None and self.pipeline[i] != "FLUSH" and self.pipeline[i].tipo != "beq":    
                if self.pipeline[i].registrador_destino[0] == self.pipeline[i-1].input_1[0]:
                    self.execution(i, 0)
                elif self.pipeline[i-1].tipo != "beq" and self.pipeline[i].registrador_destino[0] == self.pipeline[i-1].input_2[0]:
                    self.execution(i, 1)
                elif self.pipeline[i-1].tipo == "beq" and self.pipeline[i].registrador_destino[0] == self.pipeline[i].registrador_destino[0]:
                    self.execution(i, 2) 

            self.incrementa_estagio(i)


    def incrementa_estagio(self, i):
        if self.pipeline[i] != None and i+1 < 5:
            self.pipeline[i+1] = self.pipeline[i]
            self.pipeline[i] = None
                    
        elif self.pipeline[i] != None and i+1 == 5:
            self.pipeline[i] = None
    



    def printEstagioAtual(self):
        print("------------------------------------")
        print(f"Ciclo número {self.ciclo_counter}")
        print("------------------------------------")
        for i in range(0, len(self.pipeline), 1):
            if self.pipeline[i] != None:
                if self.pipeline[i] == "FLUSH":
                    if i == 0:
                        print(f"FLUSH no estágio FETCH.")
                    elif i == 1:
                        print(f"FLUSH no estágio DECODE.")
                    elif i == 2:
                        print(f"FLUSH no estágio EXECUTE.")
                    elif i == 3:
                        print(f"FLUSH no estágio MEMORY.")
                    elif i == 4:
                        print(f"FLUSH no estágio WRITE-BACK.")
                else: 
                    if i == 0:
                        print(f"A instrução {self.pipeline[i].tipo} está no estágio FETCH.")
                    elif i == 1:
                        print(f"A instrução {self.pipeline[i].tipo} está no estágio DECODE.")
                    elif i == 2:
                        print(f"A instrução {self.pipeline[i].tipo} está no estágio EXECUTE.")
                    elif i == 3:
                        print(f"A instrução {self.pipeline[i].tipo} está no estágio MEMORY.")
                    elif i == 4:
                        print(f"A instrução {self.pipeline[i].tipo} está no estágio WRITE-BACK.")
        print("")
        

