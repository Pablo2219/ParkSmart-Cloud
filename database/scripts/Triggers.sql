-- Generado desde database/parksmart_db.sql.
-- Sin credenciales ni clausulas DEFINER.

DELIMITER $$

DROP TRIGGER IF EXISTS `TR_Cliente_AI_Bitacora`$$
CREATE TRIGGER `TR_Cliente_AI_Bitacora` AFTER INSERT ON `cliente` FOR EACH ROW BEGIN
    INSERT INTO bitacora (
        idUsuario,
        modulo,
        accion,
        descripcion,
        resultado
    )
    VALUES (
        NULL,
        'Cliente',
        'INSERT',
        CONCAT('Se registro el cliente con identificacion: ', NEW.identificacion),
        'EXITOSO'
    );
END$$

DROP TRIGGER IF EXISTS `TR_Notificacion_BU`$$
CREATE TRIGGER `TR_Notificacion_BU` BEFORE UPDATE ON `notificacion` FOR EACH ROW BEGIN
    IF NEW.estado = 'ENVIADA'
       AND OLD.estado <> 'ENVIADA'
       AND NEW.fechaEnvio IS NULL THEN
        SET NEW.fechaEnvio = NOW();
    END IF;
    IF NEW.estado = 'LEIDA'
       AND OLD.estado <> 'LEIDA'
       AND NEW.fechaLectura IS NULL THEN
        SET NEW.fechaLectura = NOW();
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Ocupacion_AI`$$
CREATE TRIGGER `TR_Ocupacion_AI` AFTER INSERT ON `ocupacion` FOR EACH ROW BEGIN
    DECLARE vIdEspacio BIGINT UNSIGNED;
    UPDATE qr
    SET estado = 'USADO',
        fechaUso = NOW()
    WHERE idQr = NEW.idQr;
    UPDATE reserva
    SET estado = 'UTILIZADA'
    WHERE idReserva = NEW.idReserva;
    SELECT idEspacio
    INTO vIdEspacio
    FROM reserva
    WHERE idReserva = NEW.idReserva;
    UPDATE espacio
    SET estado = 'OCUPADO'
    WHERE idEspacio = vIdEspacio;
END$$

DROP TRIGGER IF EXISTS `TR_Ocupacion_BU`$$
CREATE TRIGGER `TR_Ocupacion_BU` BEFORE UPDATE ON `ocupacion` FOR EACH ROW BEGIN
    IF NEW.fechaSalida IS NOT NULL THEN
        IF NEW.fechaSalida <= NEW.fechaEntrada THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La fecha de salida debe ser posterior a la fecha de entrada';
        END IF;
        SET NEW.tiempoTotalMinutos = FN_CalcularTiempoOcupacion(
            NEW.fechaEntrada,
            NEW.fechaSalida
        );
        SET NEW.estado = 'FINALIZADA';
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Ocupacion_AU`$$
CREATE TRIGGER `TR_Ocupacion_AU` AFTER UPDATE ON `ocupacion` FOR EACH ROW BEGIN
    DECLARE vIdEspacio BIGINT UNSIGNED;
    IF NEW.estado = 'FINALIZADA'
       AND OLD.estado <> 'FINALIZADA' THEN
        SELECT r.idEspacio
        INTO vIdEspacio
        FROM reserva r
        WHERE r.idReserva = NEW.idReserva;
        UPDATE espacio
        SET estado = 'DISPONIBLE'
        WHERE idEspacio = vIdEspacio;
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Pago_BU`$$
CREATE TRIGGER `TR_Pago_BU` BEFORE UPDATE ON `pago` FOR EACH ROW BEGIN
    IF NEW.estado = 'PAGADO'
       AND OLD.estado <> 'PAGADO' THEN
        IF NEW.metodoPago IS NULL THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Debe indicar el metodo de pago';
        END IF;
        IF NEW.fechaPago IS NULL THEN
            SET NEW.fechaPago = NOW();
        END IF;
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Pago_AU_Bitacora`$$
CREATE TRIGGER `TR_Pago_AU_Bitacora` AFTER UPDATE ON `pago` FOR EACH ROW BEGIN
    IF NEW.estado = 'PAGADO'
       AND OLD.estado <> 'PAGADO' THEN
        INSERT INTO bitacora (
            idUsuario,
            modulo,
            accion,
            descripcion,
            resultado
        )
        VALUES (
            NULL,
            'Pago',
            'UPDATE',
            CONCAT('Se registro el pago: ', NEW.codigoPago),
            'EXITOSO'
        );
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Qr_BI`$$
CREATE TRIGGER `TR_Qr_BI` BEFORE INSERT ON `qr` FOR EACH ROW BEGIN
    IF NEW.fechaExpiracion <= NEW.fechaActivacion THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de expiracion del QR debe ser posterior a la fecha de activacion';
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Reserva_AI`$$
CREATE TRIGGER `TR_Reserva_AI` AFTER INSERT ON `reserva` FOR EACH ROW BEGIN
    IF NEW.estado IN ('PENDIENTE', 'CONFIRMADA') THEN
        UPDATE espacio
        SET estado = 'RESERVADO'
        WHERE idEspacio = NEW.idEspacio;
    END IF;
END$$

DROP TRIGGER IF EXISTS `TR_Reserva_AI_Bitacora`$$
CREATE TRIGGER `TR_Reserva_AI_Bitacora` AFTER INSERT ON `reserva` FOR EACH ROW BEGIN
    INSERT INTO bitacora (
        idUsuario,
        modulo,
        accion,
        descripcion,
        resultado
    )
    VALUES (
        NULL,
        'Reserva',
        'INSERT',
        CONCAT('Se creo la reserva: ', NEW.codigoReserva),
        'EXITOSO'
    );
END$$

DROP TRIGGER IF EXISTS `TR_Reserva_AU`$$
CREATE TRIGGER `TR_Reserva_AU` AFTER UPDATE ON `reserva` FOR EACH ROW BEGIN
    IF NEW.estado = 'CANCELADA'
       AND OLD.estado <> 'CANCELADA' THEN
        UPDATE espacio
        SET estado = 'DISPONIBLE'
        WHERE idEspacio = NEW.idEspacio;
    END IF;
END$$

DELIMITER ;