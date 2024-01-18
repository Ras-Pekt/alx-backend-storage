--  a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser()
BEGIN
    UPDATE users
    SET average_score = (
        SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections
        JOIN projects
        ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id
    );
END;$$
DELIMITER ;
