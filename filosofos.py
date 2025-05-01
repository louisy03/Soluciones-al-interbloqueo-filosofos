import threading
import time
import random
from datetime import datetime

class Filosofo(threading.Thread):
    def __init__(self, id, tenedores, semaforo_global, contador_comidas):
        super().__init__()
        self.id = id
        self.tenedor_izq = tenedores[id]
        self.tenedor_der = tenedores[(id + 1) % 5]
        self.semaforo_global = semaforo_global
        self.contador_comidas = contador_comidas

    def log(self, mensaje):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] Filosofo {self.id + 1}: {mensaje}")

    def run(self):
        while self.contador_comidas[self.id] < 6:
            self.log("Esta pensando.")
            time.sleep(random.uniform(0.5, 1.5))

            self.log("Tiene hambre e intenta sentarse a la mesa.")
            self.semaforo_global.acquire()
            self.log("Se sento. Intenta tomar el tenedor izquierdo.")
            self.tenedor_izq.acquire()
            self.log("Tomo el tenedor izquierdo. Intenta tomar el derecho.")
            self.tenedor_der.acquire()
            self.log("Tomo el tenedor derecho. Esta comiendo.")

            self.contador_comidas[self.id] += 1
            self.log(f"Ha comido {self.contador_comidas[self.id]} veces.")
            time.sleep(random.uniform(0.5, 1.0))

            self.log("Termino de comer. Suelta ambos tenedores.")
            self.tenedor_izq.release()
            self.tenedor_der.release()
            self.semaforo_global.release()

            self.log("Se levanta de la mesa y vuelve a pensar.\n")

def main():
    tenedores = [threading.Semaphore(1) for _ in range(5)]
    semaforo_global = threading.Semaphore(4)
    contador_comidas = [0] * 5

    filosofos = [Filosofo(i, tenedores, semaforo_global, contador_comidas) for i in range(5)]

    for f in filosofos:
        f.start()
    
    for f in filosofos:
        f.join()

    print("Todos los filosofos han comido al menos 6 veces.")

if __name__ == "__main__":
    main()
