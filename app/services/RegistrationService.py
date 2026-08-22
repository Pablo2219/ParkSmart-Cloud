from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.Settings import settings
from app.models.Cliente import Cliente
from app.models.Proveedor import Proveedor
from app.models.Rol import Rol
from app.models.Usuario import Usuario
from app.schemas.auth.RegisterRequest import RegisterRequest
from app.security.PasswordManager import crear_hash


class RegistroService:
    def registrar(self, db: Session, datos: RegisterRequest):
        if db.scalar(select(Usuario).where(Usuario.nombreUsuario == datos.nombreUsuario)):
            raise ValueError("El nombre de usuario ya está registrado.")
        if db.scalar(select(Usuario).where(Usuario.correoElectronico == str(datos.correoElectronico))):
            raise ValueError("El correo electrónico ya está registrado.")

        rol = db.scalar(select(Rol).where(Rol.nombreRol == datos.rol, Rol.estado == "ACTIVO"))
        if rol is None:
            raise ValueError("El rol solicitado no está disponible.")

        id_cliente = None
        id_proveedor = None

        if datos.rol == "CLIENTE":
            if db.scalar(select(Cliente).where(Cliente.identificacion == datos.identificacion)):
                raise ValueError("La identificación ya está registrada.")
            cliente = Cliente(
                identificacion=datos.identificacion,
                nombre=datos.nombre,
                primerApellido=datos.primerApellido,
                segundoApellido=datos.segundoApellido,
                telefono=datos.telefono,
                correoElectronico=str(datos.correoElectronico),
                direccion=datos.direccion,
                estado="ACTIVO",
            )
            db.add(cliente)
            db.flush()
            id_cliente = cliente.idCliente
        else:
            if db.scalar(select(Proveedor).where(Proveedor.identificacion == datos.identificacion)):
                raise ValueError("La identificación del proveedor ya está registrada.")
            proveedor = Proveedor(
                identificacion=datos.identificacion,
                nombreComercial=datos.nombreComercial,
                telefono=datos.telefono,
                correoElectronico=str(datos.correoElectronico),
                direccion=datos.direccion,
                estado="ACTIVO",
            )
            db.add(proveedor)
            db.flush()
            id_proveedor = proveedor.idProveedor

        usuario = Usuario(
            idRol=rol.idRol,
            idCliente=id_cliente,
            idProveedor=id_proveedor,
            nombreUsuario=datos.nombreUsuario,
            correoElectronico=str(datos.correoElectronico),
            contrasenaHash=crear_hash(datos.contrasena),
            estado="ACTIVO",
            aceptaPrivacidad=True,
            fechaConsentimiento=datetime.now(),
            versionPoliticaPrivacidad=settings.PRIVACY_POLICY_VERSION,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return {
            "idUsuario": usuario.idUsuario,
            "nombreUsuario": usuario.nombreUsuario,
            "correoElectronico": usuario.correoElectronico,
            "rol": datos.rol,
            "idCliente": id_cliente,
            "idProveedor": id_proveedor,
            "politicaPrivacidad": settings.PRIVACY_POLICY_VERSION,
        }


registro_service = RegistroService()
