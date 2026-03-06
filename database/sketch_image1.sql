-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 12, 2025 at 09:39 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sketch_image1`
--

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

CREATE TABLE `result` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `test_logo` varchar(30) NOT NULL,
  `result` varchar(20) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `result`
--


-- --------------------------------------------------------

--
-- Table structure for table `sk_admin`
--

CREATE TABLE `sk_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sk_admin`
--

INSERT INTO `sk_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `sk_data`
--

CREATE TABLE `sk_data` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `image_file` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sk_data`
--

INSERT INTO `sk_data` (`id`, `pid`, `image_file`) VALUES
(1, 1, 'm1PXL_20240130_033934688.jpg'),
(2, 1, 'm2PXL_20240130_033945713.MP.jpg'),
(3, 1, 'm3PXL_20240130_033952974.jpg'),
(4, 1, 'm4PXL_20240130_034025583.jpg'),
(5, 1, 'm5PXL_20240130_034046716.jpg'),
(6, 1, 'm6PXL_20240130_034111773.jpg'),
(7, 1, 'm7PXL_20240130_034157779.MP.jpg'),
(8, 1, 'm8PXL_20240130_034358279.jpg'),
(9, 1, 'm9PXL_20240130_034421261.MP.jpg'),
(10, 1, 'm10PXL_20240130_034637524.jpg'),
(11, 1, 'm11PXL_20240130_034658277.MP.jpg'),
(12, 1, 'm12PXL_20240130_034709371.jpg'),
(13, 1, 'm13PXL_20240130_034713740.MP.jpg'),
(14, 2, 'm14PXL_20240130_033921922.MP.jpg'),
(15, 2, 'm15PXL_20240130_033940471.jpg'),
(16, 2, 'm16PXL_20240130_034007969.MP.jpg'),
(17, 2, 'm17PXLC_20240130_034025583.jpg'),
(18, 2, 'm18PXLC_20240130_034034781.MP.jpg'),
(19, 2, 'm19PXLC_20240130_034046716.jpg'),
(20, 2, 'm20PXLC_20240130_034052740.jpg'),
(21, 2, 'm21PXLC_20240130_034157779.MP.jpg'),
(22, 2, 'm22PXLC_20240130_034208375.jpg'),
(23, 2, 'm23PXLC_20240130_034213224.jpg'),
(24, 2, 'm24PXLC_20240130_034343211.MP.jpg'),
(25, 2, 'm25PXLC_20240130_034358279.jpg'),
(26, 3, 'm26PXLI_20240130_033926988.jpg'),
(27, 3, 'm27PXLI_20240130_033934688.jpg'),
(28, 3, 'm28PXLI_20240130_033940471.jpg'),
(29, 3, 'm29PXLI_20240130_034025583.jpg'),
(30, 3, 'm30PXLI_20240130_034034781.MP.jpg'),
(31, 3, 'm31PXLI_20240130_034637524.jpg'),
(32, 3, 'm32PXLI_20240130_034157779.MP.jpg'),
(33, 3, 'm33PXLI_20240130_034213224.jpg'),
(34, 3, 'm34PXLI_20240130_034353453.jpg'),
(35, 3, 'm35PXLI_20240130_034421261.MP.jpg'),
(36, 3, 'm36PXLI_20240130_034034781.MP.jpg'),
(37, 4, 'm37p7.jpeg'),
(38, 5, 'm38p6.jpeg'),
(39, 6, 'm39p1.jpeg'),
(40, 7, 'm40p5.jpeg'),
(41, 8, 'm41p3.jpeg'),
(42, 9, 'm42p2.jpeg'),
(43, 10, 'm43p4.jpeg'),
(44, 11, 'm44log.jpg'),
(45, 12, 'm45reg.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `sk_page`
--

CREATE TABLE `sk_page` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `filename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sk_page`
--

INSERT INTO `sk_page` (`id`, `title`, `filename`) VALUES
(1, 'Button', 'h1button.html'),
(2, 'Checkbox', 'h2checkbox.html'),
(3, 'Image', 'h3image1.html'),
(4, 'Name', 'h4name.html'),
(5, 'Username', 'h5username.html'),
(6, 'Password', 'h6password.html'),
(7, 'Mobile', 'h7mobile.html'),
(8, 'Email', 'h8email.html'),
(9, 'Gender', 'h9gender.html'),
(10, 'Address', 'h10address.html'),
(11, 'Login', 'h11login.html'),
(12, 'Sign Up', 'h12register.html');

-- --------------------------------------------------------

--
-- Table structure for table `sk_register`
--

CREATE TABLE `sk_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `city` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  PRIMARY KEY  (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sk_register`
--

INSERT INTO `sk_register` (`id`, `name`, `mobile`, `email`, `city`, `uname`, `pass`) VALUES
(1, 'Santhosh', 9895445274, 'santhosh@gmail.com', 'Salem', 'santhosh', '123456');
