"""
Demo: Auto Repair Shop con ObjectBox.

La primera vez que se ejecuta, siembra los datos (vehiculos, mecanicos,
refacciones y ordenes de servicio). En ejecuciones siguientes detecta
que ya existen datos y solo los lee, demostrando que quedaron
persistidos en disco (carpeta ./data).
"""

from repository import RepairShop, VEHICLE_CAR, VEHICLE_MOTORCYCLE


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

    # --- Ordenes de servicio: referencian vehiculo, mecanico y refacciones ---
    shop.create_service_order(
        order_number="SO-0001",
        vehicle_type=VEHICLE_CAR,
        vehicle_id=car_id,
        mechanic_id=mechanic_id,
        part_ids=[part_oil_filter_id, part_brake_pads_id],
        description="Brake service and oil change",
        labor_cost=500.0,
        status="in progress",
    )

    shop.create_service_order(
        order_number="SO-0002",
        vehicle_type=VEHICLE_MOTORCYCLE,
        vehicle_id=motorcycle_id,
        mechanic_id=mechanic_id,
        part_ids=[part_spark_plug_id],
        description="Minor tune-up",
        labor_cost=300.0,
        status="closed",
    )


def main():
    shop = RepairShop(directory="data")
    try:
        # --- Verificacion de persistencia: si ya hay ordenes, no se siembra de nuevo ---
        if shop.box_order.count() == 0:
            print("No previous data found: seeding initial data...\n")
            seed_data(shop)
        else:
            print("Existing data found on disk (persistence verified).\n")

        orders = shop.box_order.get_all()
        for order in orders:
            shop.print_order(order)
            print()
    finally:
        shop.close()


if __name__ == "__main__":
    main()
