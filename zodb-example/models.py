"""
Data model for the Auto Repair Shop example (ZODB).

Conceptos ilustrados en este archivo:
  - Herencia: "Vehicle" es la clase base con los campos y comportamiento
    comunes; "Car" y "Motorcycle" la extienden y agregan sus propios
    campos. En ZODB la herencia es nativa de Python: cualquier clase
    que herede de Persistent se puede guardar en la BD.
  - Referencias entre objetos: "ServiceOrder" mantiene referencias
    directas a los objetos Vehicle y Mechanic (no solo IDs). ZODB
    maneja automaticamente la persistencia de estas referencias.
  - Listas dentro de un objeto: ServiceOrder.parts es una lista
    persistente (PersistentList) que contiene objetos Part. ZODB
    persiste automaticamente la lista y sus elementos.
  - Persistencia: todo objeto que hereda de Persistent se guarda
    automaticamente en la BD cuando se modifica y se hace commit().
"""

from persistent import Persistent
from persistent.list import PersistentList


class Vehicle(Persistent):
    """Clase base para vehiculos.

    Define los campos y el comportamiento comun a todo vehiculo que
    entra al taller. Las subclases heredan estos campos.
    """

    def __init__(self, plate="", make="", model="", year=0):
        self.plate = plate
        self.make = make
        self.model = model
        self.year = year

    def description(self) -> str:
        return f"{self.make} {self.model} ({self.year}) - plate {self.plate}"

    def kind(self) -> str:
        return self.__class__.__name__


class Car(Vehicle):
    def __init__(self, plate="", make="", model="", year=0, door_count=0):
        super().__init__(plate, make, model, year)
        self.door_count = door_count

    def description(self) -> str:
        return f"[Car] {super().description()} - {self.door_count} doors"


class Motorcycle(Vehicle):
    def __init__(self, plate="", make="", model="", year=0, engine_displacement_cc=0):
        super().__init__(plate, make, model, year)
        self.engine_displacement_cc = engine_displacement_cc

    def description(self) -> str:
        return f"[Motorcycle] {super().description()} - {self.engine_displacement_cc}cc"


class Mechanic(Persistent):
    def __init__(self, name="", specialty=""):
        self.name = name
        self.specialty = specialty


class Part(Persistent):
    def __init__(self, name="", price=0.0):
        self.name = name
        self.price = price


class ServiceOrder(Persistent):
    def __init__(
        self,
        order_number="",
        vehicle=None,
        mechanic=None,
        parts=None,
        description="",
        status="open",
        labor_cost=0.0,
    ):
        self.order_number = order_number
        # --- Referencia directa al objeto Vehicle (Car o Motorcycle) ---
        self.vehicle = vehicle
        # --- Referencia directa al objeto Mechanic ---
        self.mechanic = mechanic
        # --- Lista persistente de objetos Part (no solo IDs) ---
        # Se usa PersistentList para que ZODB detecte cambios en la lista.
        self.parts = PersistentList(parts or [])
        self.description = description
        self.status = status
        self.labor_cost = labor_cost
