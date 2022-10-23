DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_code` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_price` float NOT NULL,
  `in_stock` int(11) NOT NULL,
  `sold` int(11) NOT NULL,
  `ordered` date NOT NULL,
  `last_purchase` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'25032002','Apple',2.25,13789,132,'2022-09-02','2022-09-01'),(2,'25032003','Banana',3.27,1389,231,'2022-09-02','2022-09-01'),(3,'25032004','Milk',0.99,23789,3112,'2022-09-02','2022-09-01'),(4,'25032005','Honey',2.25,789,12,'2022-09-02','2022-09-01'),(5,'25032006','Ice Cream',5.25,1789,32,'2022-09-02','2022-09-01');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Precious','Akande','pakande','akandep','employee','2022-09-05'),(2,'Brooke','Johnson','bjohnson','johnsonb','manager','2022-09-05');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `member_code` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1,30301,'John','Smith','johnsmith@gmail.com','0489 333 111','2022-09-29');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sale_code`varchar(255) NOT NULL,
  `member_code` varchar(255) NOT NULL,
  `product_code` varchar(255) NOT NULL,
  `quantity` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

INSERT INTO `sales` VALUES (16,4,30301,25032002,12,'2022-10-14'),(17,4,30301,25032003,5,'2022-10-14'),(18,4,30301,25032004,8,'2022-10-14');
INSERT INTO `sales` VALUES (19,5,30301,25032002,2,'2022-10-15'),(20,5,30301,25032003,8,'2022-10-15'),(21,5,30301,25032004,7,'2022-10-15');
INSERT INTO `sales` VALUES (22,6,30301,25032002,7,'2022-10-16'),(23,6,30301,25032003,4,'2022-10-16'),(24,6,30301,25032004,6,'2022-10-16');
INSERT INTO `sales` VALUES (25,7,30301,25032002,9,'2022-10-17'),(26,7,30301,25032003,3,'2022-10-17'),(27,7,30301,25032004,9,'2022-10-17');
INSERT INTO `sales` VALUES (28,8,30301,25032002,4,'2022-10-18'),(29,8,30301,25032003,2,'2022-10-18'),(30,8,30301,25032004,9,'2022-10-18');
INSERT INTO `sales` VALUES (31,9,30301,25032002,5,'2022-10-19'),(32,9,30301,25032003,2,'2022-10-19'),(33,9,30301,25032004,8,'2022-10-19');
INSERT INTO `sales` VALUES (34,10,30301,25032002,5,'2022-10-20'),(35,10,30301,25032003,10,'2022-10-20'),(36,10,30301,25032004,8,'2022-10-20');
INSERT INTO `sales` VALUES (37,11,30301,25032002,8,'2022-10-21'),(38,11,30301,25032003,14,'2022-10-21'),(39,11,30301,25032004,6,'2022-10-21');
INSERT INTO `sales` VALUES (40,12,30301,25032002,1,'2022-10-22'),(41,12,30301,25032003,15,'2022-10-22'),(42,12,30301,25032004,7,'2022-10-22');
INSERT INTO `sales` VALUES (43,13,30301,25032002,7,'2022-10-23'),(44,13,30301,25032003,19,'2022-10-23'),(45,13,30301,25032004,8,'2022-10-23');
INSERT INTO `sales` VALUES (46,14,30301,25032002,9,'2022-10-24'),(47,14,30301,25032003,19,'2022-10-24'),(48,14,30301,25032004,7,'2022-10-24');
INSERT INTO `sales` VALUES (49,15,30301,25032002,20,'2022-10-25'),(50,15,30301,25032003,20,'2022-10-25'),(51,15,30301,25032004,7,'2022-10-25');
INSERT INTO `sales` VALUES (52,16,30301,25032002,14,'2022-10-26'),(53,16,30301,25032003,20,'2022-10-26'),(54,16,30301,25032004,8,'2022-10-26');
INSERT INTO `sales` VALUES (55,17,30301,25032002,17,'2022-10-27'),(56,17,30301,25032003,5,'2022-10-27'),(57,17,30301,25032004,6,'2022-10-27');
INSERT INTO `sales` VALUES (58,18,30301,25032002,19,'2022-10-28'),(59,18,30301,25032003,7,'2022-10-28'),(60,18,30301,25032004,6,'2022-10-28');
INSERT INTO `sales` VALUES (61,19,30301,25032002,19,'2022-10-29'),(62,19,30301,25032003,9,'2022-10-29'),(63,19,30301,25032004,8,'2022-10-29');
INSERT INTO `sales` VALUES (64,20,30301,25032002,19,'2022-10-30'),(65,20,30301,25032003,8,'2022-10-30'),(66,20,30301,25032004,2,'2022-10-30');
INSERT INTO `sales` VALUES (67,21,30301,25032002,4,'2022-10-31'),(68,21,30301,25032003,1,'2022-10-31'),(69,21,30301,25032004,8,'2022-10-31');
INSERT INTO `sales` VALUES (70,22,30301,25032002,12,'2022-11-01'),(71,22,30301,25032003,1,'2022-11-01'),(72,22,30301,25032004,8,'2022-11-01');
INSERT INTO `sales` VALUES (73,23,30301,25032002,8,'2022-11-02'),(74,23,30301,25032003,8,'2022-11-02'),(75,23,30301,25032004,8,'2022-11-02');
INSERT INTO `sales` VALUES (76,24,30301,25032002,8,'2022-11-03'),(77,24,30301,25032003,7,'2022-11-03'),(78,24,30301,25032004,7,'2022-11-03');
INSERT INTO `sales` VALUES (79,25,30301,25032002,6,'2022-11-04'),(80,25,30301,25032003,13,'2022-11-04'),(81,25,30301,25032004,9,'2022-11-04');
INSERT INTO `sales` VALUES (82,26,30301,25032002,5,'2022-11-05'),(83,26,30301,25032003,17,'2022-11-05'),(84,26,30301,25032004,9,'2022-11-05');
INSERT INTO `sales` VALUES (85,27,30301,25032002,1,'2022-11-06'),(86,27,30301,25032003,13,'2022-11-06'),(87,27,30301,25032004,6,'2022-11-06');
INSERT INTO `sales` VALUES (88,28,30301,25032002,18,'2022-11-07'),(89,28,30301,25032003,6,'2022-11-07'),(90,28,30301,25032004,7,'2022-11-07');
INSERT INTO `sales` VALUES (91,29,30301,25032002,17,'2022-11-08'),(92,29,30301,25032003,5,'2022-11-08'),(93,29,30301,25032004,8,'2022-11-08');
INSERT INTO `sales` VALUES (94,30,30301,25032002,5,'2022-11-09'),(95,30,30301,25032003,7,'2022-11-09'),(96,30,30301,25032004,16,'2022-11-09');
INSERT INTO `sales` VALUES (97,31,30301,25032002,4,'2022-11-10'),(98,31,30301,25032003,14,'2022-11-10'),(99,31,30301,25032004,8,'2022-11-10');
INSERT INTO `sales` VALUES (100,32,30301,25032002,1,'2022-11-11'),(101,32,30301,25032003,18,'2022-11-11'),(102,32,30301,25032004,3,'2022-11-11');
INSERT INTO `sales` VALUES (103,33,30301,25032002,1,'2022-11-12'),(104,33,30301,25032003,9,'2022-11-12'),(105,33,30301,25032004,8,'2022-11-12');
INSERT INTO `sales` VALUES (106,34,30301,25032002,8,'2022-11-13'),(107,34,30301,25032003,8,'2022-11-13'),(108,34,30301,25032004,8,'2022-11-13');
INSERT INTO `sales` VALUES (109,35,30301,25032002,15,'2022-11-14'),(110,35,30301,25032003,5,'2022-11-14'),(111,35,30301,25032004,7,'2022-11-14');



