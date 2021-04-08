-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: fastapi_blog
-- ------------------------------------------------------
-- Server version	5.7.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `desc` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `user_id` varchar(40) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `article_category_id` (`category_id`),
  KEY `article_user_id` (`user_id`),
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `article_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES (1,'xxx','xxxxx','xxxxxxxxxxxxx',2,'0e88bf356ee74f1385138d0cb4979953','2021-04-02 18:10:56','2021-04-02 18:10:58',1),(2,'测试的第一篇博客文章','这个是测试的第一篇文字的描述，主要用于测试使用','本篇文章主要用于测试，这个是测试的内容',1,'0e88bf356ee74f1385138d0cb4979953','2020-12-15 15:20:22','2020-12-15 15:20:22',0),(3,'测试的第二篇博客文章','这个是测试的第二篇文字的描述，主要用于测试使用二','本篇文章主要用于测试，这个是测试的内容',1,'0e88bf356ee74f1385138d0cb4979953','2021-04-02 14:08:39','2021-04-02 14:08:39',0),(4,'Linux相关的测试文章标题','这个是linux分类下的文章描述','本文章主要讲解linux的内容',2,'0e88bf356ee74f1385138d0cb4979953','2021-04-01 14:15:47','2021-04-01 14:15:51',0);
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article_tag`
--

DROP TABLE IF EXISTS `article_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articletag_article_id` (`article_id`),
  KEY `articletag_tag_id` (`tag_id`),
  CONSTRAINT `article_tag_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`),
  CONSTRAINT `article_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_tag`
--

