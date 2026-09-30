# Auto Repair Shop — ZODB example

Ejemplo de un taller mecánico usando [ZODB](http://www.zodb.org/).

## Estructura

- `models.py` — entidades: `Vehicle` (clase base), `Car`, `Motorcycle`, `Mechanic`, `Part`, `ServiceOrder`.
- `repository.py` — clase `RepairShop`: encapsula la conexión ZODB y expone métodos para registrar y consultar entidades.
- `main.py` — punto de entrada: siembra datos de ejemplo y los imprime.

## Uso

```bash
pip install -r requirements.txt
python3 main.py
```

La primera ejecución siembra los datos en `data/shop.fs`. Ejecuciones
posteriores detectan que ya existen y solo los leen (persistencia).

## Notas técnicas

- `Vehicle`, `Car` y `Motorcycle` heredan de `Persistent`; la herencia es
  nativa de Python, sin decoradores especiales.
- `ServiceOrder.vehicle` y `ServiceOrder.mechanic` son referencias
  directas a los objetos reales (no IDs); ZODB persiste esas referencias
  automáticamente.
- `ServiceOrder.parts` es una `PersistentList` de objetos `Part` reales;
  se usa `PersistentList` en lugar de `list` para que ZODB detecte
  cambios dentro de la lista.
- Las transacciones son explícitas: cada alta llama a `transaction.commit()`.

## Limpieza

```bash
rm -rf data
```
