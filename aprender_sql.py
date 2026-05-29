import sqlite3

# 1. CONEXIÓN: Nos conectamos a la misma base de datos (no se borrará lo anterior)
conexion = sqlite3.connect("mi_empresa.db")
cursor = conexion.cursor()

# =========================================================================
# LÓGICA 4: ACTUALIZAR DATOS (Comando UPDATE)
# Vamos a darle un aumento de sueldo a Ana (ID 2) porque trabaja excelente.
# =========================================================================
print("🚀 Aplicando aumento de sueldo a Ana...")

nuevo_sueldo = 3200.00
id_ana = 2

cursor.execute(
    """
UPDATE empleados 
SET salario = ? 
WHERE id = ?
""",
    (nuevo_sueldo, id_ana),
)

# Guardamos los cambios en el disco duro
conexion.commit()
print("✅ Sueldo de Ana actualizado con éxito.")

# =========================================================================
# LÓGICA 5: BORRAR REGISTROS (Comando DELETE)
# Carlos (ID 3) renunció a la empresa. Debemos quitarlo de la tabla de forma segura.
# =========================================================================
print("\n🔥 Eliminando registro de Carlos por renuncia...")

id_carlos = 3

cursor.execute(
    """
DELETE FROM empleados 
WHERE id = ?
""",
    (id_carlos,),
)  # Nota: En Python, si pasas un solo dato en SQL, se pone una coma al final (tupla de un elemento)

conexion.commit()
print("🗑️ Registro eliminado de la base de datos.")

# =========================================================================
# LÓGICA 6: VERIFICACIÓN FINAL (SELECT)
# Consultamos la tabla entera para ver cómo quedó la empresa hoy
# =========================================================================
print("\n📋 --- ESTADO ACTUAL DE LA PLANTILLA ---")

cursor.execute("SELECT id, nombre, puesto, salario FROM empleados")
resultados = cursor.fetchall()

for fila in resultados:
    id_emp, nombre, puesto, salario = fila
    print(f"ID: {id_emp} | {nombre} -> {puesto} | Sueldo: ${salario:,.2f}")

# Cerramos la conexión
conexion.close()
print("\n🔒 Conexión cerrada.")
