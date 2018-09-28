BEGIN;
--
-- Alter field created_at on label
--
ALTER TABLE `label` ALTER COLUMN `created_at` SET DEFAULT '2018-09-26 07:52:13.108929';
ALTER TABLE `label` MODIFY `created_at` datetime(6) NOT NULL;
ALTER TABLE `label` ALTER COLUMN `created_at` DROP DEFAULT;
--
-- Alter field created_at on note
--
ALTER TABLE `note` ALTER COLUMN `created_at` SET DEFAULT '2018-09-26 07:52:13.113691';
ALTER TABLE `note` MODIFY `created_at` datetime(6) NOT NULL;
ALTER TABLE `note` ALTER COLUMN `created_at` DROP DEFAULT;
--
-- Alter field updated_at on note
--
ALTER TABLE `note` ALTER COLUMN `updated_at` SET DEFAULT '2018-09-26 07:52:13.118358';
ALTER TABLE `note` MODIFY `updated_at` datetime(6) NOT NULL;
ALTER TABLE `note` ALTER COLUMN `updated_at` DROP DEFAULT;
COMMIT;
