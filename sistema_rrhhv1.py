from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Datos que utilizará nuestro programa
# ---------------------------------------------------------------------------
UIT = 5500
LIMITE_VACACIONES = 30
FECHA_ACTUAL = "10/10/2026"
MES_ACTUAL = 10
ANIO_ACTUAL = 2026
AREAS = ["Operaciones", "Comercial", "Finanzas", "Recursos Humanos", "TI"]
LINEA_LARGA = "=============================================="


# ---------------------------------------------------------------------------
# Excepcion personalizada
# ---------------------------------------------------------------------------
class ExcepcionPersonalizada(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


# ---------------------------------------------------------------------------
# AFP
# ---------------------------------------------------------------------------
class AFP:
    def __init__(self, nombre, aporte, comision, seguro):
        self.__nombre = nombre
        self.__aporte = aporte
        self.__comision = comision
        self.__seguro = seguro

    @property
    def nombre(self):
        return self.__nombre

    def calcular_descuento(self, sueldo):
        return sueldo * (self.__aporte + self.__comision + self.__seguro)

    def __str__(self):
        return self.__nombre


AFPS = [
    AFP("Integra", 0.10, 0.0155, 0.0137),
    AFP("Prima", 0.10, 0.0160, 0.0137),
    AFP("Profuturo", 0.10, 0.0169, 0.0137),
    AFP("Habitat", 0.10, 0.0147, 0.0137),
]

# ---------------------------------------------------------------------------
# Empleado E Hijo: Operativo + Administrativo
# ---------------------------------------------------------------------------
class Empleado(ABC):
    def __init__(self, dni, nombres, apellidos, area, fecha_ingreso, sueldo_bruto, afp):
        if dni < 10000000 or dni > 99999999:
            raise ExcepcionPersonalizada("El DNI debe tener 8 digitos")
        if nombres == "" or apellidos == "":
            raise ExcepcionPersonalizada("Los nombres y apellidos no pueden estar vacios")
        if area == "":
            raise ExcepcionPersonalizada("El area no puede estar vacia")
        if sueldo_bruto <= 0:
            raise ExcepcionPersonalizada("El sueldo bruto debe ser mayor a cero")
        self.__dni = dni
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__area = area
        self.__fecha_ingreso = fecha_ingreso
        self.__sueldo_bruto = sueldo_bruto
        self.__afp = afp
        self.__activo = True
        self.__fecha_cese = ""
        self.__faltas = 0

    @property
    def dni(self):
        return self.__dni

    @property
    def nombres(self):
        return self.__nombres

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        if area == "":
            raise ExcepcionPersonalizada("El area no puede estar vacia")
        self.__area = area

    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso

    @property
    def sueldo_bruto(self):
        return self.__sueldo_bruto

    @sueldo_bruto.setter
    def sueldo_bruto(self, sueldo):
        if sueldo <= 0:
            raise ExcepcionPersonalizada("El sueldo bruto debe ser mayor a cero")
        self.__sueldo_bruto = sueldo

    @property
    def afp(self):
        return self.__afp

    @afp.setter
    def afp(self, afp):
        self.__afp = afp

    @property
    def activo(self):
        return self.__activo

    @property
    def fecha_cese(self):
        return self.__fecha_cese

    @property
    def faltas(self):
        return self.__faltas

    @faltas.setter
    def faltas(self, faltas):
        if faltas < 0 or faltas > 30:
            raise ExcepcionPersonalizada("Las faltas deben estar entre 0 y 30 dias")
        self.__faltas = faltas

    def calcular_descuento_faltas(self):
        # Cada dia de falta descuenta un dia de sueldo (sueldo / 30)
        return self.__sueldo_bruto / 30 * self.__faltas

    def registrar_cese(self, fecha):
        if not self.__activo:
            raise ExcepcionPersonalizada("El colaborador ya esta cesado")
        self.__activo = False
        self.__fecha_cese = fecha

    @abstractmethod
    def calcular_ingreso_total(self):
        pass

    @abstractmethod
    def descripcion_tipo(self):
        pass

    def __str__(self):
        if self.activo:
            texto = "Activo"
        else:
            texto = "Cesado"
        return f"{self.dni} - {self.nombres} {self.apellidos} - {self.area} - {texto}"


class Administrativo(Empleado):
    def __init__(self, dni, nombres, apellidos, area, fecha_ingreso, sueldo_bruto, afp, bono):
        super().__init__(dni, nombres, apellidos, area, fecha_ingreso, sueldo_bruto, afp)
        if bono < 0:
            raise ExcepcionPersonalizada("El bono no puede ser negativo")
        self.__bono = bono

    def calcular_ingreso_total(self):
        return self.sueldo_bruto + self.__bono

    def descripcion_tipo(self):
        return f"Administrativo (bono S/. {self.__bono:.2f})"


class Operativo(Empleado):
    def __init__(self, dni, nombres, apellidos, area, fecha_ingreso, sueldo_bruto, afp,
                turno, horas_extra):
        super().__init__(dni, nombres, apellidos, area, fecha_ingreso, sueldo_bruto, afp)
        if horas_extra < 0:
            raise ExcepcionPersonalizada("Las horas extra no pueden ser negativas")
        self.__turno = turno
        self.__horas_extra = horas_extra

    def calcular_ingreso_total(self):
        valor_hora = self.sueldo_bruto / 240
        pago_extra = self.__horas_extra * valor_hora * 1.25
        return self.sueldo_bruto + pago_extra

    def descripcion_tipo(self):
        return f"Operativo (turno {self.__turno}, {self.__horas_extra} horas extra)"

# ---------------------------------------------------------------------------
# Vacaciones y capacitaciones
# ---------------------------------------------------------------------------
class Vacacion:
    def __init__(self, empleado, fecha_inicio, dias):
        if dias <= 0:
            raise ExcepcionPersonalizada("Los dias de vacaciones deben ser mayores a cero")
        self.__empleado = empleado
        self.__fecha_inicio = fecha_inicio
        self.__dias = dias
        self.__aprobada = False

    @property
    def empleado(self):
        return self.__empleado

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def dias(self):
        return self.__dias

    @property
    def aprobada(self):
        return self.__aprobada

    def aprobar(self):
        self.__aprobada = True

    def __str__(self):
        if self.aprobada:
            texto = "Aprobada"
        else:
            texto = "Pendiente"
        return f"Vacaciones desde {self.fecha_inicio} - {self.dias} dias - {texto}"

class Capacitacion:
    def __init__(self, empleado, nombre, fecha, horas):
        if nombre == "":
            raise ExcepcionPersonalizada("El nombre de la capacitacion no puede estar vacio")
        if horas <= 0:
            raise ExcepcionPersonalizada("Las horas deben ser mayores a cero")
        self.__empleado = empleado
        self.__nombre = nombre
        self.__fecha = fecha
        self.__horas = horas
        self.__completada = False

    @property
    def empleado(self):
        return self.__empleado

    @property
    def nombre(self):
        return self.__nombre

    @property
    def completada(self):
        return self.__completada

    def completar(self):
        self.__completada = True

    def __str__(self):
        if self.completada:
            texto = "Completada"
        else:
            texto = "Pendiente"
        return f"Capacitacion {self.__nombre} - {self.__fecha} - {self.__horas} horas - {texto}"

# ---------------------------------------------------------------------------
# Registros
# ---------------------------------------------------------------------------
class RegistroVacaciones:
    def __init__(self):
        self.__vacaciones = []

    @property
    def vacaciones(self):
        return self.__vacaciones

    def buscar_por_dni(self, dni):
        encontradas = []
        for v in self.__vacaciones:
            if v.empleado.dni == dni:
                encontradas.append(v)
        return encontradas

    def dias_aprobados(self, dni):
        total = 0
        for v in self.buscar_por_dni(dni):
            if v.aprobada:
                total = total + v.dias
        return total

    def dias_solicitados(self, dni):
        total = 0
        for v in self.buscar_por_dni(dni):
            total = total + v.dias
        return total

    def solicitar(self, vacacion):
        if self.dias_solicitados(vacacion.empleado.dni) + vacacion.dias > LIMITE_VACACIONES:
            raise ExcepcionPersonalizada("Los dias superan el limite de vacaciones")
        self.__vacaciones.append(vacacion)

    def aprobar(self, vacacion):
        if self.dias_aprobados(vacacion.empleado.dni) + vacacion.dias > LIMITE_VACACIONES:
            raise ExcepcionPersonalizada("No se puede aprobar: supera el limite de vacaciones")
        vacacion.aprobar()

class RegistroCapacitaciones:
    def __init__(self):
        self.__capacitaciones = []

    @property
    def capacitaciones(self):
        return self.__capacitaciones

    def agregar(self, capacitacion):
        self.__capacitaciones.append(capacitacion)

    def buscar_por_dni(self, dni):
        encontradas = []
        for c in self.__capacitaciones:
            if c.empleado.dni == dni:
                encontradas.append(c)
        return encontradas

# ---------------------------------------------------------------------------
# Sistema RRHH
# ---------------------------------------------------------------------------
class SistemaRRHH:
    def __init__(self):
        self.__empleados = []
        self.__registro_vacaciones = RegistroVacaciones()
        self.__registro_capacitaciones = RegistroCapacitaciones()
        self.registrar_empleado(Operativo(
            45678912, "Jesus Andres", "Lujan", "Operaciones", "15/03/2024", 3500, AFPS[0], "Noche", 10))
        self.registrar_empleado(Administrativo(
            73738625, "Ariel", "Zarate", "TI", "14/10/2022", 2500, AFPS[1], 150))
        self.registrar_empleado(Administrativo(
            47891234, "Vannesa", "Rios", "Finanzas", "10/01/2022", 9800, AFPS[2], 200))
        self.registrar_empleado(Administrativo(
            41234567, "Gianpiero", "Yataco", "Comercial", "01/06/2023", 5200, AFPS[1], 150))
        self.registrar_empleado(Administrativo(
            76543210, "Victor", "Balboa", "Recursos Humanos", "10/09/2025", 5200, AFPS[1], 150))

    @property
    def empleados(self):
        return self.__empleados

    @property
    def vacaciones(self):
        return self.__registro_vacaciones

    @property
    def capacitaciones(self):
        return self.__registro_capacitaciones

    def registrar_empleado(self, empleado):
        for e in self.__empleados:
            if e.dni == empleado.dni:
                raise ExcepcionPersonalizada("Ya existe un colaborador con ese DNI")
        self.__empleados.append(empleado)

    def buscar_por_dni(self, dni):
        for e in self.__empleados:
            if e.dni == dni:
                return e
        raise ExcepcionPersonalizada(f"El colaborador con DNI {dni} no existe")

    def buscar_por_nombre(self, texto):
        encontrados = []
        for e in self.__empleados:
            if e.nombres == texto or e.apellidos == texto:
                encontrados.append(e)
        return encontrados

    def buscar_por_area(self, area):
        encontrados = []
        for e in self.__empleados:
            if e.area == area:
                encontrados.append(e)
        return encontrados


