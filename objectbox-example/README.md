# Auto Repair Shop — ObjectBox example

Ejemplo de un taller mecánico usando [ObjectBox](https://github.com/objectbox/objectbox-python).

## Estructura

- `models.py` — entidades: `Vehicle` (clase base), `Car`, `Motorcycle`, `Mechanic`, `Part`, `ServiceOrder`.
- `repository.py` — clase `RepairShop`: encapsula el `Store` y los `Box`, y resuelve manualmente las referencias entre objetos.
- `main.py` — punto de entrada: siembra datos de ejemplo y los imprime.

## Uso

```bash
pip install -r requirements.txt
python3 main.py
```

La primera ejecución siembra los datos en la carpeta `data/`. Ejecuciones
posteriores detectan que ya existen y solo los leen (persistencia).

## Notas técnicas

- `Vehicle` no es una `@Entity`; es una clase base normal de Python. `Car` y
  `Motorcycle` sí son `@Entity` y heredan sus campos porque están
  declarados sin paréntesis en la clase base (p. ej. `plate = String`).
- Esta versión de ObjectBox para Python no tiene relaciones nativas
  (`ToOne`/`ToMany`), por lo que `ServiceOrder` guarda IDs
  (`vehicle_type` + `vehicle_id`, `mechanic_id`, `part_ids`) y
  `repository.py` los resuelve consultando los `Box` correspondientes.

## Limpieza

```bash
rm -rf data objectbox-model.json
```
