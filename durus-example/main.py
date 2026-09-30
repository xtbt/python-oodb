"""
Demo: Auto Repair Shop con Durus.

La primera vez que se ejecuta, siembra los datos (vehiculos, mecanicos,
refacciones y ordenes de servicio). En ejecuciones siguientes detecta
que ya existen datos y solo los lee, demostrando que quedaron
persistidos en disco (archivo ./data/shop.durus).

Diferencias clave frente a ObjectBox (y similitudes con ZODB):
  - Las referencias entre objetos son directas (order.vehicle es el
    objeto Vehicle real, no un ID).
  - Las listas (parts) son PersistentList y contienen objetos reales,
    no IDs.
  - No hay necesidad de "resolver" referencias manualmente.
  - La herencia de Python es nativa: Car y Motorcycle heredan de
    Vehicle sin necesidad de decoradores especiales.
"""

from repository import RepairShop


def seed_data(shop: RepairShop):
    # --- Vehiculos: instancias de las subclases Car y Motorcycle ---
    car_id = shop.register_car(
        plate="ABC-123", make="Toyota", model="Corolla", year=2020,
        door_count=4,
    )
    motorcycle_id = shop.register_motorcycle(
        plate="XYZ-987", make="Honda", model="CBR 600", year=2022,
        engine_displacement_cc=600,
    )

    mechanic_id = shop.register_mechanic(name="John Smith", specialty="Engine")

    # --- Refacciones que luego se referenciaran desde las ordenes ---
    part_oil_filter_id = shop.register_part(name="Oil filter", price=180.0)
    part_brake_pads_id = shop.register_part(name="Brake pads set", price=650.0)
    part_spark_plug_id = shop.register_part(name="Spark plug", price=95.0)

    # --- Obtener los objetos reales (no IDs) para usarlos como referencias ---
    car = shop.get_car(car_id)
    motorcycle = shop.get_motorcycle(motorcycle_id)
    mechanic = shop.get_mechanic(mechanic_id)
    part_oil_filter = shop.get_part(part_oil_filter_id)
    part_brake_pads = shop.get_part(part_brake_pads_id)
    part_spark_plug = shop.get_part(part_spark_plug_id)

    # --- Ordenes de servicio: referencian directamente vehiculo, mecanico y refacciones ---
    shop.create_service_order(
        order_number="SO-0001",
        vehicle=car,
        mechanic=mechanic,
        parts=[part_oil_filter, part_brake_pads],
        description="Brake service and oil change",
        labor_cost=500.0,
        status="in progress",
    )

    shop.create_service_order(
        order_number="SO-0002",
        vehicle=motorcycle,
        mechanic=mechanic,
        parts=[part_spark_plug],
        description="Minor tune-up",
        labor_cost=300.0,
        status="closed",
    )


def main():
    shop = RepairShop(db_path="data/shop.durus")
    try:
        # --- Verificacion de persistencia: si ya hay ordenes, no se siembra de nuevo ---
        if len(shop.get_all_orders()) == 0:
            print("No previous data found: seeding initial data...\n")
            seed_data(shop)
        else:
            print("Existing data found on disk (persistence verified).\n")

        orders = shop.get_all_orders()
        for order in orders:
            shop.print_order(order)
            print()
    finally:
        shop.close()


if __name__ == "__main__":
    main()