LOCK TABLES `article_tag` WRITE;
/*!40000 ALTER TABLE `article_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article_up`
--

DROP TABLE IF EXISTS `article_up`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_up` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(40) NOT NULL,
  `article_id` int(11) NOT NULL,
  `is_up` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articleupdown_user_id` (`user_id`),
  KEY `articleupdown_article_id` (`article_id`),
  CONSTRAINT `article_up_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`uuid`),
  CONSTRAINT `article_up_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_up`
--

LOCK TABLES `article_up` WRITE;
/*!40000 ALTER TABLE `article_up` DISABLE KEYS */;
/*!40000 ALTER TABLE `article_up` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_site`
--

DROP TABLE IF EXISTS `blog_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `site_name` varchar(64) NOT NULL,
  `theme` varchar(32) NOT NULL,
  `user_id` varchar(40) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blogsite_user_id` (`user_id`),
  CONSTRAINT `blog_site_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_site`
--

LOCK TABLES `blog_site` WRITE;
/*!40000 ALTER TABLE `blog_site` DISABLE KEYS */;
INSERT INTO `blog_site` VALUES (1,'人生苦短--测试数据','hsz的博客站点--测试数据','本博客站点主要记录的是Python编程相关--测试数据','0e88bf356ee74f1385138d0cb4979953','2020-12-15 15:17:43','2020-12-15 15:17:43');
/*!40000 ALTER TABLE `blog_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `description` varchar(128) NOT NULL,
  `blog_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_blog_id` (`blog_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`blog_id`) REFERENCES `blog_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'python','python学习的分类',1,'2020-12-15 15:20:07','2020-12-15 15:20:07'),(2,'Linux','Linux 相关的分类',1,'2021-04-01 14:14:06','2021-04-01 14:14:13');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `user_id` varchar(40) NOT NULL,
  `content` varchar(255) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_article_id` (`article_id`),
  KEY `comment_user_id` (`user_id`),
  KEY `comment_parent_id` (`parent_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`uuid`),
  CONSTRAINT `comment_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `comment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,2,'0e88bf356ee74f1385138d0cb4979953','文章写的非常好，666！','2020-12-15 16:06:36','2020-12-15 16:06:36',NULL),(2,2,'0e88bf356ee74f1385138d0cb4979953','文章写的非常好，666修改的！','2020-12-15 16:06:44','2020-12-15 16:42:35',NULL),(4,2,'b3b612341eb94f23983fffa7c9b0e970','文章写的非常好，admin修改！','2020-12-15 18:02:47','2020-12-15 18:03:47',NULL);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migratehistory`
--

DROP TABLE IF EXISTS `migratehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migratehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `migrated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migratehistory`
--

LOCK TABLES `migratehistory` WRITE;
/*!40000 ALTER TABLE `migratehistory` DISABLE KEYS */;
INSERT INTO `migratehistory` VALUES (1,'0001_migration_202012101758','2020-12-10 09:58:55'),(2,'0002_migration_202104061401','2021-04-06 06:01:48');
/*!40000 ALTER TABLE `migratehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `blog_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tag_blog_id` (`blog_id`),
  CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`blog_id`) REFERENCES `blog_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uuid` varchar(40) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `created` datetime NOT NULL,
  `email` varchar(128) DEFAULT NULL,
  `user_type` int(11) NOT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `user_username` (`username`),
  UNIQUE KEY `user_mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('0e88bf356ee74f1385138d0cb4979953','testuser01','$2b$12$9Ok1u..HiW4PqcBWVbIMbugEKpKGppSUaPDzkD37msDR7J3pizdhK','2020-12-15 15:09:55','testuser01@example.com',0,'18666666666','2020-12-15 15:09:55'),('386a81a506404641bd7e697c03d01398','iajwyfuqmhqqxcxowoyqmjpzskjghonv','$2b$12$D480300NOtXIPuXRx072EeVB7He7u7PtjsGx2qCy6kFiGSE/aM6MK','2021-03-18 09:56:01','kcwjycuouznmegenmqegvdxhdvyjkazd@nsmyegrbhjfrbkqymaoyuxvgniqcpxuz.com',1,NULL,'2021-03-18 09:56:02'),('49a2a6b9e1544d5dbd1f08a33a25dde7','bkbqupshtxwfgqfhgcufrwisqthkfmqm','$2b$12$DMgkjNZjpeDE0QWVvFgOSuN1JmqF02H2uBEh1E4H6So6rzNA799wW','2021-03-18 10:37:59','sureznagmamdojgzajckornourtjncjf@ilbowrxlwedrfyektgyycocuyodzqsdc.com',1,NULL,'2021-03-18 10:37:59'),('95a009c709e14a5281a0cd8dae32d8dc','qpojezfgwupksmpxlzugokpsbglopuel','$2b$12$PuQ5vbH8yCNrpx/k4BwYFOe8oHiajSO31//X7JBH7akMcEymc0k96','2021-03-18 10:34:36','dsivaidhyabzkdeklgfuyeoqigvnymby@uaqlsdzkqgsznejgnhefzwvlooxsfube.com',1,NULL,'2021-03-18 10:34:36'),('a5255515cef74a349ed5186de789ae63','yqscohgiriqfajuztgsducsicgqprnpc','$2b$12$F.T4x7qqW3JPk/JR.5sTm..sq0GPmR/e6Vb7JfsGNrWSO0DorXMAi','2021-03-18 09:55:52','wpqipberzjihbrzjysvpzkazbcxoyspb@maeywiqalawsfltqteykrvzqeswcryga.com',1,NULL,'2021-03-18 09:55:52'),('b3b612341eb94f23983fffa7c9b0e970','testadmin','$2b$12$bEO8oOV2P5Oracfml8qAwOz467NsiapcPK0ACjmKkQfZPe9ukiW6K','2020-12-15 17:16:40','testadmin@example.com',0,'18066666666','2020-12-15 17:16:41'),('b5af4f17bb1e4dbb8a4dd7a60252aaf1','nzzolylktvzgjfmculylzjkgjyqejddv','$2b$12$UJFY51LIMojryaR6/SMZ3uXbPIzA/J6JIBJbG2ZskPbvEoqqDZrzK','2021-03-17 17:46:05','jrcrpxtztlagjsyiolynrapawlbjhgho@dkkingskveafamjqymitdinfmiluriod.com',1,NULL,'2021-03-17 17:46:05'),('ba75708749b444b1912d0fd749c8a7ea','tzbbzwzbcpoijdhuphsgyqfsudeapacv','$2b$12$omI2GYUrgG4FUG8lWVY4Bey1zSk21.LiupBo3IOnnOdkOg2T120O2','2021-03-18 10:16:12','fqfgsfpyztotjxmgfmuyinjhuroesdeo@qqugvaeipjynfxlteycxzvblciqudgyq.com',1,NULL,'2021-03-18 10:16:13'),('d39633053f2d48a2b1ab048a9d04e793','fiytjjajhgxvohggabnqazjhmdjvrpuq','$2b$12$DuMZWDsZr7xCICDTdf3sSebfUk9APeqmnR9.CvbY9/n4mwzbnugO.','2021-03-18 10:38:19','ntntrdyuhujgowewyfmdebqjyegzsasq@lllymzdvujyzdfwmfdaovucitblbxffz.com',1,NULL,'2021-03-18 10:38:19'),('d7177ad0290241f186c1179c63a4af3a','bmbwwfmiehzgcvuhgtuvjwvhegxbaafq','$2b$12$dg0hi2tRo7Mpc9c1F1MIluVVGlIO0MP822NT1es2vOiEM7uS2aXmi','2021-03-18 09:56:14','ytrkrkmpgeibuiajidjttzidwxikahuv@pkodochzxkivlkgzlfljhjcelaldkeoy.com',1,NULL,'2021-03-18 09:56:14'),('e7bcc23ab24d41baacd3ee7483070529','nkoaffsjxhvlamtzhduoejcdxnovteys','$2b$12$dFfTB2ZEFnJwA81fYXEuHeRWH8vBw1D4/B7aTbxiipJtz3EuvXxAq','2021-03-18 10:35:03','jqkrdpwpoebdrfuclcflaavasqnwawmy@okschebketsdjwdrggrxlwbxybdzctkz.com',1,NULL,'2021-03-18 10:35:03'),('f83e5830c79a44d09605e2ca8ab64603','gwuvuzdsxoskjyqosmbpodtsbbljcita','$2b$12$GfVNf.jtuoz42DK1lFZdN.pZhqC7UqgUWMYpaVLZwrgaRTfdmbb/6','2021-03-18 10:35:22','psxqelvlehldeqynxsbnldqdutkjswme@bvebnckcxiitklfftjnpagqfdfledcsd.com',1,NULL,'2021-03-18 10:35:22');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-06 14:15:56
