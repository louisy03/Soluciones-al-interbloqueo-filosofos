import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, id, tenedores, semaforo_global, contador_comidas):
        super().__init__()
        self.id = id
        self.tenedor_izq = tenedores[id]
        self.tenedor_der = tenedores[(id + 1) % 5]
        self.semaforo_global = semaforo_global
        self.contador_comidas = contador_comidas

    def run(self):
        while self.contador_comidas[self.id] < 6:
            # Pensar
            time.sleep(random.uniform(0.5, 1.5))
            
            # Intentar comer
            self.semaforo_global.acquire()  # Evita que mas de 4 filosofos coman
            
            self.tenedor_izq.acquire()
            self.tenedor_der.acquire()
            
            # Comer
            self.contador_comidas[self.id] += 1
            print(f"Filosofo {self.id + 1} ha comido {self.contador_comidas[self.id]} veces")
            time.sleep(random.uniform(0.5, 1.0))
            
            # Liberar tenedores
            self.tenedor_izq.release()
            self.tenedor_der.release()
            self.semaforo_global.release()

def main():
    tenedores = [threading.Semaphore(1) for _ in range(5)]
    semaforo_global = threading.Semaphore(4)  # Solo 4 filosofos pueden comer a la vez
    contador_comidas = [0] * 5
    
    filosofos = [Filosofo(i, tenedores, semaforo_global, contador_comidas) for i in range(5)]
    
    for f in filosofos:
        f.start()
    
    for f in filosofos:
        f.join()
    
    print("Todos los filosofos han comido al menos 6 veces")

if __name__ == "__main__":
    main()
