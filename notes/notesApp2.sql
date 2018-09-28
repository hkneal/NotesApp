BEGIN;
--
CREATE SCHEMA IF NOT EXISTS `notesApp` DEFAULT CHARACTER SET utf8 ;
USE `notesApp` ;
-- Alter field id on note
--
ALTER TABLE `label` DROP FOREIGN KEY `label_notes_id_ab124b07_fk`;
ALTER TABLE `note` MODIFY `id` integer AUTO_INCREMENT NOT NULL;
ALTER TABLE `label` MODIFY `notes_id` integer NOT NULL;
ALTER TABLE `label` ADD CONSTRAINT `label_notes_id_ab124b07_fk` FOREIGN KEY (`notes_id`) REFERENCES `note` (`id`);
COMMIT;
