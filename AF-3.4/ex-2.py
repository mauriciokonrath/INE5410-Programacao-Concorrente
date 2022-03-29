from time import sleep
from random import randint
from threading import Thread, Semaphore

def produtor():
  global buffer
  for i in range(10):
    #decrementa o semaforo dos espaços
    sem_espaco.acquire()
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i)
    buffer.append(item)
    print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
    #incrementa o semaforo dos produtos
    sem_produtos.release()

def consumidor():
  global buffer
  for i in range(10):
    sem_produtos.acquire()
    # aguarda que haja um item para consumir 
    item = buffer.pop(0)
    print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
    sleep(randint(0,2))         # fica um tempo consumindo...
    #incrementa o semaforo dos espaços
    sem_espaco.release()

buffer = []
tam_buffer = 3
sem_espaco = Semaphore(tam_buffer)
sem_produtos = Semaphore(0)
#thread produtor
produtor = Thread(target=produtor) 
#thread consumidor
consumidor = Thread(target=consumidor) 
produtor.start()
consumidor.start()
produtor.join()
consumidor.join() 