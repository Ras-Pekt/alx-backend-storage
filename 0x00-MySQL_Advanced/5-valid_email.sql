-- a SQL script that creates a trigger that resets the attribute valid_email only when the email has been changed
DELIMITER $$
CREATE TRIGGER reset_valid_email_attribute
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	IF NEW.email <> OLD.email
		SET valid_email = 1 - NEW.valid_email;
	END IF;
END;$$
DELIMITER ;
