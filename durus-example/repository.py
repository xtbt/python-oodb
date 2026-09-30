"""
Capa de acceso a datos del Auto Repair Shop (Durus).

Encapsula el FileStorage y la Connection de Durus, y expone metodos
para registrar y consultar entidades. Igual que ZODB, Durus persiste
automaticamente los objetos referenciados y las listas persistentes;
no hace falta resolver IDs manualmente.
"""

import logging
import os
from typing import List, Union

from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict

from models import Car, Motorcycle, Mechanic, Part, ServiceOrder

Vehicle = Union[Car, Motorcycle]

# --- Durus registra cada commit en el logger 'durus' a nivel INFO ---
# Se sube el nivel a WARNING para no ensuciar la salida de la demo.
logging.getLogger("durus").setLevel(logging.WARNING)


class RepairShop:
    def __init__(self, db_path: str = "data/shop.durus"):
        # --- Crear el directorio de datos si no existe ---
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.storage = FileStorage(db_path)
        self.connection = Connection(self.storage)
        self.root = self.connection.get_root()

        # --- Inicializar contenedores (PersistentDict) si no existen todavia ---
        if "cars" not in self.root:
            self.root["cars"] = PersistentDict()
        if "motorcycles" not in self.root:
            self.root["motorcycles"] = PersistentDict()
        if "mechanics" not in self.root:
            self.root["mechanics"] = PersistentDict()
        if "parts" not in self.root:
            self.root["parts"] = PersistentDict()
        if "orders" not in self.root:
            self.root["orders"] = PersistentDict()
        self.connection.commit()

        self.cars = self.root["cars"]
        self.motorcycles = self.root["motorcycles"]
        self.mechanics = self.root["mechanics"]
        self.parts = self.root["parts"]
        self.orders = self.root["orders"]

        self._next_id = {"car": 1, "motorcycle": 1, "mechanic": 1, "part": 1, "order": 1}

    def close(self):
        # --- En Durus se cierra el storage; la connection no tiene close() ---
        self.storage.close()

    def _commit(self):
        # --- Las transacciones en Durus son explicitas, igual que en ZODB ---
        self.connection.commit()

    # ------------------------------------------------------------------
    # Altas
    # ------------------------------------------------------------------
    def register_car(self, plate, make, model, year, door_count) -> int:
        car = Car(plate=plate, make=make, model=model, year=year, door_count=door_count)
        car_id = self._next_id["car"]
        self.cars[car_id] = car
        self._next_id["car"] += 1
        self._commit()
        return car_id

    def register_motorcycle(self, plate, make, model, year, engine_displacement_cc) -> int:
        motorcycle = Motorcycle(
            plate=plate, make=make, model=model, year=year,
            engine_displacement_cc=engine_displacement_cc,
        )
        motorcycle_id = self._next_id["motorcycle"]
        self.motorcycles[motorcycle_id] = motorcycle
        self._next_id["motorcycle"] += 1
        self._commit()
        return motorcycle_id

    def register_mechanic(self, name, specialty) -> int:
        mechanic = Mechanic(name=name, specialty=specialty)
        mechanic_id = self._next_id["mechanic"]
        self.mechanics[mechanic_id] = mechanic
        self._next_id["mechanic"] += 1
        self._commit()
        return mechanic_id

    def register_part(self, name, price) -> int:
        part = Part(name=name, price=price)
        part_id = self._next_id["part"]
        self.parts[part_id] = part
        self._next_id["part"] += 1
        self._commit()
        return part_id

    def create_service_order(
        self,
        order_number: str,
        vehicle: Vehicle,
        mechanic: Mechanic,
        parts: List[Part],
        description: str,
        labor_cost: float,
        status: str = "open",
    ) -> int:
        # --- Aqui se guardan objetos reales, no IDs (referencia directa) ---
        order = ServiceOrder(
            order_number=order_number,
            vehicle=vehicle,
            mechanic=mechanic,
            parts=parts,
            description=description,
            status=status,
            labor_cost=labor_cost,
        )
        order_id = self._next_id["order"]
        self.orders[order_id] = order
        self._next_id["order"] += 1
        self._commit()
        return order_id

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def get_car(self, car_id: int) -> Car:
        return self.cars.get(car_id)

    def get_motorcycle(self, motorcycle_id: int) -> Motorcycle:
        return self.motorcycles.get(motorcycle_id)

    def get_mechanic(self, mechanic_id: int) -> Mechanic:
        return self.mechanics.get(mechanic_id)

    def get_part(self, part_id: int) -> Part:
        return self.parts.get(part_id)

    def get_order(self, order_id: int) -> ServiceOrder:
        return self.orders.get(order_id)

    def get_all_orders(self) -> List[ServiceOrder]:
        return list(self.orders.values())

    def total_cost(self, order: ServiceOrder) -> float:
        parts_cost = sum(p.price for p in order.parts)
        return order.labor_cost + parts_cost

    def print_order(self, order: ServiceOrder):
        # --- Acceso directo a los objetos referenciados, sin resolver IDs ---
        print(f"Order {order.order_number} [{order.status}]")
        print(f"  Vehicle: {order.vehicle.description()}")
        print(f"  Mechanic: {order.mechanic.name} ({order.mechanic.specialty})")
        print(f"  Description: {order.description}")
        print("  Parts:")
        for p in order.parts:
            print(f"    - {p.name}: ${p.price:,.2f}")
        print(f"  Labor cost: ${order.labor_cost:,.2f}")
        print(f"  Total cost: ${self.total_cost(order):,.2f}")
