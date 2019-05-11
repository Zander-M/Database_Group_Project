-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2019-05-11 04:58:54
-- 服务器版本： 10.1.34-MariaDB
-- PHP Version: 7.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ams`
--
CREATE DATABASE IF NOT EXISTS `ams_test` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ams_test`;

-- --------------------------------------------------------

--
-- 表的结构 `airline`
--

CREATE TABLE `airline` (
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `airplane`
--

CREATE TABLE `airplane` (
  `airplane_id` int(10) UNSIGNED NOT NULL,
  `airline` varchar(20) NOT NULL,
  `seat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `airport`
--

CREATE TABLE `airport` (
  `name` char(3) NOT NULL,
  `city` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(30) DEFAULT NULL,
  `pwd` varchar(94) DEFAULT NULL,
  `BAID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `customer`
--

CREATE TABLE `customer` (
  `email` varchar(30) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `pwd` varchar(94) DEFAULT NULL,
  `building_number` varchar(20) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(14) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `passport_expiration_date` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `customer_phone`
--

CREATE TABLE `customer_phone` (
  `phone` decimal(15,0) NOT NULL,
  `email` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `flight`
--

CREATE TABLE `flight` (
  `flight_id` int(10) UNSIGNED NOT NULL,
  `airline` varchar(20) NOT NULL,
  `airplane_id` int(10) UNSIGNED DEFAULT NULL,
  `base_price` int(11) DEFAULT NULL,
  `flight_status` int(11) DEFAULT NULL,
  `dept_time` datetime DEFAULT NULL,
  `arrv_time` datetime DEFAULT NULL,
  `dept_airport` char(3) DEFAULT NULL,
  `arrv_airport` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `staff`
--

CREATE TABLE `staff` (
  `username` varchar(10) NOT NULL,
  `pwd` varchar(94) DEFAULT NULL,
  `first_name` varchar(10) DEFAULT NULL,
  `last_name` varchar(10) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `airline` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `staff_phone`
--

CREATE TABLE `staff_phone` (
  `phone_number` decimal(15,0) NOT NULL,
  `username` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` int(10) UNSIGNED NOT NULL,
  `flight_id` int(10) UNSIGNED DEFAULT NULL,
  `airline` varchar(20) DEFAULT NULL,
  `customer_email` varchar(30) DEFAULT NULL,
  `BAID` varchar(8) DEFAULT NULL,
  `sold_price` int(11) DEFAULT NULL,
  `payment_method` int(11) DEFAULT NULL,
  `card_number` decimal(20,0) DEFAULT NULL,
  `name_on_card` varchar(20) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `purchase_date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline`,`airplane_id`),
  ADD KEY `airplane_id` (`airplane_id`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`BAID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `customer_phone`
--
ALTER TABLE `customer_phone`
  ADD PRIMARY KEY (`phone`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline`,`flight_id`),
  ADD KEY `flight_id` (`flight_id`),
  ADD KEY `airline` (`airline`,`airplane_id`),
  ADD KEY `dept_airport` (`dept_airport`),
  ADD KEY `arrv_airport` (`arrv_airport`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline` (`airline`);

--
-- Indexes for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD PRIMARY KEY (`phone_number`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `airline` (`airline`,`flight_id`),
  ADD KEY `customer_email` (`customer_email`),
  ADD KEY `FK_BAID` (`BAID`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `airplane`
--
ALTER TABLE `airplane`
  MODIFY `airplane_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `flight`
--
ALTER TABLE `flight`
  MODIFY `flight_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `ticket`
--
ALTER TABLE `ticket`
  MODIFY `ticket_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 限制导出的表
--

--
-- 限制表 `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`) ON DELETE CASCADE;

--
-- 限制表 `customer_phone`
--
ALTER TABLE `customer_phone`
  ADD CONSTRAINT `customer_phone_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE;

--
-- 限制表 `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline`,`airplane_id`) REFERENCES `airplane` (`airline`, `airplane_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`dept_airport`) REFERENCES `airport` (`name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrv_airport`) REFERENCES `airport` (`name`);

--
-- 限制表 `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`) ON DELETE CASCADE;

--
-- 限制表 `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD CONSTRAINT `staff_phone_ibfk_1` FOREIGN KEY (`username`) REFERENCES `staff` (`username`) ON DELETE CASCADE;

--
-- 限制表 `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `FK_BAID` FOREIGN KEY (`BAID`) REFERENCES `booking_agent` (`BAID`),
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline`,`flight_id`) REFERENCES `flight` (`airline`, `flight_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`customer_email`) REFERENCES `customer` (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
