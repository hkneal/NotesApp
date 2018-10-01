BEGIN;
--
-- Create Table

CREATE SCHEMA IF NOT EXISTS `notesApp` DEFAULT CHARACTER SET utf8 ;
USE `notesApp` ;

-- Create model Label
--
CREATE TABLE `label` (`created_at` datetime(6) NOT NULL, `label` varchar(45) NOT NULL PRIMARY KEY);
--
-- Create model Note
--
CREATE TABLE `note` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(45) NULL, `note` varchar(500) NULL, `created_at` datetime(6) NOT NULL, `updated_at` datetime(6) NOT NULL, `notes_id` integer NOT NULL);
--
-- Add field labels to label
--
ALTER TABLE `label` ADD COLUMN `labels_id` integer NOT NULL;
ALTER TABLE `note` ADD CONSTRAINT `note_notes_id_50fc9cc4_fk_auth_user_id` FOREIGN KEY (`notes_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `label` ADD CONSTRAINT `label_labels_id_09bc1372_fk_note_id` FOREIGN KEY (`labels_id`) REFERENCES `note` (`id`);
COMMIT;
