-- Generado desde database/parksmart_db.sql.
-- Sin credenciales ni clausulas DEFINER.

DELIMITER $$

DROP PROCEDURE IF EXISTS `SP_CancelarReserva`$$
CREATE PROCEDURE `SP_CancelarReserva`(
    IN pIdReserva BIGINT UNSIGNED
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vIdEspacio BIGINT UNSIGNED;
    SELECT idEspacio
    INTO vIdEspacio
    FROM reserva
    WHERE idReserva = pIdReserva
      AND estado IN ('PENDIENTE', 'CONFIRMADA');
    UPDATE reserva
    SET estado = 'CANCELADA'
    WHERE idReserva = pIdReserva
      AND estado IN ('PENDIENTE', 'CONFIRMADA');
    UPDATE espacio
    SET estado = 'DISPONIBLE'
    WHERE idEspacio = vIdEspacio;
END$$

DROP PROCEDURE IF EXISTS `SP_CrearReserva`$$
CREATE PROCEDURE `SP_CrearReserva`(
    IN pIdCliente BIGINT UNSIGNED,
    IN pIdVehiculo BIGINT UNSIGNED,
    IN pIdEspacio BIGINT UNSIGNED,
    IN pFechaInicioReserva DATETIME,
    IN pFechaFinReserva DATETIME
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vEspacioDisponible INT DEFAULT 0;
    DECLARE vVehiculoCliente INT DEFAULT 0;
    DECLARE vReservasCruzadas INT DEFAULT 0;
    DECLARE vCodigoReserva VARCHAR(30);
    SELECT COUNT(*)
    INTO vEspacioDisponible
    FROM espacio
    WHERE idEspacio = pIdEspacio
      AND estado = 'DISPONIBLE';

    IF vEspacioDisponible = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El espacio no se encuentra disponible';
    END IF;
    SELECT COUNT(*)
    INTO vVehiculoCliente
    FROM vehiculo
    WHERE idVehiculo = pIdVehiculo
      AND idCliente = pIdCliente
      AND estado = 'ACTIVO';
    IF vVehiculoCliente = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El vehiculo no pertenece al cliente o no esta activo';
    END IF;
    SELECT COUNT(*)
    INTO vReservasCruzadas
    FROM reserva
    WHERE idEspacio = pIdEspacio
      AND estado IN ('PENDIENTE', 'CONFIRMADA')
      AND pFechaInicioReserva < fechaFinReserva
      AND pFechaFinReserva > fechaInicioReserva;

    IF vReservasCruzadas > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ya existe una reserva activa para ese espacio en ese horario';
    END IF;
    SET vCodigoReserva = CONCAT(
        'RES-',
        DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')
    );
    INSERT INTO reserva (
        idCliente,
        idVehiculo,
        idEspacio,
        codigoReserva,
        fechaInicioReserva,
        fechaFinReserva,
        estado
    )
    VALUES (
        pIdCliente,
        pIdVehiculo,
        pIdEspacio,
        vCodigoReserva,
        pFechaInicioReserva,
        pFechaFinReserva,
        'CONFIRMADA'
    );
    UPDATE espacio
    SET estado = 'RESERVADO'
    WHERE idEspacio = pIdEspacio;
END$$

DROP PROCEDURE IF EXISTS `SP_FinalizarOcupacionGenerarPago`$$
CREATE PROCEDURE `SP_FinalizarOcupacionGenerarPago`(
    IN pIdOcupacion BIGINT UNSIGNED,
    IN pTarifaPorHora DECIMAL(10,2),
    IN pPorcentajeImpuesto DECIMAL(5,2)
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vFechaEntrada DATETIME;
    DECLARE vFechaSalida DATETIME;
    DECLARE vTiempoMinutos INT UNSIGNED;
    DECLARE vSubtotal DECIMAL(10,2);
    DECLARE vImpuesto DECIMAL(10,2);
    DECLARE vTotal DECIMAL(10,2);
    DECLARE vCodigoPago VARCHAR(30);
    DECLARE vIdEspacio BIGINT UNSIGNED;
    SELECT
        fechaEntrada
    INTO
        vFechaEntrada
    FROM ocupacion
    WHERE idOcupacion = pIdOcupacion
      AND estado = 'EN_CURSO';
    SET vFechaSalida = NOW();
    SET vTiempoMinutos = FN_CalcularTiempoOcupacion(
        vFechaEntrada,
        vFechaSalida
    );
    SET vSubtotal = FN_CalcularSubtotalPago(
        vTiempoMinutos,
        pTarifaPorHora
    );
    SET vImpuesto = FN_CalcularImpuesto(
        vSubtotal,
        pPorcentajeImpuesto
    );
    SET vTotal = FN_CalcularTotalPago(
        vSubtotal,
        vImpuesto
    );
    SET vCodigoPago = CONCAT(
        'PAG-',
        pIdOcupacion,
        '-',
        DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')
    );
    UPDATE ocupacion
    SET fechaSalida = vFechaSalida,
        tiempoTotalMinutos = vTiempoMinutos,
        estado = 'FINALIZADA'
    WHERE idOcupacion = pIdOcupacion;
    INSERT INTO pago (
        idOcupacion,
        codigoPago,
        tiempoCobradoMinutos,
        tarifaPorHora,
        montoSubtotal,
        montoImpuesto,
        montoTotal,
        estado,
        fechaLimitePago
    )
    VALUES (
        pIdOcupacion,
        vCodigoPago,
        vTiempoMinutos,
        pTarifaPorHora,
        vSubtotal,
        vImpuesto,
        vTotal,
        'PENDIENTE',
        DATE_ADD(NOW(), INTERVAL 24 HOUR)
    );
    SELECT r.idEspacio
    INTO vIdEspacio
    FROM ocupacion o
    INNER JOIN reserva r
        ON o.idReserva = r.idReserva
    WHERE o.idOcupacion = pIdOcupacion;
    UPDATE espacio
    SET estado = 'DISPONIBLE'
    WHERE idEspacio = vIdEspacio;
END$$

DROP PROCEDURE IF EXISTS `SP_GenerarDeudaPago`$$
CREATE PROCEDURE `SP_GenerarDeudaPago`(
    IN pIdPago BIGINT UNSIGNED
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vPagoVencido TINYINT DEFAULT 0;
    DECLARE vMontoTotal DECIMAL(10,2);
    DECLARE vFechaLimite DATETIME;
    DECLARE vCodigoDeuda VARCHAR(30);

    SET vPagoVencido = FN_VerificarPagoVencido(pIdPago);

    IF vPagoVencido = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El pago no esta vencido o no se encuentra pendiente';
    END IF;

    SELECT montoTotal, fechaLimitePago
    INTO vMontoTotal, vFechaLimite
    FROM pago
    WHERE idPago = pIdPago;

    SET vCodigoDeuda = CONCAT(
        'DEU-',
        pIdPago,
        '-',
        DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')
    );

    INSERT INTO deuda (
        idPago,
        codigoDeuda,
        montoDeuda,
        fechaLimite,
        estado
    )
    VALUES (
        pIdPago,
        vCodigoDeuda,
        vMontoTotal,
        vFechaLimite,
        'VENCIDA'
    );

    UPDATE pago
    SET estado = 'VENCIDO'
    WHERE idPago = pIdPago;
END$$

DROP PROCEDURE IF EXISTS `SP_GenerarQrReserva`$$
CREATE PROCEDURE `SP_GenerarQrReserva`(
    IN pIdReserva BIGINT UNSIGNED
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vCodigoQr VARCHAR(100);
    DECLARE vFechaInicio DATETIME;
    DECLARE vFechaFin DATETIME;

    SELECT
        fechaInicioReserva,
        fechaFinReserva
    INTO
        vFechaInicio,
        vFechaFin
    FROM reserva
    WHERE idReserva = pIdReserva
      AND estado = 'CONFIRMADA';
    SET vCodigoQr = CONCAT(
        'QR-',
        pIdReserva,
        '-',
        DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')
    );
    INSERT INTO qr (
        idReserva,
        codigoQr,
        fechaActivacion,
        fechaExpiracion,
        estado
    )
    VALUES (
        pIdReserva,
        vCodigoQr,
        DATE_SUB(vFechaInicio, INTERVAL 10 MINUTE),
        vFechaFin,
        'ACTIVO'
    );
END$$

DROP PROCEDURE IF EXISTS `SP_IniciarOcupacion`$$
CREATE PROCEDURE `SP_IniciarOcupacion`(
    IN pIdQr BIGINT UNSIGNED
)
    SQL SECURITY INVOKER
BEGIN
    DECLARE vQrValido TINYINT DEFAULT 0;
    DECLARE vIdReserva BIGINT UNSIGNED;
    DECLARE vIdEspacio BIGINT UNSIGNED;
    SET vQrValido = FN_ValidarQrActivo(pIdQr);
    IF vQrValido = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El codigo QR no es valido o esta fuera del rango permitido';
    END IF;
    SELECT
        q.idReserva,
        r.idEspacio
    INTO
        vIdReserva,
        vIdEspacio
    FROM qr q
    INNER JOIN reserva r
        ON q.idReserva = r.idReserva
    WHERE q.idQr = pIdQr;
    INSERT INTO ocupacion (
        idReserva,
        idQr,
        fechaEntrada,
        estado
    )
    VALUES (
        vIdReserva,
        pIdQr,
        NOW(),
        'EN_CURSO'
    );
    UPDATE qr
    SET estado = 'USADO',
        fechaUso = NOW()
    WHERE idQr = pIdQr;
    UPDATE reserva
    SET estado = 'UTILIZADA'
    WHERE idReserva = vIdReserva;
    UPDATE espacio
    SET estado = 'OCUPADO'
    WHERE idEspacio = vIdEspacio;
END$$

DROP PROCEDURE IF EXISTS `SP_RegistrarCliente`$$
CREATE PROCEDURE `SP_RegistrarCliente`(
    IN pIdentificacion VARCHAR(20),
    IN pNombre VARCHAR(50),
    IN pPrimerApellido VARCHAR(50),
    IN pSegundoApellido VARCHAR(50),
    IN pTelefono VARCHAR(20),
    IN pCorreoElectronico VARCHAR(120),
    IN pDireccion VARCHAR(250)
)
    SQL SECURITY INVOKER
BEGIN
    INSERT INTO cliente (
        identificacion,
        nombre,
        primerApellido,
        segundoApellido,
        telefono,
        correoElectronico,
        direccion,
        estado
    )
    VALUES (
        pIdentificacion,
        pNombre,
        pPrimerApellido,
        pSegundoApellido,
        pTelefono,
        pCorreoElectronico,
        pDireccion,
        'ACTIVO'
    );
END$$

DROP PROCEDURE IF EXISTS `SP_RegistrarPago`$$
CREATE PROCEDURE `SP_RegistrarPago`(
    IN pIdPago BIGINT UNSIGNED,
    IN pMetodoPago VARCHAR(20),
    IN pNumeroComprobante VARCHAR(100)
)
    SQL SECURITY INVOKER
BEGIN
    UPDATE pago
    SET metodoPago = pMetodoPago,
        numeroComprobante = pNumeroComprobante,
        estado = 'PAGADO',
        fechaPago = NOW()
    WHERE idPago = pIdPago
      AND estado = 'PENDIENTE';
END$$

DROP PROCEDURE IF EXISTS `SP_RegistrarVehiculo`$$
CREATE PROCEDURE `SP_RegistrarVehiculo`(
    IN pIdCliente BIGINT UNSIGNED,
    IN pPlaca VARCHAR(20),
    IN pMarca VARCHAR(50),
    IN pModelo VARCHAR(50),
    IN pColor VARCHAR(30),
    IN pTipoVehiculo VARCHAR(20)
)
    SQL SECURITY INVOKER
BEGIN
    INSERT INTO vehiculo (
        idCliente,
        placa,
        marca,
        modelo,
        color,
        tipoVehiculo,
        estado
    )
    VALUES (
        pIdCliente,
        pPlaca,
        pMarca,
        pModelo,
        pColor,
        pTipoVehiculo,
        'ACTIVO'
    );
END$$

DELIMITER ;