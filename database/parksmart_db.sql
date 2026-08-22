-- MySQL dump 10.13  Distrib 8.4.6, for Win64 (x86_64)
--
-- Host: localhost    Database: parksmart
-- ------------------------------------------------------
-- Server version	8.4.6

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `parksmart`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `parksmart` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `parksmart`;

--
-- Table structure for table `bitacora`
--

DROP TABLE IF EXISTS `bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bitacora` (
  `idBitacora` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del registro de bitacora',
  `idUsuario` bigint unsigned DEFAULT NULL COMMENT 'Usuario que realizo la accion',
  `modulo` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Modulo del sistema donde ocurrio la accion',
  `accion` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Accion realizada por el usuario',
  `descripcion` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Descripcion detallada de la accion realizada',
  `resultado` enum('EXITOSO','FALLIDO','ADVERTENCIA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EXITOSO' COMMENT 'Resultado de la accion realizada',
  `direccionIp` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Direccion IP desde donde se realizo la accion',
  `userAgent` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Informacion del navegador o cliente utilizado',
  `fechaRegistro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en que se registro la accion',
  PRIMARY KEY (`idBitacora`),
  KEY `IX_Bitacora_Modulo` (`modulo`),
  KEY `IX_Bitacora_Accion` (`accion`),
  KEY `IX_Bitacora_Resultado` (`resultado`),
  KEY `IX_Bitacora_FechaRegistro` (`fechaRegistro`),
  KEY `IX_Bitacora_IdUsuario` (`idUsuario`),
  CONSTRAINT `FK_Bitacora_Usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Registro de acciones realizadas dentro del sistema ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora`
--

LOCK TABLES `bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora` DISABLE KEYS */;
INSERT INTO `bitacora` VALUES (1,NULL,'Cliente','INSERT','Se registro el cliente con identificacion: 118880999','EXITOSO',NULL,NULL,'2026-07-02 21:00:49'),(2,NULL,'Reserva','INSERT','Se creo la reserva: RES-20260702212328766168','EXITOSO',NULL,NULL,'2026-07-02 21:23:28'),(3,NULL,'Reserva','INSERT','Se creo la reserva: RES-20260705212249482986','EXITOSO',NULL,NULL,'2026-07-05 21:22:49'),(4,NULL,'Pago','UPDATE','Se registro el pago: PAG-20260705221428254069','EXITOSO',NULL,NULL,'2026-07-05 22:24:34');
/*!40000 ALTER TABLE `bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idCliente` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del cliente',
  `identificacion` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Documento oficial de identificacion',
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Nombre del cliente',
  `primerApellido` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Primer apellido del cliente',
  `segundoApellido` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Segundo apellido del cliente',
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Numero de telefono de contacto',
  `correoElectronico` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Correo electronico del cliente',
  `direccion` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Direccion fisica del cliente',
  `estado` enum('ACTIVO','INACTIVO','SUSPENDIDO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO' COMMENT 'Estado actual del cliente',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  `provincia` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Provincia del cliente',
  `canton` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Canton del cliente',
  `distrito` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Distrito del cliente',
  `direccionExacta` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Direccion exacta del cliente',
  PRIMARY KEY (`idCliente`),
  UNIQUE KEY `UK_Cliente_Identificacion` (`identificacion`),
  UNIQUE KEY `UK_Cliente_CorreoElectronico` (`correoElectronico`),
  KEY `IX_Cliente_PrimerApellido` (`primerApellido`),
  KEY `IX_Cliente_Telefono` (`telefono`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Informacion de los clientes registrados en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'118880999','Carlos','Prueba','ParkSmart','88889999','carlos.prueba@parksmart.com',NULL,'ACTIVO','2026-07-02 21:00:49','2026-07-02 21:00:49','San Jose','Central','Carmen','Frente al parque central');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `deuda`
--

DROP TABLE IF EXISTS `deuda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deuda` (
  `idDeuda` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico de la deuda',
  `idPago` bigint unsigned NOT NULL COMMENT 'Pago asociado a la deuda',
  `codigoDeuda` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Codigo unico de referencia de la deuda',
  `montoDeuda` decimal(10,2) NOT NULL COMMENT 'Monto total adeudado',
  `fechaGeneracion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en que se genero la deuda',
  `fechaLimite` datetime NOT NULL COMMENT 'Fecha limite para cancelar la deuda',
  `estado` enum('PENDIENTE','PAGADA','VENCIDA','ANULADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado actual de la deuda',
  `observaciones` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Observaciones adicionales de la deuda',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idDeuda`),
  UNIQUE KEY `UK_Deuda_CodigoDeuda` (`codigoDeuda`),
  UNIQUE KEY `UK_Deuda_IdPago` (`idPago`),
  KEY `IX_Deuda_Estado` (`estado`),
  KEY `IX_Deuda_FechaLimite` (`fechaLimite`),
  CONSTRAINT `FK_Deuda_Pago` FOREIGN KEY (`idPago`) REFERENCES `pago` (`idPago`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `CK_Deuda_Monto` CHECK ((`montoDeuda` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Deudas generadas por pagos vencidos en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deuda`
--

LOCK TABLES `deuda` WRITE;
/*!40000 ALTER TABLE `deuda` DISABLE KEYS */;
/*!40000 ALTER TABLE `deuda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `espacio`
--

DROP TABLE IF EXISTS `espacio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `espacio` (
  `idEspacio` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del espacio de parqueo',
  `idSector` bigint unsigned NOT NULL COMMENT 'Sector al que pertenece el espacio',
  `codigoEspacio` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Codigo visible del espacio de parqueo',
  `tipoEspacio` enum('REGULAR','MOTOCICLETA','DISCAPACIDAD','ELECTRICO','VIP') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'REGULAR' COMMENT 'Tipo de espacio de parqueo',
  `estado` enum('DISPONIBLE','OCUPADO','RESERVADO','MANTENIMIENTO','INACTIVO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'DISPONIBLE' COMMENT 'Estado actual del espacio',
  `descripcion` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Descripcion opcional del espacio',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idEspacio`),
  UNIQUE KEY `UK_Espacio_CodigoEspacio` (`codigoEspacio`),
  KEY `IX_Espacio_IdSector` (`idSector`),
  KEY `IX_Espacio_TipoEspacio` (`tipoEspacio`),
  KEY `IX_Espacio_Estado` (`estado`),
  CONSTRAINT `FK_Espacio_Sector` FOREIGN KEY (`idSector`) REFERENCES `sector` (`idSector`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Espacios individuales de parqueo registrados en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `espacio`
--

LOCK TABLES `espacio` WRITE;
/*!40000 ALTER TABLE `espacio` DISABLE KEYS */;
INSERT INTO `espacio` VALUES (1,1,'A-01','REGULAR','RESERVADO','Espacio de prueba','2026-07-02 21:20:09','2026-07-02 21:23:28'),(2,1,'A-02','REGULAR','DISPONIBLE','Segundo espacio de prueba','2026-07-05 21:22:03','2026-07-05 21:58:48');
/*!40000 ALTER TABLE `espacio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificacion`
--

DROP TABLE IF EXISTS `notificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificacion` (
  `idNotificacion` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico de la notificacion',
  `idCliente` bigint unsigned NOT NULL COMMENT 'Cliente que recibe la notificacion',
  `idReserva` bigint unsigned DEFAULT NULL COMMENT 'Reserva relacionada con la notificacion',
  `idPago` bigint unsigned DEFAULT NULL COMMENT 'Pago relacionado con la notificacion',
  `idDeuda` bigint unsigned DEFAULT NULL COMMENT 'Deuda asociada a la notificacion',
  `tipoNotificacion` enum('RESERVA','PAGO','DEUDA','SISTEMA') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Tipo de notificacion generada',
  `canal` enum('EMAIL','SMS','WHATSAPP','PUSH') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EMAIL' COMMENT 'Canal utilizado para enviar la notificacion',
  `titulo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Titulo de la notificacion',
  `mensaje` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Contenido del mensaje enviado',
  `destinatario` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Destinatario de la notificacion',
  `estado` enum('PENDIENTE','ENVIADA','LEIDA','ERROR') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado de la notificacion',
  `fechaEnvio` datetime DEFAULT NULL COMMENT 'Fecha en que se envio la notificacion',
  `fechaLectura` datetime DEFAULT NULL COMMENT 'Fecha en que el cliente leyo la notificacion',
  `observaciones` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Observaciones adicionales de la notificacion',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idNotificacion`),
  KEY `FK_Notificacion_Reserva` (`idReserva`),
  KEY `FK_Notificacion_Pago` (`idPago`),
  KEY `IX_Notificacion_Estado` (`estado`),
  KEY `IX_Notificacion_Tipo` (`tipoNotificacion`),
  KEY `IX_Notificacion_Canal` (`canal`),
  KEY `IX_Notificacion_FechaEnvio` (`fechaEnvio`),
  KEY `IX_Notificacion_IdCliente` (`idCliente`),
  CONSTRAINT `FK_Notificacion_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FK_Notificacion_Pago` FOREIGN KEY (`idPago`) REFERENCES `pago` (`idPago`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `FK_Notificacion_Reserva` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Notificaciones enviadas a los clientes de ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacion`
--

LOCK TABLES `notificacion` WRITE;
/*!40000 ALTER TABLE `notificacion` DISABLE KEYS */;
INSERT INTO `notificacion` VALUES (1,1,2,1,NULL,'PAGO','EMAIL','Pago confirmado','Su pago fue registrado correctamente en ParkSmart.',NULL,'PENDIENTE',NULL,NULL,NULL,'2026-07-05 22:40:11','2026-07-05 22:40:11');
/*!40000 ALTER TABLE `notificacion` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ocupacion`
--

DROP TABLE IF EXISTS `ocupacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocupacion` (
  `idOcupacion` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico de la ocupacion',
  `idReserva` bigint unsigned NOT NULL COMMENT 'Reserva asociada a la ocupacion',
  `idEspacio` bigint unsigned DEFAULT NULL COMMENT 'Espacio asociado a la ocupacion',
  `idQr` bigint unsigned DEFAULT NULL COMMENT 'Codigo QR asociado a la ocupacion',
  `fechaEntrada` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de ingreso al parqueo',
  `fechaSalida` datetime DEFAULT NULL COMMENT 'Fecha y hora de salida del parqueo',
  `tiempoTotalMinutos` int unsigned DEFAULT NULL COMMENT 'Tiempo total de ocupacion en minutos',
  `estado` enum('EN_CURSO','FINALIZADA','CANCELADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'EN_CURSO' COMMENT 'Estado actual de la ocupacion',
  `observaciones` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Observaciones adicionales de la ocupacion',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idOcupacion`),
  UNIQUE KEY `UK_Ocupacion_IdReserva` (`idReserva`),
  UNIQUE KEY `UK_Ocupacion_IdQr` (`idQr`),
  KEY `IX_Ocupacion_Estado` (`estado`),
  KEY `IX_Ocupacion_FechaEntrada` (`fechaEntrada`),
  KEY `IX_Ocupacion_FechaSalida` (`fechaSalida`),
  CONSTRAINT `FK_Ocupacion_Qr` FOREIGN KEY (`idQr`) REFERENCES `qr` (`idQr`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FK_Ocupacion_Reserva` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `CK_Ocupacion_Fechas` CHECK (((`fechaSalida` is null) or (`fechaSalida` > `fechaEntrada`)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Registro del uso real de los espacios de parqueo en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocupacion`
--

LOCK TABLES `ocupacion` WRITE;
/*!40000 ALTER TABLE `ocupacion` DISABLE KEYS */;
INSERT INTO `ocupacion` VALUES (1,2,2,NULL,'2026-07-05 21:37:05','2026-07-05 21:58:49',21,'FINALIZADA','Inicio de ocupacion desde Swagger','2026-07-05 21:37:05','2026-07-05 21:58:48');
/*!40000 ALTER TABLE `ocupacion` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `idPago` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del pago',
  `idOcupacion` bigint unsigned NOT NULL COMMENT 'Ocupacion asociada al pago',
  `codigoPago` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Codigo unico de referencia del pago',
  `tiempoCobradoMinutos` int unsigned DEFAULT '1' COMMENT 'Tiempo cobrado en minutos',
  `tarifaPorHora` decimal(10,2) DEFAULT '0.00' COMMENT 'Tarifa por hora aplicada',
  `montoSubtotal` decimal(10,2) DEFAULT '0.00' COMMENT 'Subtotal del pago',
  `montoImpuesto` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT 'Monto correspondiente a impuestos',
  `montoTotal` decimal(10,2) NOT NULL COMMENT 'Monto total a pagar',
  `metodoPago` enum('EFECTIVO','TARJETA','SINPE','PASARELA') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Metodo utilizado para realizar el pago',
  `estado` enum('PENDIENTE','PAGADO','RECHAZADO','VENCIDO','ANULADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado actual del pago',
  `fechaGeneracion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en que se genero el pago',
  `fechaLimitePago` datetime DEFAULT NULL COMMENT 'Fecha limite para realizar el pago',
  `fechaPago` datetime DEFAULT NULL COMMENT 'Fecha en que se realizo el pago',
  `referenciaTransaccion` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Referencia de la transaccion del pago',
  `numeroComprobante` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Numero de comprobante o referencia del pago',
  `observaciones` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Observaciones adicionales del pago',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idPago`),
  UNIQUE KEY `UK_Pago_CodigoPago` (`codigoPago`),
  UNIQUE KEY `UK_Pago_IdOcupacion` (`idOcupacion`),
  KEY `IX_Pago_Estado` (`estado`),
  KEY `IX_Pago_MetodoPago` (`metodoPago`),
  KEY `IX_Pago_FechaLimitePago` (`fechaLimitePago`),
  KEY `IX_Pago_FechaPago` (`fechaPago`),
  CONSTRAINT `FK_Pago_Ocupacion` FOREIGN KEY (`idOcupacion`) REFERENCES `ocupacion` (`idOcupacion`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `CK_Pago_MontoImpuesto` CHECK ((`montoImpuesto` >= 0)),
  CONSTRAINT `CK_Pago_MontoSubtotal` CHECK ((`montoSubtotal` >= 0)),
  CONSTRAINT `CK_Pago_MontoTotal` CHECK ((`montoTotal` >= 0)),
  CONSTRAINT `CK_Pago_TarifaPorHora` CHECK ((`tarifaPorHora` >= 0)),
  CONSTRAINT `CK_Pago_TiempoCobrado` CHECK ((`tiempoCobradoMinutos` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Pagos generados por la ocupacion de espacios en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
INSERT INTO `pago` VALUES (1,1,'PAG-20260705221428254069',1,0.00,0.00,0.00,0.00,'EFECTIVO','PAGADO','2026-07-05 22:14:28','2026-07-06 22:14:28','2026-07-05 22:24:34','string',NULL,'string','2026-07-05 22:14:28','2026-07-05 22:24:34');
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `qr`
--

DROP TABLE IF EXISTS `qr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qr` (
  `idQr` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del codigo QR',
  `idReserva` bigint unsigned NOT NULL COMMENT 'Reserva asociada al codigo QR',
  `codigoQr` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Codigo unico generado para el QR',
  `tokenQr` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Token de seguridad asociado al codigo QR',
  `fechaGeneracion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en que se genero el codigo QR',
  `fechaValidezInicio` datetime DEFAULT NULL COMMENT 'Fecha y hora desde la cual el QR es valido',
  `fechaValidezFin` datetime DEFAULT NULL COMMENT 'Fecha y hora hasta la cual el QR es valido',
  `fechaActivacion` datetime DEFAULT NULL COMMENT 'Fecha de activacion del codigo QR',
  `fechaExpiracion` datetime DEFAULT NULL COMMENT 'Fecha de expiracion del codigo QR',
  `fechaUso` datetime DEFAULT NULL COMMENT 'Fecha y hora en que el QR fue utilizado',
  `estado` enum('GENERADO','ACTIVO','USADO','VENCIDO','CANCELADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'GENERADO' COMMENT 'Estado actual del codigo QR',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idQr`),
  UNIQUE KEY `UK_Qr_CodigoQr` (`codigoQr`),
  UNIQUE KEY `UK_Qr_IdReserva` (`idReserva`),
  KEY `IX_Qr_Estado` (`estado`),
  KEY `IX_Qr_Fechas` (`fechaActivacion`,`fechaExpiracion`),
  CONSTRAINT `FK_Qr_Reserva` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `CK_Qr_Fechas` CHECK ((`fechaExpiracion` > `fechaActivacion`))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Codigos QR generados para las reservas de ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qr`
--

LOCK TABLES `qr` WRITE;
/*!40000 ALTER TABLE `qr` DISABLE KEYS */;
INSERT INTO `qr` VALUES (1,1,'QR-20260702224229998858','wtOsQW3oUoPCsgt2zmwGM66CZzzxdhuAHtg1UG68ZUQ','2026-07-02 22:42:30','2026-07-02 21:20:00','2026-07-02 22:30:00',NULL,NULL,NULL,'GENERADO','2026-07-02 22:42:30','2026-07-02 22:42:30'),(2,2,'QR-20260705212316653107','YZerMAsb47hl2_HHLZG9T1U7DFplNhJ6mN8kD5JG-xg','2026-07-05 21:23:16','2026-07-05 21:15:00','2026-07-05 22:25:00',NULL,NULL,'2026-07-05 21:26:55','USADO','2026-07-05 21:23:16','2026-07-05 21:26:54');
/*!40000 ALTER TABLE `qr` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `idReserva` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico de la reserva',
  `idCliente` bigint unsigned NOT NULL COMMENT 'Cliente que realiza la reserva',
  `idVehiculo` bigint unsigned NOT NULL COMMENT 'Vehiculo asociado a la reserva',
  `idEspacio` bigint unsigned NOT NULL COMMENT 'Espacio reservado por el cliente',
  `codigoReserva` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Codigo unico de referencia de la reserva',
  `fechaInicioReserva` datetime NOT NULL COMMENT 'Fecha y hora de inicio de la reserva',
  `fechaFinReserva` datetime NOT NULL COMMENT 'Fecha y hora final de la reserva',
  `estado` enum('PENDIENTE','CONFIRMADA','CANCELADA','VENCIDA','UTILIZADA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado actual de la reserva',
  `observaciones` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Observaciones adicionales de la reserva',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idReserva`),
  UNIQUE KEY `UK_Reserva_CodigoReserva` (`codigoReserva`),
  KEY `IX_Reserva_IdCliente` (`idCliente`),
  KEY `IX_Reserva_IdVehiculo` (`idVehiculo`),
  KEY `IX_Reserva_IdEspacio` (`idEspacio`),
  KEY `IX_Reserva_Estado` (`estado`),
  KEY `IX_Reserva_Fechas` (`fechaInicioReserva`,`fechaFinReserva`),
  CONSTRAINT `FK_Reserva_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FK_Reserva_Espacio` FOREIGN KEY (`idEspacio`) REFERENCES `espacio` (`idEspacio`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FK_Reserva_Vehiculo` FOREIGN KEY (`idVehiculo`) REFERENCES `vehiculo` (`idVehiculo`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `CK_Reserva_Fechas` CHECK ((`fechaFinReserva` > `fechaInicioReserva`))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Reservas realizadas por los clientes en ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
INSERT INTO `reserva` VALUES (1,1,1,1,'RES-20260702212328766168','2026-07-02 21:30:00','2026-07-02 22:30:00','CONFIRMADA','Reserva de prueba desde Swagger','2026-07-02 21:23:28','2026-07-02 21:23:28'),(2,1,1,2,'RES-20260705212249482986','2026-07-05 21:25:00','2026-07-05 22:25:00','UTILIZADA','Reserva actual para prueba de QR y ocupacion','2026-07-05 21:22:49','2026-07-05 21:26:54');
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `idRol` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del rol',
  `nombreRol` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Nombre del rol dentro del sistema',
  `descripcion` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Descripcion general del rol',
  `estado` enum('ACTIVO','INACTIVO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO' COMMENT 'Estado actual del rol',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idRol`),
  UNIQUE KEY `UK_Rol_NombreRol` (`nombreRol`),
  KEY `IX_Rol_Estado` (`estado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Roles de usuario del sistema ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'ADMINISTRADOR','Usuario con acceso completo al sistema ParkSmart','ACTIVO','2026-07-02 20:08:29','2026-07-02 20:08:29'),(2,'CLIENTE','Usuario cliente de la aplicacion ParkSmart','ACTIVO','2026-07-02 20:08:29','2026-07-02 20:08:29'),(3,'OPERADOR','Usuario encargado de la gestion operativa del parqueo','ACTIVO','2026-07-02 20:08:29','2026-07-02 20:08:29');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sector`
--

DROP TABLE IF EXISTS `sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sector` (
  `idSector` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del sector',
  `nombreSector` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Nombre del sector del parqueo',
  `descripcion` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Descripcion general del sector',
  `ubicacion` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Ubicacion fisica del sector dentro del parqueo',
  `estado` enum('ACTIVO','INACTIVO','MANTENIMIENTO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO' COMMENT 'Estado actual del sector',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idSector`),
  UNIQUE KEY `UK_Sector_NombreSector` (`nombreSector`),
  KEY `IX_Sector_Estado` (`estado`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Sectores o zonas disponibles dentro del parqueo ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sector`
--

LOCK TABLES `sector` WRITE;
/*!40000 ALTER TABLE `sector` DISABLE KEYS */;
INSERT INTO `sector` VALUES (1,'Sector A','Sector principal del parqueo','Entrada principal','ACTIVO','2026-07-02 21:17:17','2026-07-02 21:17:17');
/*!40000 ALTER TABLE `sector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del usuario',
  `idRol` bigint unsigned NOT NULL COMMENT 'Rol asignado al usuario',
  `idCliente` bigint unsigned DEFAULT NULL COMMENT 'Cliente relacionado con el usuario, si aplica',
  `nombreUsuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Nombre de usuario para iniciar sesion',
  `correoElectronico` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Correo electronico del usuario',
  `contrasenaHash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Contrasena cifrada del usuario',
  `estado` enum('ACTIVO','INACTIVO','BLOQUEADO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO' COMMENT 'Estado actual del usuario',
  `ultimoAcceso` datetime DEFAULT NULL COMMENT 'Fecha del ultimo acceso al sistema',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `UK_Usuario_NombreUsuario` (`nombreUsuario`),
  UNIQUE KEY `UK_Usuario_CorreoElectronico` (`correoElectronico`),
  KEY `IX_Usuario_Estado` (`estado`),
  KEY `IX_Usuario_UltimoAcceso` (`ultimoAcceso`),
  KEY `IX_Usuario_IdRol` (`idRol`),
  KEY `IX_Usuario_IdCliente` (`idCliente`),
  CONSTRAINT `FK_Usuario_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `FK_Usuario_Rol` FOREIGN KEY (`idRol`) REFERENCES `rol` (`idRol`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Usuarios con acceso al sistema ParkSmart';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiculo`
--

DROP TABLE IF EXISTS `vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiculo` (
  `idVehiculo` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identificador unico del vehiculo',
  `idCliente` bigint unsigned NOT NULL COMMENT 'Cliente propietario del vehiculo',
  `placa` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Numero de placa del vehiculo',
  `marca` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Marca del vehiculo',
  `modelo` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Modelo del vehiculo',
  `color` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Color del vehiculo',
  `tipoVehiculo` enum('AUTOMOVIL','MOTOCICLETA','CAMIONETA','OTRO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'AUTOMOVIL' COMMENT 'Tipo de vehiculo registrado',
  `estado` enum('ACTIVO','INACTIVO') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO' COMMENT 'Estado actual del vehiculo',
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creacion del registro',
  `fechaActualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ultima actualizacion del registro',
  PRIMARY KEY (`idVehiculo`),
  UNIQUE KEY `UK_Vehiculo_Placa` (`placa`),
  KEY `IX_Vehiculo_IdCliente` (`idCliente`),
  KEY `IX_Vehiculo_TipoVehiculo` (`tipoVehiculo`),
  KEY `IX_Vehiculo_Estado` (`estado`),
  CONSTRAINT `FK_Vehiculo_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Informacion de los vehiculos registrados por los clientes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiculo`
--

LOCK TABLES `vehiculo` WRITE;
/*!40000 ALTER TABLE `vehiculo` DISABLE KEYS */;
INSERT INTO `vehiculo` VALUES (1,1,'ABC123','Toyota','Rav4','Gris','AUTOMOVIL','ACTIVO','2026-07-02 21:03:41','2026-07-02 21:03:41');
/*!40000 ALTER TABLE `vehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_bitacoradetalle`
--

DROP TABLE IF EXISTS `vw_bitacoradetalle`;
/*!50001 DROP VIEW IF EXISTS `vw_bitacoradetalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_bitacoradetalle` AS SELECT 
 1 AS `idBitacora`,
 1 AS `modulo`,
 1 AS `accion`,
 1 AS `descripcion`,
 1 AS `resultado`,
 1 AS `direccionIp`,
 1 AS `fechaRegistro`,
 1 AS `idUsuario`,
 1 AS `nombreUsuario`,
 1 AS `idRol`,
 1 AS `nombreRol`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_clientesactivos`
--

DROP TABLE IF EXISTS `vw_clientesactivos`;
/*!50001 DROP VIEW IF EXISTS `vw_clientesactivos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_clientesactivos` AS SELECT 
 1 AS `idCliente`,
 1 AS `identificacion`,
 1 AS `nombreCompleto`,
 1 AS `telefono`,
 1 AS `correoElectronico`,
 1 AS `estado`,
 1 AS `fechaCreacion`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_deudaspendientes`
--

DROP TABLE IF EXISTS `vw_deudaspendientes`;
/*!50001 DROP VIEW IF EXISTS `vw_deudaspendientes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_deudaspendientes` AS SELECT 
 1 AS `idDeuda`,
 1 AS `codigoDeuda`,
 1 AS `montoDeuda`,
 1 AS `fechaGeneracion`,
 1 AS `fechaLimite`,
 1 AS `estadoDeuda`,
 1 AS `idPago`,
 1 AS `codigoPago`,
 1 AS `montoTotal`,
 1 AS `estadoPago`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `telefono`,
 1 AS `correoElectronico`,
 1 AS `placa`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_espaciosdisponibles`
--

DROP TABLE IF EXISTS `vw_espaciosdisponibles`;
/*!50001 DROP VIEW IF EXISTS `vw_espaciosdisponibles`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_espaciosdisponibles` AS SELECT 
 1 AS `idEspacio`,
 1 AS `codigoEspacio`,
 1 AS `tipoEspacio`,
 1 AS `estadoEspacio`,
 1 AS `idSector`,
 1 AS `nombreSector`,
 1 AS `ubicacion`,
 1 AS `estadoSector`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_notificacionespendientes`
--

DROP TABLE IF EXISTS `vw_notificacionespendientes`;
/*!50001 DROP VIEW IF EXISTS `vw_notificacionespendientes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_notificacionespendientes` AS SELECT 
 1 AS `idNotificacion`,
 1 AS `tipoNotificacion`,
 1 AS `canal`,
 1 AS `titulo`,
 1 AS `mensaje`,
 1 AS `destinatario`,
 1 AS `estado`,
 1 AS `fechaCreacion`,
 1 AS `idCliente`,
 1 AS `nombreCliente`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ocupacionesactivas`
--

DROP TABLE IF EXISTS `vw_ocupacionesactivas`;
/*!50001 DROP VIEW IF EXISTS `vw_ocupacionesactivas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ocupacionesactivas` AS SELECT 
 1 AS `idOcupacion`,
 1 AS `fechaEntrada`,
 1 AS `fechaSalida`,
 1 AS `estadoOcupacion`,
 1 AS `idReserva`,
 1 AS `codigoReserva`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `idVehiculo`,
 1 AS `placa`,
 1 AS `tipoVehiculo`,
 1 AS `idEspacio`,
 1 AS `codigoEspacio`,
 1 AS `nombreSector`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_pagospendientes`
--

DROP TABLE IF EXISTS `vw_pagospendientes`;
/*!50001 DROP VIEW IF EXISTS `vw_pagospendientes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_pagospendientes` AS SELECT 
 1 AS `idPago`,
 1 AS `codigoPago`,
 1 AS `tiempoCobradoMinutos`,
 1 AS `tarifaPorHora`,
 1 AS `montoSubtotal`,
 1 AS `montoImpuesto`,
 1 AS `montoTotal`,
 1 AS `estadoPago`,
 1 AS `fechaLimitePago`,
 1 AS `idOcupacion`,
 1 AS `idReserva`,
 1 AS `codigoReserva`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `telefono`,
 1 AS `correoElectronico`,
 1 AS `placa`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_qractivos`
--

DROP TABLE IF EXISTS `vw_qractivos`;
/*!50001 DROP VIEW IF EXISTS `vw_qractivos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_qractivos` AS SELECT 
 1 AS `idQr`,
 1 AS `codigoQr`,
 1 AS `fechaGeneracion`,
 1 AS `fechaActivacion`,
 1 AS `fechaExpiracion`,
 1 AS `estadoQr`,
 1 AS `idReserva`,
 1 AS `codigoReserva`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `placa`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_reservasactivas`
--

DROP TABLE IF EXISTS `vw_reservasactivas`;
/*!50001 DROP VIEW IF EXISTS `vw_reservasactivas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_reservasactivas` AS SELECT 
 1 AS `idReserva`,
 1 AS `codigoReserva`,
 1 AS `fechaInicioReserva`,
 1 AS `fechaFinReserva`,
 1 AS `estadoReserva`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `placa`,
 1 AS `codigoEspacio`,
 1 AS `nombreSector`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_reservasdetalle`
--

DROP TABLE IF EXISTS `vw_reservasdetalle`;
/*!50001 DROP VIEW IF EXISTS `vw_reservasdetalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_reservasdetalle` AS SELECT 
 1 AS `idReserva`,
 1 AS `codigoReserva`,
 1 AS `fechaInicioReserva`,
 1 AS `fechaFinReserva`,
 1 AS `estadoReserva`,
 1 AS `idCliente`,
 1 AS `nombreCliente`,
 1 AS `telefono`,
 1 AS `correoElectronico`,
 1 AS `idVehiculo`,
 1 AS `placa`,
 1 AS `marca`,
 1 AS `modelo`,
 1 AS `color`,
 1 AS `tipoVehiculo`,
 1 AS `idEspacio`,
 1 AS `codigoEspacio`,
 1 AS `tipoEspacio`,
 1 AS `estadoEspacio`,
 1 AS `idSector`,
 1 AS `nombreSector`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'parksmart'
--

--
-- Dumping routines for database 'parksmart'
--
/*!50003 DROP FUNCTION IF EXISTS `FN_CalcularHorasCobro` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_CalcularImpuesto` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_CalcularSubtotalPago` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_CalcularTiempoOcupacion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_CalcularTotalPago` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_ValidarQrActivo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `FN_VerificarPagoVencido` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CancelarReserva` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CrearReserva` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_FinalizarOcupacionGenerarPago` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_GenerarDeudaPago` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_GenerarQrReserva` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_IniciarOcupacion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_RegistrarCliente` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_RegistrarPago` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_RegistrarVehiculo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
 ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `parksmart`
--

USE `parksmart`;

--
-- Final view structure for view `vw_bitacoradetalle`
--

/*!50001 DROP VIEW IF EXISTS `vw_bitacoradetalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_bitacoradetalle` AS select `b`.`idBitacora` AS `idBitacora`,`b`.`modulo` AS `modulo`,`b`.`accion` AS `accion`,`b`.`descripcion` AS `descripcion`,`b`.`resultado` AS `resultado`,`b`.`direccionIp` AS `direccionIp`,`b`.`fechaRegistro` AS `fechaRegistro`,`u`.`idUsuario` AS `idUsuario`,`u`.`nombreUsuario` AS `nombreUsuario`,`r`.`idRol` AS `idRol`,`r`.`nombreRol` AS `nombreRol` from ((`bitacora` `b` left join `usuario` `u` on((`b`.`idUsuario` = `u`.`idUsuario`))) left join `rol` `r` on((`u`.`idRol` = `r`.`idRol`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_clientesactivos`
--

/*!50001 DROP VIEW IF EXISTS `vw_clientesactivos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_clientesactivos` AS select `c`.`idCliente` AS `idCliente`,`c`.`identificacion` AS `identificacion`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCompleto`,`c`.`telefono` AS `telefono`,`c`.`correoElectronico` AS `correoElectronico`,`c`.`estado` AS `estado`,`c`.`fechaCreacion` AS `fechaCreacion` from `cliente` `c` where (`c`.`estado` = 'ACTIVO') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_deudaspendientes`
--

/*!50001 DROP VIEW IF EXISTS `vw_deudaspendientes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_deudaspendientes` AS select `d`.`idDeuda` AS `idDeuda`,`d`.`codigoDeuda` AS `codigoDeuda`,`d`.`montoDeuda` AS `montoDeuda`,`d`.`fechaGeneracion` AS `fechaGeneracion`,`d`.`fechaLimite` AS `fechaLimite`,`d`.`estado` AS `estadoDeuda`,`p`.`idPago` AS `idPago`,`p`.`codigoPago` AS `codigoPago`,`p`.`montoTotal` AS `montoTotal`,`p`.`estado` AS `estadoPago`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`c`.`telefono` AS `telefono`,`c`.`correoElectronico` AS `correoElectronico`,`v`.`placa` AS `placa` from (((((`deuda` `d` join `pago` `p` on((`d`.`idPago` = `p`.`idPago`))) join `ocupacion` `o` on((`p`.`idOcupacion` = `o`.`idOcupacion`))) join `reserva` `r` on((`o`.`idReserva` = `r`.`idReserva`))) join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) where (`d`.`estado` in ('PENDIENTE','VENCIDA')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_espaciosdisponibles`
--

/*!50001 DROP VIEW IF EXISTS `vw_espaciosdisponibles`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_espaciosdisponibles` AS select `e`.`idEspacio` AS `idEspacio`,`e`.`codigoEspacio` AS `codigoEspacio`,`e`.`tipoEspacio` AS `tipoEspacio`,`e`.`estado` AS `estadoEspacio`,`s`.`idSector` AS `idSector`,`s`.`nombreSector` AS `nombreSector`,`s`.`ubicacion` AS `ubicacion`,`s`.`estado` AS `estadoSector` from (`espacio` `e` join `sector` `s` on((`e`.`idSector` = `s`.`idSector`))) where ((`e`.`estado` = 'DISPONIBLE') and (`s`.`estado` = 'ACTIVO')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_notificacionespendientes`
--

/*!50001 DROP VIEW IF EXISTS `vw_notificacionespendientes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_notificacionespendientes` AS select `n`.`idNotificacion` AS `idNotificacion`,`n`.`tipoNotificacion` AS `tipoNotificacion`,`n`.`canal` AS `canal`,`n`.`titulo` AS `titulo`,`n`.`mensaje` AS `mensaje`,`n`.`destinatario` AS `destinatario`,`n`.`estado` AS `estado`,`n`.`fechaCreacion` AS `fechaCreacion`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente` from (`notificacion` `n` join `cliente` `c` on((`n`.`idCliente` = `c`.`idCliente`))) where (`n`.`estado` = 'PENDIENTE') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ocupacionesactivas`
--

/*!50001 DROP VIEW IF EXISTS `vw_ocupacionesactivas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_ocupacionesactivas` AS select `o`.`idOcupacion` AS `idOcupacion`,`o`.`fechaEntrada` AS `fechaEntrada`,`o`.`fechaSalida` AS `fechaSalida`,`o`.`estado` AS `estadoOcupacion`,`r`.`idReserva` AS `idReserva`,`r`.`codigoReserva` AS `codigoReserva`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`v`.`idVehiculo` AS `idVehiculo`,`v`.`placa` AS `placa`,`v`.`tipoVehiculo` AS `tipoVehiculo`,`e`.`idEspacio` AS `idEspacio`,`e`.`codigoEspacio` AS `codigoEspacio`,`s`.`nombreSector` AS `nombreSector` from (((((`ocupacion` `o` join `reserva` `r` on((`o`.`idReserva` = `r`.`idReserva`))) join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) join `espacio` `e` on((`r`.`idEspacio` = `e`.`idEspacio`))) join `sector` `s` on((`e`.`idSector` = `s`.`idSector`))) where (`o`.`estado` = 'ACTIVA') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_pagospendientes`
--

/*!50001 DROP VIEW IF EXISTS `vw_pagospendientes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_pagospendientes` AS select `p`.`idPago` AS `idPago`,`p`.`codigoPago` AS `codigoPago`,`p`.`tiempoCobradoMinutos` AS `tiempoCobradoMinutos`,`p`.`tarifaPorHora` AS `tarifaPorHora`,`p`.`montoSubtotal` AS `montoSubtotal`,`p`.`montoImpuesto` AS `montoImpuesto`,`p`.`montoTotal` AS `montoTotal`,`p`.`estado` AS `estadoPago`,`p`.`fechaLimitePago` AS `fechaLimitePago`,`o`.`idOcupacion` AS `idOcupacion`,`r`.`idReserva` AS `idReserva`,`r`.`codigoReserva` AS `codigoReserva`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`c`.`telefono` AS `telefono`,`c`.`correoElectronico` AS `correoElectronico`,`v`.`placa` AS `placa` from ((((`pago` `p` join `ocupacion` `o` on((`p`.`idOcupacion` = `o`.`idOcupacion`))) join `reserva` `r` on((`o`.`idReserva` = `r`.`idReserva`))) join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) where (`p`.`estado` = 'PENDIENTE') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_qractivos`
--

/*!50001 DROP VIEW IF EXISTS `vw_qractivos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_qractivos` AS select `q`.`idQr` AS `idQr`,`q`.`codigoQr` AS `codigoQr`,`q`.`fechaGeneracion` AS `fechaGeneracion`,`q`.`fechaActivacion` AS `fechaActivacion`,`q`.`fechaExpiracion` AS `fechaExpiracion`,`q`.`estado` AS `estadoQr`,`r`.`idReserva` AS `idReserva`,`r`.`codigoReserva` AS `codigoReserva`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`v`.`placa` AS `placa` from (((`qr` `q` join `reserva` `r` on((`q`.`idReserva` = `r`.`idReserva`))) join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) where (`q`.`estado` in ('GENERADO','ACTIVO')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_reservasactivas`
--

/*!50001 DROP VIEW IF EXISTS `vw_reservasactivas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_reservasactivas` AS select `r`.`idReserva` AS `idReserva`,`r`.`codigoReserva` AS `codigoReserva`,`r`.`fechaInicioReserva` AS `fechaInicioReserva`,`r`.`fechaFinReserva` AS `fechaFinReserva`,`r`.`estado` AS `estadoReserva`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`v`.`placa` AS `placa`,`e`.`codigoEspacio` AS `codigoEspacio`,`s`.`nombreSector` AS `nombreSector` from ((((`reserva` `r` join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) join `espacio` `e` on((`r`.`idEspacio` = `e`.`idEspacio`))) join `sector` `s` on((`e`.`idSector` = `s`.`idSector`))) where (`r`.`estado` in ('PENDIENTE','CONFIRMADA')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_reservasdetalle`
--

/*!50001 DROP VIEW IF EXISTS `vw_reservasdetalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `vw_reservasdetalle` AS select `r`.`idReserva` AS `idReserva`,`r`.`codigoReserva` AS `codigoReserva`,`r`.`fechaInicioReserva` AS `fechaInicioReserva`,`r`.`fechaFinReserva` AS `fechaFinReserva`,`r`.`estado` AS `estadoReserva`,`c`.`idCliente` AS `idCliente`,concat_ws(' ',`c`.`nombre`,`c`.`primerApellido`,`c`.`segundoApellido`) AS `nombreCliente`,`c`.`telefono` AS `telefono`,`c`.`correoElectronico` AS `correoElectronico`,`v`.`idVehiculo` AS `idVehiculo`,`v`.`placa` AS `placa`,`v`.`marca` AS `marca`,`v`.`modelo` AS `modelo`,`v`.`color` AS `color`,`v`.`tipoVehiculo` AS `tipoVehiculo`,`e`.`idEspacio` AS `idEspacio`,`e`.`codigoEspacio` AS `codigoEspacio`,`e`.`tipoEspacio` AS `tipoEspacio`,`e`.`estado` AS `estadoEspacio`,`s`.`idSector` AS `idSector`,`s`.`nombreSector` AS `nombreSector` from ((((`reserva` `r` join `cliente` `c` on((`r`.`idCliente` = `c`.`idCliente`))) join `vehiculo` `v` on((`r`.`idVehiculo` = `v`.`idVehiculo`))) join `espacio` `e` on((`r`.`idEspacio` = `e`.`idEspacio`))) join `sector` `s` on((`e`.`idSector` = `s`.`idSector`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-05 22:47:24
