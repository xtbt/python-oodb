"""
Capa de acceso a datos del Auto Repair Shop (ObjectBox).

Encapsula el Store de ObjectBox y los Box de cada entidad, y ademas
resuelve "a mano" las referencias entre objetos (vehiculo y mecanico
de una orden de servicio, y las refacciones usadas), ya que esta
version de ObjectBox para Python no trae relaciones nativas.
"""

from typing import List, Union

from objectbox import Store

from models import Car, Motorcycle, Mechanic, Part, ServiceOrder

Vehicle = Union[Car, Motorcycle]

VEHICLE_CAR = "Car"
VEHICLE_MOTORCYCLE = "Motorcycle"


class RepairShop:
    def __init__(self, directory: str = "data"):
        self.store = Store(directory=directory)
        self.box_car = self.store.box(Car)
        self.box_motorcycle = self.store.box(Motorcycle)
        self.box_mechanic = self.store.box(Mechanic)
        self.box_part = self.store.box(Part)
        self.box_order = self.store.box(ServiceOrder)

    def close(self):
        self.store.close()

    # ------------------------------------------------------------------
    # Altas
    # ------------------------------------------------------------------
    def register_car(self, plate, make, model, year, door_count) -> int:
        car = Car(plate=plate, make=make, model=model, year=year, door_count=door_count)
        return self.box_car.put(car)

    def register_motorcycle(self, plate, make, model, year, engine_displacement_cc) -> int:
        motorcycle = Motorcycle(
            plate=plate, make=make, model=model, year=year,
            engine_displacement_cc=engine_displacement_cc,
        )
        return self.box_motorcycle.put(motorcycle)

    def register_mechanic(self, name, specialty) -> int:
        return self.box_mechanic.put(Mechanic(name=name, specialty=specialty))

    def register_part(self, name, price) -> int:
        return self.box_part.put(Part(name=name, price=price))

    def create_service_order(
        self,
        order_number: str,
        vehicle_type: str,
        vehicle_id: int,
        mechanic_id: int,
        part_ids: List[int],
        description: str,
        labor_cost: float,
        status: str = "open",
    ) -> int:
        order = ServiceOrder(
            order_number=order_number,
            vehicle_type=vehicle_type,
            vehicle_id=vehicle_id,
            mechanic_id=mechanic_id,
            part_ids=part_ids,
            description=description,
            status=status,
            labor_cost=labor_cost,
        )
        return self.box_order.put(order)

    # ------------------------------------------------------------------
    # Resolucion manual de referencias (no hay ToOne/ToMany nativos)
    # ------------------------------------------------------------------
    def get_vehicle(self, vehicle_type: str, vehicle_id: int) -> Vehicle:
        if vehicle_type == VEHICLE_CAR:
            return self.box_car.get(vehicle_id)
        if vehicle_type == VEHICLE_MOTORCYCLE:
            return self.box_motorcycle.get(vehicle_id)
        raise ValueError(f"Unknown vehicle type: {vehicle_type}")

    def get_mechanic(self, mechanic_id: int) -> Mechanic:
        return self.box_mechanic.get(mechanic_id)

    def get_parts(self, part_ids: List[int]) -> List[Part]:
        return [self.box_part.get(pid) for pid in part_ids]

    def total_cost(self, order: ServiceOrder) -> float:
        parts = self.get_parts(order.part_ids)
        parts_cost = sum(p.price for p in parts)
        return order.labor_cost + parts_cost

    def print_order(self, order: ServiceOrder):
        vehicle = self.get_vehicle(order.vehicle_type, order.vehicle_id)
        mechanic = self.get_mechanic(order.mechanic_id)
        parts = self.get_parts(order.part_ids)

        print(f"Order {order.order_number} [{order.status}]")
        print(f"  Vehicle: {vehicle.description()}")
        print(f"  Mechanic: {mechanic.name} ({mechanic.specialty})")
        print(f"  Description: {order.description}")
        print("  Parts:")
        for p in parts:
            print(f"    - {p.name}: ${p.price:,.2f}")
        print(f"  Labor cost: ${order.labor_cost:,.2f}")
        print(f"  Total cost: ${self.total_cost(order):,.2f}")
