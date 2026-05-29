import sqlite3


# =========================================================================
# 🏢 CLASE PADRE (Superclase)
# =========================================================================
class Empleado:
    def __init__(self, nombre, puesto, salario):
        self.nombre = nombre
        self.puesto = puesto
        self.salario = salario

    def trabajar(self):
        print(f"👨‍💻 {self.nombre} está realizando sus tareas como {self.puesto}.")


# =========================================================================
# 👑 CLASE HIJA (Subclase) - Aplica HERENCIA
# Al poner (Empleado) al lado del nombre, le decimos a Python que herede todo
# =========================================================================
class Gerente(Empleado):
    def __init__(self, nombre, puesto, salario, presupuesto_equipo):
        # 'super()' invoca al constructor del Padre para que guarde el nombre, puesto y salario
        super().__init__(nombre, puesto, salario)
        # Añadimos la propiedad única que solo tienen los gerentes
        self.presupuesto = presupuesto_equipo

    # Modificamos una acción del padre para que sea especial (Polimorfismo)
    def trabajar(self):
        print(
            f"📈 {self.nombre} está liderando la reunión de planificación con un presupuesto de ${self.presupuesto:,.2f}."
        )


# =========================================================================
# 🗄️ CONTROLADOR: Gestor de Base de Datos Adaptado
# =========================================================================
class GestorBaseDatos:
    def __init__(self, nombre_bd):
        self.conexion = sqlite3.connect(nombre_bd)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puesto TEXT,
            salario REAL,
            presupuesto_gerente REAL  -- Columna extra para cuando guardemos un gerente
        )
        """)
        self.conexion.commit()

    def guardar_en_sistema(self, persona):
        """Este método es inteligente: puede recibir tanto un Empleado como un Gerente."""
        # Verificamos si el objeto que nos pasaron es un Gerente usando 'hasattr'
        presupuesto = persona.presupuesto if hasattr(persona, "presupuesto") else None

        datos = (persona.nombre, persona.puesto, persona.salario, presupuesto)

        self.cursor.execute(
            """
        INSERT INTO empleados (nombre, puesto, salario, presupuesto_gerente) 
        VALUES (?, ?, ?, ?)
        """,
            datos,
        )
        self.conexion.commit()
        print(f"📥 Guardado en Base de Datos: {persona.nombre} ({persona.puesto})")

    def cerrar(self):
        self.conexion.close()


# =========================================================================
# 🎮 PROGRAMA PRINCIPAL
# =========================================================================
gestor = GestorBaseDatos("empresa_avanzada.db")

# 1. Creamos un empleado normal (usando la clase padre)
emp_estandar = Empleado("Carlos", "Desarrollador Backend", 3200.00)

# 2. Creamos un gerente (usando la clase hija)
gerente_equipo = Gerente("Ernest Pro", "Director de Tecnología", 7500.00, 25000.00)

print("🎬 --- PROBANDO ACCIONES EN VIVO ---")
# Ambos objetos saben ejecutar el método .trabajar(), pero lo hacen de forma diferente
emp_estandar.trabajar()
gerente_equipo.trabajar()

print("\n💾 --- ALMACENANDO EN EL SISTEMA ---")
gestor.guardar_en_sistema(emp_estandar)
gestor.guardar_en_sistema(gerente_equipo)

gestor.cerrar()
