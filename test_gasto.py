import unittest

from src.modelo.declarative_base import Session
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.logica.Logica_mock import Logica_mock
from faker import Faker


class tests_gastos(unittest.TestCase):

    def setUp(self):

        self.session = Session()

        self.cuentas_claras = Logica_mock()


        self.data_factory = Faker()


    def tearDown(self):

        self.session = Session()

        busqueda_gastos = self.session.query(Gasto).all()
        busqueda_viajeros = self.session.query(Viajero).all()
        busqueda_actividad = self.session.query(Actividad).all()

        for gasto in busqueda_gastos:
            self.session.delete(gasto)

        for viajero in busqueda_viajeros:
            self.session.delete(viajero)

        for actividad in busqueda_actividad:
            self.session.delete(actividad)

        self.session.commit()
        self.session.close()

    def test_agregar_gasto_actividad(self):
        """
        Prueba agregar un gasto a una actividad especifica
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        prueba_gasto = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       self.data_factory.name(),
                                                       self.data_factory.random_int(1,1000),
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto, True)
        self.assertEqual(len(gastos_actividad), 1)

    def test_agregar_gasto_actividad_con_viajero_no_asociado_a_actividad(self):
        """
        Prueba agregar un gasto a una actividad especifica cuando el viajero solicitado no hace parte de la misma
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)


        prueba_gasto = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       self.data_factory.name(),
                                                       self.data_factory.random_int(1,1000),
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto, False)
        self.assertEqual(gastos_actividad, None)

    def test_agregar_gasto_igual_cero_a_actividad(self):
        """
        Prueba agregar un gasto  que tenga valor  igual a 0 a una actividad especifica
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        prueba_gasto = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       self.data_factory.name(),
                                                       0,
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto, False)
        self.assertEqual(gastos_actividad, None)

    def test_agregar_gasto_negativo_a_actividad(self):
        """
        Prueba agregar un gasto  que tenga valor  negativo a 0 a una actividad especifica
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        prueba_gasto = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       self.data_factory.name(),
                                                       self.data_factory.random_int(1,1000)*-1,
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto, False)
        self.assertEqual(gastos_actividad, None)

    def test_agregar_gasto_repetido_actividad(self):
        """
        Prueba agregar un gasto con nombre  repetido una actividad especifica
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()
        concepto_gasto = self.data_factory.name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        prueba_gasto1 = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_gasto,
                                                       self.data_factory.random_int(1,1000),
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        prueba_gasto2 = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_gasto,
                                                       self.data_factory.random_int(1,1000),
                                                       self.data_factory.date(),
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto1, True)
        self.assertEqual(prueba_gasto2, False)
        self.assertEqual(len(gastos_actividad), 1)

    def test_agregar_gasto_actividad_con_concepto_fecha_igual_none(self):
        """
        Prueba agregar un gasto a una actividad especifica con concepto o fecho vacios
        """
        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        prueba_gasto = self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       None,
                                                       self.data_factory.random_int(1,1000),
                                                       None,
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gastos_actividad = self.cuentas_claras.dar_gastos_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.assertEqual(prueba_gasto, False)
        self.assertEqual(gastos_actividad, None)

    def test_editar_gasto(self):
        """
        Prueba editar el concepto, valor o fecha de un gasto manteniendo el viajero
        """

        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        concepto_anterior = self.data_factory.name()
        valor_anterior = self.data_factory.random_int(1, 1000)
        fecha_anterior = self.data_factory.date()

        nuevo_concepto = self.data_factory.name()
        nuevo_valor = self.data_factory.random_int(1, 1000)
        nueva_fecha = self.data_factory.date()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_anterior,
                                                       valor_anterior,
                                                       fecha_anterior,
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto_id = self.session.query(Gasto).filter(Gasto.concepto == concepto_anterior).first().id

        prueba_editar = self.cuentas_claras.editar_gasto(gasto_id,
                                                         nuevo_concepto,
                                                         nuevo_valor,
                                                         nueva_fecha,
                                                         self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto = self.session.query(Gasto).filter(Gasto.id == gasto_id).first()
        self.assertEqual(prueba_editar, True)
        self.assertEqual(gasto.concepto, nuevo_concepto)
        self.assertEqual(gasto.valor, nuevo_valor)
        self.assertEqual(gasto.fecha, nueva_fecha)

    def test_editar_gasto_con_valor_igual_cero(self):
        """
        Prueba editar el gasto con valor igual a cero
        """

        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        concepto_anterior = self.data_factory.name()
        valor_anterior = self.data_factory.random_int(1, 1000)
        fecha_anterior = self.data_factory.date()

        nuevo_concepto = self.data_factory.name()

        nueva_fecha = self.data_factory.date()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_anterior,
                                                       valor_anterior,
                                                       fecha_anterior,
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto_id = self.session.query(Gasto).filter(Gasto.concepto == concepto_anterior).first().id

        prueba_editar = self.cuentas_claras.editar_gasto(gasto_id,
                                                         nuevo_concepto,
                                                         0,
                                                         nueva_fecha,
                                                         self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto = self.session.query(Gasto).filter(Gasto.id == gasto_id).first()
        self.assertEqual(prueba_editar, False)
        self.assertEqual(gasto.concepto, concepto_anterior)
        self.assertEqual(gasto.valor, valor_anterior)
        self.assertEqual(gasto.fecha, fecha_anterior)


    def test_editar_gasto_con_valor_negativo(self):
        """
        Prueba editar el gasto con valor negativo
        """

        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        concepto_anterior = self.data_factory.name()
        valor_anterior = self.data_factory.random_int(1, 1000)
        fecha_anterior = self.data_factory.date()

        nuevo_concepto = self.data_factory.name()
        nuevo_valor = self.data_factory.random_int(1, 1000)*-1
        nueva_fecha = self.data_factory.date()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_anterior,
                                                       valor_anterior,
                                                       fecha_anterior,
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto_id = self.session.query(Gasto).filter(Gasto.concepto == concepto_anterior).first().id

        prueba_editar = self.cuentas_claras.editar_gasto(gasto_id,
                                                         nuevo_concepto,
                                                         nuevo_valor,
                                                         nueva_fecha,
                                                         self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto = self.session.query(Gasto).filter(Gasto.id == gasto_id).first()
        self.assertEqual(prueba_editar, False)
        self.assertEqual(gasto.concepto, concepto_anterior)
        self.assertEqual(gasto.valor, valor_anterior)
        self.assertEqual(gasto.fecha, fecha_anterior)

    def test_editar_gasto_con_concepto_o_fecha_vacios(self):
        """
        Prueba editar el gasto con concepto o fecha vacios
        """

        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        concepto_anterior = self.data_factory.name()
        valor_anterior = self.data_factory.random_int(1, 1000)
        fecha_anterior = self.data_factory.date()


        nuevo_valor = self.data_factory.random_int(1, 1000)


        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_anterior,
                                                       valor_anterior,
                                                       fecha_anterior,
                                                       self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto_id = self.session.query(Gasto).filter(Gasto.concepto == concepto_anterior).first().id

        prueba_editar = self.cuentas_claras.editar_gasto(gasto_id,
                                                         None,
                                                         nuevo_valor,
                                                         None,
                                                         self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id)

        gasto = self.session.query(Gasto).filter(Gasto.id == gasto_id).first()
        self.assertEqual(prueba_editar, False)
        self.assertEqual(gasto.concepto, concepto_anterior)
        self.assertEqual(gasto.valor, valor_anterior)
        self.assertEqual(gasto.fecha, fecha_anterior)

    def test_editar_gasto_asociandolo_a_un_nuevo_viajero(self):
        """
        Prueba editar el gasto asociandolo a un nuevo viajero
        """

        nombre_actividad = self.data_factory.name()
        nombre_viajero = self.data_factory.first_name()
        apellido_viajero = self.data_factory.last_name()

        nombre_viajero2 = self.data_factory.first_name()
        apellido_viajero2 = self.data_factory.last_name()

        concepto_anterior = self.data_factory.name()
        valor_anterior = self.data_factory.random_int(1, 1000)
        fecha_anterior = self.data_factory.date()

        nuevo_concepto = self.data_factory.name()
        nuevo_valor = self.data_factory.random_int(1, 1000)
        nueva_fecha = self.data_factory.date()

        self.cuentas_claras.insertar_actividad(nombre_actividad)
        self.cuentas_claras.agregar_viajero(nombre_viajero,apellido_viajero)
        self.cuentas_claras.agregar_viajero(nombre_viajero2,apellido_viajero2)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        self.cuentas_claras.asociar_viajero_a_actividad(self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero2 and Viajero.apellido == apellido_viajero2).first().id,
                                                        self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id)

        viajero1_id = self.session.query(Viajero).filter(
            Viajero.nombre == nombre_viajero and Viajero.apellido == apellido_viajero).first().id
        viajero2_id = self.session.query(Viajero).filter(
            Viajero.nombre == nombre_viajero2 and Viajero.apellido == apellido_viajero2).first().id

        self.cuentas_claras.crear_gasto_para_actividad(self.session.query(Actividad).filter(Actividad.nombre == nombre_actividad).first().id,
                                                       concepto_anterior,
                                                       valor_anterior,
                                                       fecha_anterior,
                                                       viajero1_id)

        gasto_id = self.session.query(Gasto).filter(Gasto.concepto == concepto_anterior).first().id

        prueba_editar = self.cuentas_claras.editar_gasto(gasto_id,
                                                         nuevo_concepto,
                                                         nuevo_valor,
                                                         nueva_fecha,
                                                         viajero2_id)

        gasto = self.session.query(Gasto).filter(Gasto.id == gasto_id).first()
        gastos_viajero1 = self.session.query(Gasto).filter(Gasto.viajero == viajero1_id).all()
        gastos_viajero2 = self.session.query(Gasto).filter(Gasto.viajero == viajero2_id).all()
        self.assertEqual(prueba_editar, True)
        self.assertEqual(gasto.concepto, nuevo_concepto)
        self.assertEqual(gasto.valor, nuevo_valor)
        self.assertEqual(gasto.fecha, nueva_fecha)
        self.assertEqual(len(gastos_viajero2),1)
        self.assertEqual(len(gastos_viajero1),0)

