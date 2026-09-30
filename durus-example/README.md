# Auto Repair Shop — Durus example

Ejemplo de un taller mecánico usando [Durus](https://pypi.org/project/Durus/).

## Estructura

- `models.py` — entidades: `Vehicle` (clase base), `Car`, `Motorcycle`, `Mechanic`, `Part`, `ServiceOrder`.
- `repository.py` — clase `RepairShop`: encapsula el `FileStorage` y la `Connection` de Durus, y expone métodos para registrar y consultar entidades.
- `main.py` — punto de entrada: siembra datos de ejemplo y los imprime.

## Uso

```bash
pip install -r requirements.txt
python3 main.py
```

La primera ejecución siembra los datos en `data/shop.durus`. Ejecuciones
posteriores detectan que ya existen y solo los leen (persistencia).

## Notas técnicas

- `Vehicle`, `Car` y `Motorcycle` heredan de `durus.persistent.Persistent`;
  la herencia es nativa de Python, sin decoradores especiales (igual que
  en el ejemplo de ZODB).
- `ServiceOrder.vehicle` y `ServiceOrder.mechanic` son referencias
  directas a los objetos reales (no IDs); Durus detecta automáticamente
  todo objeto `Persistent` alcanzable desde el root y lo persiste junto
  con sus referencias.
- `ServiceOrder.parts` es una `PersistentList` (equivalente a la de ZODB)
  con objetos `Part` reales.
- Las transacciones son explícitas: cada alta llama a `connection.commit()`.
- A diferencia de ZODB (que usa `BTrees.OOBTree`), aquí los contenedores
  raíz (`cars`, `mechanics`, etc.) son `durus.persistent_dict.PersistentDict`.
- Se sube el nivel del logger `durus` a `WARNING` en `repository.py` para
  evitar que cada `commit()` imprima una línea de log en la consola.

## Limpieza

```bash
rm -rf data
```
