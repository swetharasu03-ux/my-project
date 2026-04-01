-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 04, 2026 at 01:15 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `26documentfacedb1`
--

-- --------------------------------------------------------

--
-- Table structure for table `filetb`
--

CREATE TABLE `filetb` (
  `id` bigint(20) NOT NULL auto_increment,
  `OwnerName` varchar(250) NOT NULL,
  `FileInfo` varchar(500) NOT NULL,
  `FileName` varchar(250) NOT NULL,
  `Pukey` varchar(250) NOT NULL,
  `pupkey` varchar(250) NOT NULL,
  `prikey` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `filetb`
--

INSERT INTO `filetb` (`id`, `OwnerName`, `FileInfo`, `FileName`, `Pukey`, `pupkey`, `prikey`) VALUES
(1, 'san567', 'myfill', '715g3.jpg', '043fe853e88a100a2caaed0b3e02d43fe01c58fab27bff1ba562cebb29323155cd9e85949b11da1f081b98735b00295ffdfa89f2f7aac6114c84fa0056b70827f6d6c229b269b5aaaa37b5767c1fb5ecd86d13020afbf497e1be5eb10c6989f27db21f51d2aa2ee3207ef7', '03d2d35cbed6b8115d046778c930d766b0e06c8dc839c600d87ab2f260f0649657', 'bea3488d94d77bc7ee26296b7e9504dbc76c3689e50a06c564c8037254f621b2');

-- --------------------------------------------------------

--
-- Table structure for table `ownertb`
--

CREATE TABLE `ownertb` (
  `id` bigint(20) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `ownertb`
--

INSERT INTO `ownertb` (`id`, `Name`, `Mobile`, `Email`, `Address`, `UserName`, `Password`) VALUES
(1, 'dhanusha', '9486365535', 'dhanushamuthu@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'dhanusha', 'dhanusha'),
(2, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'sangeeth', 'sangeeth'),
(3, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san', 'san'),
(4, 'sangeeth Kumar', '9486365535', 'sangeeth5535@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san567', 'san567');

-- --------------------------------------------------------

--
-- Table structure for table `temptb`
--

CREATE TABLE `temptb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `temptb`
--

INSERT INTO `temptb` (`id`, `UserName`) VALUES
(1, 'san567');
