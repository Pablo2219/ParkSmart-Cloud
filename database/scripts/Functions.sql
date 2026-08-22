-- Generado desde database/parksmart_db.sql.
-- Sin credenciales ni clausulas DEFINER.

DELIMITER $$

DROP FUNCTION IF EXISTS `FN_CalcularHorasCobro`$$
CREATE FUNCTION `FN_CalcularHorasCobro`(
    pTiempoMinutos INT UNSIGNED
) RETURNS int unsigned
    DETERMINISTIC
    SQL SECURITY INVOKER
BEGIN
    DECLARE vHoras INT UNSIGNED;

    IF pTiempoMinutos IS NULL OR pTiempoMinutos = 0 THEN
        SET vHoras = 0;
    ELSE
        SET vHoras = CEIL(pTiempoMinutos / 60);
    END IF;

    RETURN vHoras;
END$$

DROP FUNCTION IF EXISTS `FN_CalcularImpuesto`$$
CREATE FUNCTION `FN_CalcularImpuesto`(
    pMontoSubtotal DECIMAL(10,2),
    pPorcentajeImpuesto DECIMAL(5,2)
) RETURNS decimal(10,2)
    DETERMINISTIC
    SQL SECURITY INVOKER
BEGIN
    DECLARE vImpuesto DECIMAL(10,2);
    SET vImpuesto = pMontoSubtotal * (pPorcentajeImpuesto / 100);

    RETURN vImpuesto;
END$$

DROP FUNCTION IF EXISTS `FN_CalcularSubtotalPago`$$
CREATE FUNCTION `FN_CalcularSubtotalPago`(
    pTiempoMinutos INT UNSIGNED,
    pTarifaPorHora DECIMAL(10,2)
) RETURNS decimal(10,2)
    DETERMINISTIC
    SQL SECURITY INVOKER
BEGIN
    DECLARE vHoras INT UNSIGNED;
    DECLARE vSubtotal DECIMAL(10,2);

    SET vHoras = FN_CalcularHorasCobro(pTiempoMinutos);
    SET vSubtotal = vHoras * pTarifaPorHora;

    RETURN vSubtotal;
END$$

DROP FUNCTION IF EXISTS `FN_CalcularTiempoOcupacion`$$
CREATE FUNCTION `FN_CalcularTiempoOcupacion`(
    pFechaEntrada DATETIME,
    pFechaSalida DATETIME
) RETURNS int unsigned
    DETERMINISTIC
    SQL SECURITY INVOKER
BEGIN
    DECLARE vTiempoMinutos INT UNSIGNED;
    SET vTiempoMinutos = TIMESTAMPDIFF(
        MINUTE,
        pFechaEntrada,
        IFNULL(pFechaSalida, NOW())
    );

    RETURN vTiempoMinutos;
END$$

DROP FUNCTION IF EXISTS `FN_CalcularTotalPago`$$
CREATE FUNCTION `FN_CalcularTotalPago`(
    pMontoSubtotal DECIMAL(10,2),
    pMontoImpuesto DECIMAL(10,2)
) RETURNS decimal(10,2)
    DETERMINISTIC
    SQL SECURITY INVOKER
BEGIN
    DECLARE vTotal DECIMAL(10,2);

    SET vTotal = pMontoSubtotal + pMontoImpuesto;

    RETURN vTotal;
END$$

DROP FUNCTION IF EXISTS `FN_ValidarQrActivo`$$
CREATE FUNCTION `FN_ValidarQrActivo`(
    pIdQr BIGINT UNSIGNED
) RETURNS tinyint
    READS SQL DATA
    SQL SECURITY INVOKER
BEGIN
    DECLARE vExiste INT DEFAULT 0;
    SELECT COUNT(*)
    INTO vExiste
    FROM qr
    WHERE idQr = pIdQr
      AND estado = 'ACTIVO'
      AND NOW() BETWEEN fechaActivacion AND fechaExpiracion;
    IF vExiste > 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END$$

DROP FUNCTION IF EXISTS `FN_VerificarPagoVencido`$$
CREATE FUNCTION `FN_VerificarPagoVencido`(
    pIdPago BIGINT UNSIGNED
) RETURNS tinyint
    READS SQL DATA
    SQL SECURITY INVOKER
BEGIN
    DECLARE vExiste INT DEFAULT 0;
    SELECT COUNT(*)
    INTO vExiste
    FROM pago
    WHERE idPago = pIdPago
      AND estado = 'PENDIENTE'
      AND NOW() > fechaLimitePago;
    IF vExiste > 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END$$

DELIMITER ;