-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: blood_bank
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blood_requests`
--

DROP TABLE IF EXISTS `blood_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `request_by` varchar(255) NOT NULL,
  `blood_group` varchar(10) NOT NULL,
  `whole_blood_units` decimal(3,1) DEFAULT '0.0',
  `rbc_units` decimal(3,1) DEFAULT '0.0',
  `plasma_units` decimal(3,1) DEFAULT '0.0',
  `platelet_units` decimal(3,1) DEFAULT '0.0',
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `action_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  CONSTRAINT `blood_requests_chk_1` CHECK ((`whole_blood_units` >= 0)),
  CONSTRAINT `blood_requests_chk_2` CHECK ((`rbc_units` >= 0)),
  CONSTRAINT `blood_requests_chk_3` CHECK ((`plasma_units` >= 0)),
  CONSTRAINT `blood_requests_chk_4` CHECK ((`platelet_units` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_requests`
--

LOCK TABLES `blood_requests` WRITE;
/*!40000 ALTER TABLE `blood_requests` DISABLE KEYS */;
INSERT INTO `blood_requests` VALUES (1,'Seline','AB+',1.0,0.0,0.0,0.0,'Approved','2025-04-13 17:13:53','2025-04-13 17:14:00'),(2,'Arav','B+',1.0,0.0,0.0,0.0,'Approved','2025-04-14 05:04:54','2025-04-14 07:53:45'),(3,'Anu','A-',4.0,0.0,0.0,0.0,'Pending','2025-04-14 05:05:25',NULL),(4,'Uri','B-',1.0,0.0,0.0,0.0,'Rejected','2025-04-14 07:52:47',NULL),(5,'Wren','AB+',1.0,0.0,0.0,0.0,'Pending','2025-04-14 07:56:15',NULL),(6,'Riddhi','A+',10.0,0.0,0.0,0.0,'Rejected','2025-04-15 04:05:36',NULL),(7,'Anjana','A-',1.0,0.0,0.0,0.0,'Approved','2025-04-15 04:07:25','2025-04-15 04:07:29');
/*!40000 ALTER TABLE `blood_requests` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_inventory_after_approval` AFTER UPDATE ON `blood_requests` FOR EACH ROW BEGIN          IF NEW.status = 'Approved' AND OLD.status != 'Approved' THEN         UPDATE inventory         SET              whole_blood_units = whole_blood_units - NEW.whole_blood_units,             rbc_units = rbc_units - NEW.rbc_units,             plasma_units = plasma_units - NEW.plasma_units,             platelet_units = platelet_units - NEW.platelet_units         WHERE blood_group = NEW.blood_group;     END IF; END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `donation_details`
--

DROP TABLE IF EXISTS `donation_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation_details` (
  `donation_id` int NOT NULL AUTO_INCREMENT,
  `donor_id` int DEFAULT NULL,
  `blood_group` varchar(10) NOT NULL,
  `whole_blood_units` decimal(3,1) DEFAULT '0.0',
  `rbc_units` decimal(3,1) DEFAULT '0.0',
  `plasma_units` decimal(3,1) DEFAULT '0.0',
  `platelet_units` decimal(3,1) DEFAULT '0.0',
  `donation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`donation_id`),
  KEY `donation_details_ibfk_1` (`donor_id`),
  CONSTRAINT `donation_details_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `donors` (`donor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation_details`
--

LOCK TABLES `donation_details` WRITE;
/*!40000 ALTER TABLE `donation_details` DISABLE KEYS */;
INSERT INTO `donation_details` VALUES (1,1,'A-',1.0,0.0,0.0,0.0,'2025-04-10 12:53:32'),(2,2,'B+',1.0,0.0,0.0,0.0,'2025-04-11 18:27:06'),(3,3,'B+',1.0,0.0,0.0,0.0,'2025-04-13 08:06:18'),(4,4,'AB+',1.0,0.0,0.0,0.0,'2025-04-13 17:13:29'),(7,6,'B-',1.0,0.0,0.0,0.0,'2025-04-14 07:51:13'),(8,7,'A+',1.0,0.0,0.0,0.0,'2025-04-15 04:05:02');
/*!40000 ALTER TABLE `donation_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_inventory_and_donor_after_donation` AFTER INSERT ON `donation_details` FOR EACH ROW BEGIN
    
    UPDATE inventory
    SET
        whole_blood_units = whole_blood_units + NEW.whole_blood_units,
        rbc_units = rbc_units + NEW.rbc_units,
        plasma_units = plasma_units + NEW.plasma_units,
        platelet_units = platelet_units + NEW.platelet_units,
        last_updated = CURRENT_TIMESTAMP
    WHERE blood_group = NEW.blood_group;

    
    UPDATE donors
    SET last_donation = NEW.donation_date
    WHERE donor_id = NEW.donor_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `donors`
--

DROP TABLE IF EXISTS `donors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donors` (
  `donor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `age` int NOT NULL,
  `contact` varchar(10) NOT NULL,
  `blood_group` varchar(10) NOT NULL,
  `last_donation` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`donor_id`),
  UNIQUE KEY `donor_id` (`donor_id`,`name`,`blood_group`),
  KEY `blood_group` (`blood_group`),
  CONSTRAINT `donors_ibfk_1` FOREIGN KEY (`blood_group`) REFERENCES `inventory` (`blood_group`),
  CONSTRAINT `donors_chk_1` CHECK ((`age` >= 18)),
  CONSTRAINT `donors_chk_2` CHECK ((length(`contact`) = 10))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donors`
--

LOCK TABLES `donors` WRITE;
/*!40000 ALTER TABLE `donors` DISABLE KEYS */;
INSERT INTO `donors` VALUES (1,'Aden',19,'4532109876','A-','2025-04-10 12:53:32'),(2,'Riddhi',19,'1029384756','B+','2025-04-11 18:27:06'),(3,'Usha',45,'1093876524','B+','2025-04-13 08:06:18'),(4,'Aston Kutcher',25,'1234509876','AB+','2025-04-13 17:13:29'),(6,'Ann',28,'1093876525','B-','2025-04-14 07:51:13'),(7,'Ariel',45,'4532109876','A+','2025-04-15 04:05:02');
/*!40000 ALTER TABLE `donors` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_donor_donations` BEFORE DELETE ON `donors` FOR EACH ROW BEGIN
    DELETE FROM donation_details WHERE donor_id = OLD.donor_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `blood_group` varchar(10) NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `whole_blood_units` decimal(5,1) DEFAULT '0.0',
  `rbc_units` decimal(5,1) DEFAULT '0.0',
  `plasma_units` decimal(5,1) DEFAULT '0.0',
  `platelet_units` decimal(5,1) DEFAULT '0.0',
  PRIMARY KEY (`blood_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES ('A-','2025-04-15 04:07:29',0.0,0.0,0.0,0.0),('A+','2025-04-15 04:05:02',1.0,0.0,0.0,0.0),('AB-',NULL,0.0,0.0,0.0,0.0),('AB+','2025-04-13 17:14:00',0.0,0.0,0.0,0.0),('B-','2025-04-14 07:51:13',1.0,0.0,0.0,0.0),('B+','2025-04-14 07:53:45',1.0,0.0,0.0,0.0),('O-',NULL,0.0,0.0,0.0,0.0),('O+','2025-04-14 07:20:44',1.0,1.0,0.0,0.0);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `authentication_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('User','Staff','Admin') NOT NULL,
  PRIMARY KEY (`authentication_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('AD001','Pritha','Admin123','Admin'),('EM001','Emily','staff@1','Staff'),('EM002','Sara','1234','Staff');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-16 20:36:23
