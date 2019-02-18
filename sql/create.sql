-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.3.9-MariaDB - mariadb.org binary distribution
-- Операционная система:         Win64
-- HeidiSQL Версия:              10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Дамп структуры для таблица openvue.folder
CREATE TABLE IF NOT EXISTS `folder` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL COMMENT 'Название папки',
  `creator_id` int(11) unsigned NOT NULL COMMENT 'Создатель',
  `performer_id` int(11) unsigned DEFAULT NULL COMMENT 'Исполнитель',
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` smallint(6) NOT NULL DEFAULT 0 COMMENT '0, 1, 2, 3 - в ожидании, в работе, на проверке, проверено',
  PRIMARY KEY (`id`),
  UNIQUE KEY `folder` (`title`),
  KEY `uploaded_by` (`creator_id`),
  KEY `uploaded_at` (`updated`),
  KEY `FK_queue_performer` (`performer_id`),
  CONSTRAINT `FK_queue_creator` FOREIGN KEY (`creator_id`) REFERENCES `user` (`id`),
  CONSTRAINT `FK_queue_performer` FOREIGN KEY (`performer_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы openvue.folder: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `folder` DISABLE KEYS */;
/*!40000 ALTER TABLE `folder` ENABLE KEYS */;

-- Дамп структуры для таблица openvue.formular
CREATE TABLE IF NOT EXISTS `formular` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `folder_id` int(11) unsigned NOT NULL,
  `title` varchar(200) NOT NULL DEFAULT '',
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `FK_formular_folder` (`folder_id`),
  CONSTRAINT `FK_transcript_queue` FOREIGN KEY (`folder_id`) REFERENCES `folder` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы openvue.formular: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `formular` DISABLE KEYS */;
/*!40000 ALTER TABLE `formular` ENABLE KEYS */;

-- Дамп структуры для таблица openvue.user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(250) NOT NULL,
  `password` varchar(60) NOT NULL,
  `enabled` enum('0','1') NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL,
  `role` enum('1','2') NOT NULL DEFAULT '2' COMMENT '1 - supervisor, 2 - user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='Directory of users who has access to application.';

-- Дамп данных таблицы openvue.user: ~2 rows (приблизительно)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `email`, `password`, `enabled`, `name`, `role`) VALUES
	(1, 'admin@openlist.wiki', '$2b$12$3jiCgvlBI6MmdQe4lozqvOsQVTkCVeeMaGPKvKAQxsaQqHjWjZFv6', '1', 'Admin', '1'),
	(2, 'user@mail.ru', '$2b$12$3jiCgvlBI6MmdQe4lozqvOsQVTkCVeeMaGPKvKAQxsaQqHjWjZFv6', '1', 'User', '2');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
