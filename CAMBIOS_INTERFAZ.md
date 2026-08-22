# ParkSmart · Rediseño de interfaz

La interfaz fue reorientada como una aplicación para clientes. La API, la base de datos y la configuración Docker se conservaron sin cambios.

## Cómo probarla

1. Iniciar la API y MySQL:

   ```bash
   docker compose up --build
   ```

2. Servir la carpeta `frontend` en el puerto 5500. En Visual Studio Code se puede abrir `frontend/index.html` con Live Server. También se puede ejecutar:

   ```bash
   python -m http.server 5500 --directory frontend
   ```

3. Abrir `http://127.0.0.1:5500`.

Si la API no responde, la interfaz entra en **modo demostración**. Este modo permite revisar el diseño y simular una reserva sin modificar la base de datos.

## Funciones conectadas

- Consulta de espacios disponibles y sectores.
- Consulta de reservas, vehículos y notificaciones del cliente con ID 1.
- Creación y cancelación de reservas.
- Generación y visualización del código QR de acceso.
- Consulta de pagos vinculados a las ocupaciones de las reservas del cliente.
- Tema claro y oscuro.
- Geolocalización y mapa, con una alternativa visual si Leaflet no carga.

El cliente actual se define con `parksmart_cliente_id` en `localStorage`; mientras no exista autenticación se utiliza el ID 1.

## Backend recomendado para la siguiente etapa

Para convertir el prototipo en una app completa todavía conviene incorporar:

- Autenticación y sesión para obtener el cliente actual sin usar un ID fijo.
- Entidad de parqueo o sede con nombre, coordenadas, horario, fotografías y servicios.
- Tarifas reales por parqueo, tipo de espacio, fracción y horario.
- Disponibilidad calculada por rango de fecha y hora, no solo por estado actual.
- Pasarela de pago o integración SINPE/tarjeta.
- Endpoint seguro para validar el QR desde el dispositivo de entrada.
- Flujo para registrar vehículos desde la aplicación.
- Historial de pagos filtrado directamente por cliente.

La tarifa de ₡700 por hora mostrada en la interfaz es únicamente una referencia visual hasta que la API incluya tarifas configurables.
