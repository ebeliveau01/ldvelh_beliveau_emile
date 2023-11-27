/*
 * Création des trigger
 */

DELIMITER $$

CREATE TRIGGER personnage_before_insert BEFORE INSERT ON personnage FOR EACH ROW
BEGIN
    IF NEW.bourse > 50 THEN 
        SET NEW.bourse = 50;
    END IF;
END $$

CREATE TRIGGER personnage_after_insert AFTER INSERT ON personnage FOR EACH ROW
BEGIN
    INSERT INTO perso_armes (id_perso,no_arme) VALUES
        (NEW.id,1),
        (NEW.id,2);

    INSERT INTO perso_discipline (id_perso,no_discipline) VALUES
        (NEW.id,1),
        (NEW.id,2),
        (NEW.id,3),
        (NEW.id,4),
        (NEW.id,5),
        (NEW.id,6);
END $$

DELIMITER ;