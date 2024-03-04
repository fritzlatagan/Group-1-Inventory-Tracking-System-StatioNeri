-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 04, 2024 at 01:19 PM
-- Server version: 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stockmanagementsystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL,
  `item_id` mediumtext,
  `name` mediumtext,
  `price` mediumtext,
  `quantity` mediumtext,
  `description` mediumtext,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=Aria DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` (`id`, `item_id`, `name`, `price`, `quantity`, `description`, `date`) VALUES
(18, '429-U', 'Ballpen - Blk', '10', '99999', 'Black Ballpen', '2024-03-03 22:36:58'),
(21, '376-B', 'Ballpen - Blu', '10', '9999', 'Blue Ballpen', '2024-03-04 19:51:18'),
(27, '268-D', 'Crayons - 24s', '100', '200', 'Box Crayons (24s)', '2024-03-04 20:06:52'),
(24, '834-P', 'Meter Stick - P', '50', '250', 'Plastic Meter Stick', '2024-03-04 20:03:24'),
(23, '353-P', 'Meter Stick - W', '50', '250', 'Wooden Meter Stick', '2024-03-04 20:02:56'),
(20, '587-J', 'Notebook - Blk, Spr', '17', '850', 'Black Springbound Notebook', '2024-03-04 19:50:27'),
(19, '713-I', 'Notebook - Blu, Spr', '17', '900', 'Blue Springbound Notebook ', '2024-03-04 18:27:53'),
(26, '818-J', 'Ruler - M', '12', '500', 'Metalic 12 inch ruler', '2024-03-04 20:04:31'),
(25, '769-U', 'Ruler - P', '12', '500', 'Plastic 12 inch ruler', '2024-03-04 20:04:13'),
(22, '336-X', 'Ruler - W', '12', '500', 'Wooden 12 inch ruler', '2024-03-04 20:02:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `stocks`
--
ALTER TABLE `stocks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
