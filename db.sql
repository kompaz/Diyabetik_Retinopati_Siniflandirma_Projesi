USE bitirmeproje;

DROP TABLE IF EXISTS `doktor`;
CREATE TABLE `doktor` (
  `tc` char(11) NOT NULL,
  `sifre` varchar(20) NOT NULL,
  `ad` varchar(50) NOT NULL,
  `soyad` varchar(50) NOT NULL,
  `uzmanlik_alan` varchar(50) NOT NULL,
  `iletisim_bilgisi` char(11) DEFAULT NULL,
  PRIMARY KEY (`tc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `doktor` VALUES
('12345678901','sifre123','Ahmet','Yılmaz','Göz Doktoru','05331234567'),
('23456789012','sifre234','Elif','Kaya','Göz Doktoru','05337654321'),
('34567890123','sifre345','Mehmet','Öz','Göz Doktoru','05339876543'),
('45678901234','sifre456','Ayşe','Demir','Göz Doktoru','05332109876'),
('56789012345','sifre567','Fatma','Çelik','Göz Doktoru','05333456789');

DROP TABLE IF EXISTS `hasta`;
CREATE TABLE `hasta` (
  `tc` char(11) NOT NULL,
  `ad` varchar(50) NOT NULL,
  `soyad` varchar(50) NOT NULL,
  `dogum_tarihi` date DEFAULT NULL,
  `cinsiyet` varchar(20) DEFAULT NULL,
  `iletisim_bilgisi` char(11) DEFAULT NULL,
  PRIMARY KEY (`tc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `hasta` VALUES
('54321098765','Sezen','Aksu',NULL,'kadın',NULL),
('65432109876','Tarkan','Tevetoglu',NULL,NULL,NULL),
('76543210987','Barış','Manço',NULL,NULL,NULL),
('87654321098','Sibel','Can',NULL,NULL,NULL),
('98765432109','Kemal','Sunal',NULL,NULL,NULL);

DROP TABLE IF EXISTS `kayit`;
CREATE TABLE `kayit` (
  `kayit_id` int NOT NULL AUTO_INCREMENT,
  `doktor_tc` char(11) NOT NULL,
  `hasta_tc` char(11) NOT NULL,
  `tarih` date DEFAULT NULL,
  `hastalik_derecesi` varchar(20) DEFAULT NULL,
  `retina_gorsel` blob,
  PRIMARY KEY (`kayit_id`),
  FOREIGN KEY (`doktor_tc`) REFERENCES `doktor`(`tc`),
  FOREIGN KEY (`hasta_tc`) REFERENCES `hasta`(`tc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

