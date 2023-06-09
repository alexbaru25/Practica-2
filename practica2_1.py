"""
Solution to the one-way tunnel
Esta versión limita el número de coches y de peatones que pasan seguidos, evitando que haya injusticias
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 100
NPED = 10
TIME_CARS = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRGIAN = (30, 10) # normal 1s, 0.5s
Seguidos_coches=20
Seguidos_peatones=5
class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.patata = Value('i', 0)
        self.n_north_car=Value('i',0)  #Número de coches pasando con direccion norte
        self.n_south_car= Value('i',0) #Número de coches pasando con direccion sur
        self.n_ped=Value('i',0)        #Número de peatones cruzando

        self.coche_seguidos = Value('i', 0)
        self.peatones_seguidos= Value('i', 0)
        self.contador_peatones= Value('i', 0)
        self.contador_coches= Value('i', 0)
        self.no_north_car = Condition(self.mutex)
        self.no_south_car = Condition(self.mutex)
        self.no_ped = Condition(self.mutex)
    
    #Determina si los peatones pueden pasar
    def pass_ped(self):
        if self.contador_coches.value == NCARS:
            return self.n_north_car.value == 0 and self.n_south_car.value == 0 
        else:
            return self.n_north_car.value == 0 and self.n_south_car.value == 0 and self.peatones_seguidos.value < Seguidos_peatones
    #Determina si los coches con direccion norte pueden pasar
    def pass_north(self):
        if self.contador_peatones.value == NPED:
            return self.n_south_car.value == 0 and self.n_ped.value == 0
        else:
            return self.n_ped.value == 0 and self.n_south_car.value == 0 and self.coche_seguidos.value < Seguidos_coches
    #Determina si los coches con direccion sur pueden pasar
    def pass_south(self):
        if self.contador_peatones.value == NPED:
            return self.n_north_car.value == 0 and self.n_ped.value == 0
        else:
            return self.n_ped.value == 0 and self.n_north_car.value == 0 and self.coche_seguidos.value < Seguidos_coches

    #Analiza si el coche con la direccion dada pasa, en caso de que no sea así el se bloquea hasta nuevo aviso
    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        if direction == NORTH:
            self.no_south_car.wait_for(self.pass_north)
            self.n_north_car.value +=1
            self.coche_seguidos.value += 1
            self.contador_coches.value += 1
            self.peatones_seguidos.value = 0
        else:
            self.no_north_car.wait_for(self.pass_south)
            self.n_south_car.value +=1
            self.coche_seguidos.value += 1
            self.contador_coches.value += 1
            self.peatones_seguidos.value = 0
        self.mutex.release()

    #Funcion que nos indica cuando un coche sale, y despierta a los peatones o los coches de la direccion contraria segun que casos    
    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.patata.value += 1
        if direction == NORTH:
            self.n_north_car.value -=1
            if self.n_north_car.value == 0:
                self.no_north_car.notify_all()
                self.no_ped.notify_all()
        else:
            self.n_south_car.value -=1
            if self.n_south_car.value == 0:
                self.no_south_car.notify_all()
                self.no_ped.notify_all()
        self.mutex.release()
        
    #Analiza si el peaton pasa, en caso de que no sea así el se bloquea hasta nuevo aviso 
    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.no_ped.wait_for(self.pass_ped)
        self.n_ped.value +=1
        self.contador_peatones.value +=1
        self.peatones_seguidos.value += 1
        self.coche_seguidos.value = 0
        #print(self.n_ped.value)
        self.mutex.release()

    #Funcion que nos indica cuando un peaton sale, y despierta a los coches de la direccion contraria segun que casos    
    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.n_ped.value -=1
        if self.n_ped.value == 0:
            self.no_north_car.notify_all()
            self.no_south_car.notify_all()
        #### código
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.patata.value}'

def delay_car_north(d=50) -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_CARS[0],TIME_IN_BRIDGE_CARS[1])/d)

def delay_car_south(d=40) -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_CARS[0],TIME_IN_BRIDGE_CARS[1])/d)

def delay_pedestrian(d=10) -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_PEDESTRGIAN[0],TIME_IN_BRIDGE_PEDESTRGIAN[1])/d)


def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")


def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(monitor) -> Monitor:
    cid = 0
    plst = []
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_CARS))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars = Process(target=gen_cars, args=(monitor,))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars.start()
    gped.start()
    gcars.join()
    gped.join()


if __name__ == '__main__':
    main()
