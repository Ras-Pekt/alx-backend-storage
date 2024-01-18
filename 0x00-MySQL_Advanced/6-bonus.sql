-- a SQL script that creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
	DECLARE project_id INT;

	-- check if project exists
	SELECT id INTO project_id
	FROM projects
	WHERE name = project_name;

	-- create one if project does not exist 
	IF project_id IS NULL THEN
	BEGIN
		INSERT INTO projects (name)
		VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;

	-- insert into existing or newly created project
	INSERT INTO corrections (user_id, project_id, score)
	VALUES (user_id, project_id, score);
END;$$
DELIMITER ;