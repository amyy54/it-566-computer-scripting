SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE USER IF NOT EXISTS 'home_inventory_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'home_inventory_user'@'%';
GRANT ALL PRIVILEGES ON `home\_inventory\_user\_%`.* TO 'home_inventory_user'@'%';

COMMIT;
