# python-oodb

Tres ejemplos independientes de un mismo caso de uso (un taller mecánico:
"Auto Repair Shop") implementados con dos bases de datos orientadas a
objetos distintas para Python:

- **`objectbox-example/`** — implementación con [ObjectBox](https://github.com/objectbox/objectbox-python).
- **`zodb-example/`** — implementación con [ZODB](http://www.zodb.org/).
- **`durus-example/`** — implementación con [Durus](https://pypi.org/project/Durus/).

Cada carpeta es un proyecto autocontenido con su propio `main.py`,
modelos, capa de acceso a datos (`repository.py`) y `requirements.txt`.

## Conceptos ilustrados en los tres ejemplos

- **Herencia**: `Vehicle` es la clase base; `Car` y `Motorcycle` la extienden.
- **Referencias entre objetos**: `ServiceOrder` hace referencia a un `Vehicle` y a un `Mechanic`.
- **Listas dentro de un objeto**: `ServiceOrder` contiene la lista de `Part` (refacciones) utilizadas.
- **Persistencia**: los datos sobreviven entre ejecuciones (se siembran una sola vez y luego se leen desde disco).

El código está escrito en inglés (nombres de clases, funciones, variables);
los comentarios que explican los bloques relevantes están en español.

## Uso

```bash
# PRIMERO SE ACTIVA EL ENTORNO VIRTUAL
# En MAC/Linux
source venv/bin/activate
# En Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Ejemplo con ObjectBox
cd objectbox-example
pip install -r requirements.txt
python3 main.py

# Ejemplo con ZODB
cd ../zodb-example
pip install -r requirements.txt
python3 main.py

# Ejemplo con Durus
cd ../durus-example
pip install -r requirements.txt
python3 main.py
```

Cada script, en su primera ejecución, siembra los datos de ejemplo; en
ejecuciones posteriores detecta que ya existen y solo los lee,
demostrando la persistencia.

## Diferencia principal entre los tres enfoques

| Aspecto | ObjectBox | ZODB | Durus |
|---|---|---|---|
| Herencia de entidades | Cada `@Entity` es independiente; los campos comunes se heredan a nivel de clase Python | Herencia nativa de Python (`Persistent`) | Herencia nativa de Python (`Persistent`) |
| Referencias entre objetos | Manuales: se guardan IDs y se resuelven con los `Box` correspondientes | Automáticas: se guardan los objetos reales | Automáticas: se guardan los objetos reales |
| Listas | `Int64List` con IDs de otras entidades | `PersistentList` con los objetos reales | `PersistentList` con los objetos reales |
| Persistencia | Carpeta de datos + archivo de modelo JSON | Archivo único `.fs` (FileStorage) | Archivo único `.durus` (FileStorage propio) |
| Transacciones | Implícitas en cada `put()` | Explícitas con `transaction.commit()` | Explícitas con `connection.commit()` |
| Contenedor raíz | `Box` por entidad | `BTrees.OOBTree` | `durus.persistent_dict.PersistentDict` |

Nota: ZODB y Durus son muy similares conceptualmente (ambos usan objetos
`Persistent` con referencias directas); la diferencia principal está en
la API de conexión/transacción y en las clases de colección persistente
que ofrece cada biblioteca.

Ver el `README.md` dentro de cada carpeta para el detalle específico de
esa implementación.
