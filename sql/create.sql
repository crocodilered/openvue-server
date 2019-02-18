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

-- Дамп данных таблицы openvue.folder: ~8 rows (приблизительно)
/*!40000 ALTER TABLE `folder` DISABLE KEYS */;
/*!40000 ALTER TABLE `folder` ENABLE KEYS */;

-- Дамп данных таблицы openvue.formular: ~2 rows (приблизительно)
/*!40000 ALTER TABLE `formular` DISABLE KEYS */;
/*!40000 ALTER TABLE `formular` ENABLE KEYS */;

-- Дамп данных таблицы openvue.user: ~1 rows (приблизительно)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `email`, `password`, `enabled`, `name`, `role`) VALUES
	(1, 'admin@openlist.wiki', '$2b$12$3jiCgvlBI6MmdQe4lozqvOsQVTkCVeeMaGPKvKAQxsaQqHjWjZFv6', '1', 'Admin', '1'),
	(2, 'user@mail.ru', '$2b$12$3jiCgvlBI6MmdQe4lozqvOsQVTkCVeeMaGPKvKAQxsaQqHjWjZFv6', '1', 'User', '2');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
