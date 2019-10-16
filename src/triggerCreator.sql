DELIMITER $$
CREATE TRIGGER Desativa_post 
	AFTER UPDATE
	ON red_soc_passaros.usuario
	FOR EACH ROW BEGIN
		IF NEW.ativo = 0 THEN
			UPDATE red_soc_passaros.post SET post.ativo=0
            WHERE id_usuario=new.id_usuario;
		END IF;
	END$$
DELIMITER ;