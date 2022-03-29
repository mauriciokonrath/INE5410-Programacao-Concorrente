from threading import Thread
from time import sleep
from random import randint

import init
from atracao import *
from equipamentos import *


class Cliente(Thread):
    '''
        Os clientes (frequentadores do parque) realizam as seguintes ações:
        - Vestir os equipamentos de proteção (macacão, luvas, capacete)
        - Ir a uma das atrações:
            - Pista de patinação no gelo:
                - Pegar patins
                - Aguardar vaga na pista
                - Patinar
            - Teleférico:
                - Pagar uma cadeira livre
                - Subir a montanha
                - Ir para uma das pistas ou permanecer no teleférico
            - Pista de snowboad:
                - Pegar uma prancha
                - Aguardar vaga
                - Descer a montanha
                - Devolver equipamento, caso deixe a atração
            - Pista de esqui:
                - Pegar esquis
                - Aguardar vaga
                - Descer a montanha
                - Devolver equipamento, caso deixe a atração
            - Pistas de trenó (skeleton):
                - Pegar trenó
                - Aguardar pista livre
                - Descer a montanha
                - Devolver o equipamento
            - Pistas de bobsled:
                - Formar dupla
                - Pegar bobsled
                - Aguardar pista livre 
                - Descer a montanha
                - Devolver o equipamento
        - Decidir aleatoriamente se permanece, se vai para outra atração ou vai embora

        Cada uma dessas ações corresponde a um método do cliente. A sua responsabilidade 
        é desenvolver os comportamentos dentro dos métodos do cliente de modo que ele se
        comporte conforme a especificação contida no Moodle.

        Esses métodos são chamados no método run() da classe Cliente.
 
        Observação: Comente no código qual o objetivo de uma dada operação, 
        ou conjunto de operações, para facilitar a correção do trabalho.           
    '''
    # Construtor do cliente
    # blah blah ALTERADO em 5/03 (correção do comentário)
    def __init__(self, id):
        self.id     = id
        self.pega_bob_dupla = False

        super().__init__(name=("Cliente " + str(id)))
        # NOVO 

    # Função que imprime mensagens de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')

    # Representação do cliente nas mensagens de log
    def __repr__(self):
        return self.name

    # Comportamento do cliente
    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS ABAIXO.
        '''
        self.log("Entrou no Winter Park.")

        self.pegar_equip_protecao()

        while True:
            if randint(1,3) == 1:
                # Vai para pista de patinação
                self.pegar_patins()
                self.aguardar_lugar_pista()
                while True:
                    self.patinar()
                    if randint(1,3) == 1:
                        break
                self.devolver_patins()
            else:
                # Pega o teleférico para subir a montanha
                self.pegar_teleferico()
                self.aguardar_subida()
                if randint(1,5) == 1:
                    # Desce de teleférico
                    self.aguardar_descida()
                    self.sair_teleferico()
                else:
                    self.sair_teleferico()
                    if randint(1,2) == 1:
                    # Vai para o lado sul - esqui e snowboard
                        if randint(1,2) == 1:
                            # Esquiar
                            self.pegar_esquis()
                            while True:
                                self.aguardar_lugar_montanha_sul()  
                                self.descer_esquiando()  
                                if randint(1,2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()             # ALTERADO 2/03         
                                else:
                                    self.devolver_esquis()
                                    break
                        else:
                            # Sandboard
                            self.pegar_snowboard()
                            while True:
                                self.aguardar_lugar_montanha_sul()  
                                self.descer_snowboard()   
                                if randint(1,2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()             # ALTERADO 2/03         
                                else:
                                    self.devolver_snowboard()
                                    break                                             
                    else:
                        # Vai para o lado norte - trenó e bobsled
                        if randint(1,3) == 1:
                            # Bobsled
                            while True:                         # ALTERADO 5/03
                                self.formar_dupla()             # ALTERADO 5/03
                                self.pegar_bobsled()            # ALTERADO 5/03
                                self.aguardar_pista_bobsled()  
                                self.descer_bobsled()  
                                self.devolver_bobsled()
                                if randint(1,2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()      # ALTERADO 2/03               
                                else:
                                    break                        
                        else:
                            # Trenó   
                            while True:                         # ALTERADO 5/03
                                self.pegar_treno()              # ALTERADO 5/03
                                self.aguardar_pista_treno()  
                                self.descer_treno()  
                                self.devolver_treno()
                                if randint(1,2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()      # ALTERADO 2/03               
                                else:
                                    break                   

            if randint(1,5) == 1: 
                # Devolve o kit de equipamentos de proteção
                self.devolver_equip_protecao()
                # Vai embora
                self.log("Saiu do Winter Park.")

                return

    # Simula o tempo de uso de uma atração
    def tempo_atracao(self):
        sleep(randint(init.tempo_atracao_min, init.tempo_atracao_max) * init.unidade_de_tempo)
        
    # Cliente pega um kit com os equipamentos de proteção
    def pegar_equip_protecao(self):
        # FUNCIONARIO 0 ENTREGA UM EQUIPAMENTO DE PROTEÇÃO
        self.equip_atual = init.funcionarios[0].entrega_equipamento()
        
        self.log("Pegou um kit com equipamentos de proteção.")
        
    # Cliente devolve um kit com os equipamentos de proteção
    def devolver_equip_protecao(self):
        # FUNCIONARIO 0 RECEBE UM EQUIPAMENTO DE PROTEÇÃO
        init.funcionarios[0].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[0].release()
        self.log("Devolveu um kit com equipamentos de proteção.")


    # Cliente pega um par de patins para usar a pista de patinação
    def pegar_patins(self):
        # FUNCIONARIO 1 ENTREGA EQUIPAMENTO DE PATINS
        self.equip_atual = init.funcionarios[1].entrega_equipamento()
        self.log("Pegou um par de patins.")

    # Cliente patinando
    def patinar(self):
        self.log("Está patinando.")
        self.tempo_atracao()
        # APOS PATINAR (TEMPO DA ATRAÇÃO) CLIENTE CHAMA METODO DA ATRAÇÃO
        # QUE ELE SE ENCONTRA LIBERANDO UMA VAGA PARA PATINAR
        # SEMAFORO PRESENTE NO ARQUIVO ATRACOES.PY
        init.atracoes[0].sair_atracao()

    # Cliente devolver os patins que estava usando
    def devolver_patins(self):
        # FUNCIONARIO 1 RECEBE UM EUIPAMENTO DE PATINAÇÃO
        init.funcionarios[1].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[1].release()
        self.log("Devolveu um par de patins.")

    # Cliente aguarda que haja lugar na pista de patinação         
    def aguardar_lugar_pista(self):
        # CLIENTE AGUARDA UM LUGAR NA PISTA DE PATINAÇÃO DA SEGUINTE FORMA:
        # CHAMA O METODO DA ATRACAO 0 = PATINAÇÃO
        # METODO ENTRAR NA ATRACAO TEM UM SEMAFORO QUE CONTA QUANTOS CLIENTES É PERMITIDO
        # OCUPA UMA DAS VAGAS DA CAPACIDADE DA ATRACAO
        init.atracoes[0].entrar_atracao()
        self.log("Entrou na pista de patinação.")
        
        

    # Cliente aguarda um lugar no teleférico
    def pegar_teleferico(self):
        # SEGUE O RACIOCINIO DESCRITO NOS COMENTARIOS DO METODO def aguardar_lugar_pista(self):
        init.atracoes[1].entrar_atracao()
        self.log("Pegou cadeira no teleférico.")
        # APENAS MARCAM TEMPO DE SUBIDA E DESCIDA OS METODOS ABAIXO

    # Cliente deve aguardar a subida do teleférico
    def aguardar_subida(self):
        self.tempo_atracao() 
        self.log("Chegou ao topo da montanha de teleférico.")

    # Cliente deve aguardar a descida do teleférico 
    def aguardar_descida(self):
        self.tempo_atracao()     
        self.log("Desceu a montanha de teleférico.")

     # Cliente libera seu lugar no teleférico
    def sair_teleferico(self):
        self.log("Liberou uma cadeira no teleférico.")
        # AUMENTA EM 1 CAPACIDADE DO TELEFERICO
        init.atracoes[1].sair_atracao()
        
    # Cliente pega esquis
    def pegar_esquis(self):
        # PEGA DO FUNCIONARIO 2 UM EQUIP. DE ESQUIS
        self.equip_atual = init.funcionarios[2].entrega_equipamento()
        self.log("Pegou esquis.")

    # Cliente aguarda para poder esquiar na montanha
    def aguardar_lugar_montanha_sul(self): 
        # PEGA UMA VAGA DA MONTANHA SUL
        init.atracoes[2].entrar_atracao()
        self.log("Conseguiu lugar na montanha sul.")
      
    # Cliente desce a montanha esquiando
    def descer_esquiando(self):
        self.log("Começa a descer a montanha esquiando.")
        self.tempo_atracao()
        self.log("Terminou de descer a montanha esquiando.")
        # LIBERA UMA VAGA DA MONTANHA SUL
        init.atracoes[2].sair_atracao()

     # Cliente devolve os esquis
    def devolver_esquis(self):
        # FUNCIONARIO 2 RECEBE UM EQUIP. DE ESQUI
        init.funcionarios[2].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[2].release()
        self.log("Devolveu os esquis.")
        
    # Cliente pega uma prancha de snowboard
    def pegar_snowboard(self):
        # FUNCIONARIO 3 ENTREGA UM EQUIP. DE SNOWBOARD
        self.equip_atual = init.funcionarios[3].entrega_equipamento()
        self.log("Pegou um snowboard.")
        
    # Cliente desce a montanha com uma prancha de snowboard
    def descer_snowboard(self):
        self.log("Começou a descer a pista de snowboard.")       
        self.tempo_atracao()
        self.log("Desceu a pista de snowboard.")
        # APOS DESCER, CLIENTE SAI DA ATRAÇÃO
        init.atracoes[2].sair_atracao()

    # Cliente devolve uma prancha de snowboard
    def devolver_snowboard(self):
        # FUNCIONARIO 3 RECEBE UM EQUIP DE SNOWBOARD
        init.funcionarios[3].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[3].release()
        self.log("Devolveu um snowboard.")

    # Cliente aguarda formação da dupla
    def formar_dupla(self):
        # SEMAFORO PARA APENAS DUAS THREADS ENTRAREM NA REGIÃO CRITICA
        init.sem_apenas2.acquire()
        # MUTEX PARA SO UMA THREAD ESCREVER
        init.lock.acquire()
        init.contador_duplas += 1

        if init.contador_duplas < 2:
            nice = init.condition_dupla.wait(3)
            if not nice:
                self.log("Desistiu de esperar por uma dupla")
                init.contador_duplas = 0
            else:
                self.log("Formou uma dupla")
                init.contador_duplas = 0
        else:
            # APENAS ESSE CLIENTE PEGA EQUIPAMENTO
            self.pega_bob_dupla = True
            init.condition_dupla.notify()
        init.lock.release()
        init.sem_apenas2.release()
        
        

    # Cliente aguarda um bobsled livre para descer a montanha
    def pegar_bobsled(self):
        # FUNCIONARIO 4 ENTRA UM EQUIP DE BOBSLED
        if self.pega_bob_dupla:
            self.equip_atual = init.funcionarios[4].entrega_equipamento()
            self.log("Pegou um bobsled.")

    # Cliente aguarda uma pista de bobsled livre para descer a montanha
    def aguardar_pista_bobsled(self):
        # MUTEX QUE PERMITE APENAS 1 DESCIDA POR VEZ NA MONTANHA NORTE
        init.mutex_1_descida_norte.acquire()
        self.log("Aguarda por uma pista de bobsled.")

        init.atracoes[2].entrar_atracao()
        self.log("Conseguiu uma pista de bobsled.")

        init.mutex_1_descida_norte.release()

     # Cliente desce a montanha de bobsled
    def descer_bobsled(self):
        # SEMAFORO QUE PERMITE UMA DESCIDA POR VEZ
        init.sem_1_descida.acquire()
        
        self.log("Começou a descer a pista de bobsled.")

        init.atracoes[2].sair_atracao()

        self.log("Terminou de descer a pista de bobsled.")

        init.sem_1_descida.release()      
 
   # Cliente devolve o bobsled que usou para descer a montanha
    def devolver_bobsled(self):
        # FUNCIONARIO 4 RECEBE O QUIP DE BOBSLED
        init.funcionarios[4].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[4].release()
        self.log("Devolveu um bobsled.")

    # Cliente aguarda um trenó livre para descer a montanha
    def pegar_treno(self):
        # FUNCIONARIO 5 ENTREGA UM TRENÓ
        self.equip_atual = init.funcionarios[5].entrega_equipamento()
        self.log("Pegou um trenó.")

    # Cliente aguarda uma pista de trenó livre para descer a montanha
    def aguardar_pista_treno(self):
        # MUTEX QUE PROTEGE A ENTRADA DE UMA PESSOA POR VEZ NA MONTANHA
        init.mutex_1_descida_norte.acquire()
        self.log("Aguarda por uma pista de trenó.")
        init.atracoes[3].entrar_atracao()
        self.log("Conseguiu uma pista de trenó.")
        init.mutex_1_descida_norte.release()

     # Cliente desce a montanha de trenó
    def descer_treno(self):
        # SEMAFORO QUE PERMITE UMA DESCIDA POR VEZ
        init.sem_1_descida.acquire()
        self.log("Começou a descer a pista de trenó.")
        self.tempo_atracao()
        self.log("Terminou de descer a pista de trenó.") 
        init.atracoes[3].sair_atracao()

        init.sem_1_descida.release()
 
   # Cliente devolve o trenó que usou para descer a montanha
    def devolver_treno(self):
        # FUNCIONARIO 5 RECEBE UM EQUIP. TRENÓ
        init.funcionarios[5].recebe_equipamento(self.equip_atual)
        init.sem_limpezas[5].release()
        self.log("Devolveu um trenó.")