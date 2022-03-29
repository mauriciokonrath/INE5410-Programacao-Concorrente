from threading import Thread, Lock
from time import sleep

import init
from atracao import *
from equipamentos import *

class Funcionario(Thread):
    '''
        Funcionário deve realizar as seguintes ações:
        - Limpar os equipamentos.
        - Descansar.
        A sua responsabilidade é implementar os métodos com o comportamento do
        funcionário, respeitando as restrições impostas no enunciado do trabalho.
 
        Observação: Comente no código qual o objetivo de uma dada operação, 
        ou conjunto de operações, para facilitar a correção do trabalho.        
      
    '''

    # Construtor da classe Funcionario
    def __init__(self, id, equipamento, lock):
        self.id     = id
        self.trabalhando = False
        self.equipamento = equipamento
        self.lock_index = lock
        self.contador_limpos = 0

        super().__init__(name=("Funcionario " + str(id)))

    # Imprime mensagem de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')

    # Comportamento do Funcionario
    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS ABAIXO.
        '''
        self.log("Iniciando o expediente. Gerenciando equipamento "+self.equipamento.nome)
        self.trabalhando = True     


        cont_equip_limpos = 0
        while self.trabalhando == True :
            # IF PARA CONTROLAR O SEMAFORO QUE PERMITE A LIMPEZA
            # QUANDO O CONTADOR CHEGA NA QUANTIDADE DE EQUIPS LIMPOS ELE FICA TRAVADO POR SE TRATAR DE
            # UM SEMAFORO BINARIO E NÃO PROSSEGUE COM A EXECUÇÃO DO PROGRAMA
            
            init.sem_limpezas[self.lock_index].acquire()
            if self.trabalhando:
                self.limpar_equipamento()
                cont_equip_limpos += 1
            if cont_equip_limpos >= init.num_equip_turno:
                self.descansar()
                cont_equip_limpos = 0
                

        self.log("Terminando o expediente")

    # Funcionário limpa os equipamentos.
    def limpar_equipamento(self):
        self.contador_limpos += 1
        sleep(init.tempo_limpeza_equipamento * init.unidade_de_tempo)
        self.log(f"[{self.equipamento.nome}]: foi higienizado")
        

    # Funcionário entrega um equipamento para um cliente.
    def entrega_equipamento(self):
        # CASO O FUNCIONARIO ESTAJA DESCANSANDO ELE FICA PARADO AQUI ATE ACABAR O DESNCANSO
        while init.locks_func[self.lock_index].locked():
            pass
        # RESGATA UM EQUIP E O ENTREGA PARA O CLIENTE E RETORNA
        equip = self.equipamento.pegar_equipamento(self.equipamento)
        self.log("Entregou "+self.equipamento.nome+" para um cliente.")

        return equip

    # Funcionário recebe um equipamento.
    def recebe_equipamento(self, equip):
        # CASO O FUNCIONARIO ESTEJA NO DESCANSO NÃO PODE RECEBER UM EQUIP, ENTÃO FICA PARADO ESPERANDO O DESCANSO ACABAR
        while init.locks_func[self.lock_index].locked():
            pass
        # DEVOLVE UM EQUIPAMENTO A CONTAGEM DE QTDD EQUIPS
        #init.sem_limpezas[self.lock_index].release()
        
        self.equipamento.devolver_equipamento()
        self.log("Recebeu "+self.equipamento.nome+" de um cliente.")

    # Funcionário descansa durante um tempo
    def descansar(self):
        self.log("Hora do intervalo de descanso.")
        # LOGICA DE TRAVA DE RECEBER E ENTREGAR EQUIPAMENTOS
        init.locks_func[self.lock_index].acquire()

        sleep(init.tempo_descanso * init.unidade_de_tempo)
        self.log("Fim do intervalo de descanso.")

        init.locks_func[self.lock_index].release()

    def terminar(self):
        #libera o semaforo de limpesa quando não tem mais o que limpar e precisa terminar a execução
        init.sem_limpezas[self.lock_index].release()