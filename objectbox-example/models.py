"""
Data model for the Auto Repair Shop example (ObjectBox).

Conceptos ilustrados en este archivo:
  - Herencia: "Vehicle" es la clase base con los campos y comportamiento
    comunes; "Car" y "Motorcycle" la extienden y agregan sus propios
    campos. ObjectBox no soporta herencia de entidades como tal (cada
    @Entity genera su propia "tabla"/Box), pero al declarar las
    propiedades compartidas SIN parentesis (p. ej. `plate = String`)
    en la clase base, el decorador @Entity las detecta via la cadena
    de herencia de Python y las materializa en cada subclase.
  - Referencias entre objetos: como esta version de ObjectBox para
    Python todavia no implementa relaciones nativas (ToOne/ToMany),
    "ServiceOrder" guarda los IDs del vehiculo y del mecanico, y la
    resolucion del objeto real se hace "a mano" con los Box
    correspondientes (ver repository.py).
  - Listas dentro de un objeto: ServiceOrder.part_ids es una
    Int64List con los IDs de las Part (refacciones) utilizadas.
  - Persistencia: todo objeto guardado con Box.put() sobrevive al
    cierre del Store y puede leerse de nuevo en otra ejecucion.
"""

from objectbox import Entity, Id, String, Int32, Int64, Float64, Int64List


class Vehicle:
    """Clase base (no es una Entity de ObjectBox por si misma).

    Define los campos y el comportamiento comun a todo vehiculo que
    entra al taller. Las subclases que si se registran como @Entity
    heredan estos campos.
    """

    id = Id
    plate = String
    make = String
    model = String
    year = Int32

    def description(self) -> str:
        return f"{self.make} {self.model} ({self.year}) - plate {self.plate}"

    def kind(self) -> str:
        return self.__class__.__name__


@Entity()
class Car(Vehicle):
    door_count = Int32

    def description(self) -> str:
        return f"[Car] {super().description()} - {self.door_count} doors"


@Entity()
class Motorcycle(Vehicle):
    engine_displacement_cc = Int32

    def description(self) -> str:
        return f"[Motorcycle] {super().description()} - {self.engine_displacement_cc}cc"


@Entity()
class Mechanic:
    id = Id
    name = String
    specialty = String


@Entity()
class Part:
    id = Id
    name = String
    price = Float64


@Entity()
class ServiceOrder:
    id = Id
    order_number = String

    # --- "Referencias" manuales a otros objetos ---
    # Como no hay ToOne nativo, guardamos el tipo + id del vehiculo
    # para saber en que Box buscarlo despues.
    vehicle_type = String
    vehicle_id = Int64
    mechanic_id = Int64

    # --- Lista dentro del objeto ---
    # IDs de las refacciones (Part) usadas en esta orden.
    part_ids = Int64List

    description = String
    status = String
    labor_cost = Float64
