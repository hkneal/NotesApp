BEGIN;
--
-- Create model Label
--
CREATE TABLE `label` (`created_at` datetime(6) NOT NULL, `label` varchar(45) NOT NULL PRIMARY KEY);
--
-- Create model Note
--
CREATE TABLE `note` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(45) NULL, `note` varchar(500) NULL, `created_at` datetime(6) NOT NULL, `updated_at` datetime(6) NOT NULL, `notes_list_id` integer NOT NULL);
--
-- Add field labels_list to label
--
ALTER TABLE `label` ADD COLUMN `labels_list_id` integer NOT NULL;
ALTER TABLE `note` ADD CONSTRAINT `note_notes_list_id_2fffa767_fk_auth_user_id` FOREIGN KEY (`notes_list_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `label` ADD CONSTRAINT `label_labels_list_id_2856d3f5_fk_note_id` FOREIGN KEY (`labels_list_id`) REFERENCES `note` (`id`);
COMMIT;
