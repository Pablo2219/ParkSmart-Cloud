# ParkSmart — privacidad y Ley 8968

> Documento técnico de implementación. No constituye asesoría legal ni sustituye la revisión del responsable de la base de datos y asesoría jurídica.

ParkSmart incorpora controles técnicos alineados con la Ley 8968 de Costa Rica y su marco reglamentario: consentimiento expreso, finalidad, minimización, acceso a los datos y revocación.

## Datos que se solicitan

- Cuenta: usuario, correo y contraseña (la contraseña se almacena únicamente como hash Argon2).
- Cliente: identificación, nombre, apellidos, teléfono y datos necesarios para reservas.
- Proveedor: identificación, nombre comercial, teléfono, correo, dirección y coordenadas de los parqueos que administra.
- Operación: reservas, espacios, pagos y eventos necesarios para prestar el servicio.

No se solicitan datos sensibles para crear una cuenta.

## Consentimiento

El registro exige una acción afirmativa mediante checkbox y el backend guarda:

- `aceptaPrivacidad`.
- `fechaConsentimiento`.
- `versionPoliticaPrivacidad`.

El consentimiento se solicita antes de crear la cuenta y está asociado al titular.

## Finalidad y acceso por rol

- **CLIENTE:** consultar oferta, reservar, administrar sus vehículos y consultar sus propias reservas.
- **PROVEEDOR:** administrar únicamente sus sectores, espacios y reservas realizadas sobre esos espacios.
- **ADMINISTRADOR:** funciones administrativas del sistema.

El proveedor no recibe el catálogo privado de reservas de otros proveedores.

## Derechos del titular

La API incorpora:

- `GET /auth/mis-datos` para ejercer acceso.
- `POST /auth/revocar-consentimiento` para revocar el consentimiento y desactivar la cuenta.

La rectificación y supresión definitiva deben integrarse con un flujo administrativo que evalúe obligaciones de conservación, reservas, pagos y demás retenciones legales antes de eliminar o anonimizar información.

## Seguridad

- Contraseñas con Argon2 mediante `pwdlib`.
- Tokens JWT con expiración configurable.
- Separación de roles en backend.
- Validación de pertenencia: un proveedor solo puede crear espacios dentro de sus propios sectores y consultar sus propias reservas.
- `.env` y secretos fuera del repositorio.
- Coordenadas validadas por rango geográfico.

## Retención

La aplicación debe definir formalmente los plazos de conservación por categoría de dato y aplicar anonimización o eliminación cuando dejen de ser necesarios, considerando las excepciones y obligaciones legales aplicables. La Ley 8968 contempla criterios de actualidad y conservación, por lo que este punto debe quedar documentado en la política definitiva.

## Referencia normativa

La implementación se diseñó tomando como referencia el texto oficial de la **Ley N.º 8968, Ley de Protección de la Persona frente al Tratamiento de sus Datos Personales**, especialmente sus reglas sobre autodeterminación informativa, consentimiento informado, calidad de la información y derechos del titular.
