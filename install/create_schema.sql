# DOMAINS
-- relay_tasks_manager.`domain` definition

CREATE TABLE `domain` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- father_task
-- relay_tasks_manager.father_task definition

CREATE TABLE `father_task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(40) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `manager` varchar(100) DEFAULT NULL,
  `complete_by_order` tinyint(1) DEFAULT '0',
  `deadline` datetime DEFAULT NULL,
  `completed_date` datetime DEFAULT NULL,
  `locked` tinyint(1) DEFAULT '0',
  `creator_id` varchar(100) DEFAULT NULL,
  `is_template` tinyint(1) DEFAULT '0',
  `creation_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=255 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- relay_tasks_manager.status definition

CREATE TABLE `status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- relay_tasks_manager.task definition

CREATE TABLE `task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `type_id` int unsigned DEFAULT NULL,
  `domain_id` varchar(100) DEFAULT NULL,
  `father_id` int unsigned DEFAULT NULL,
  `status_id` int unsigned DEFAULT NULL,
  `urgency_id` int unsigned DEFAULT NULL,
  `priority` int NOT NULL DEFAULT '1',
  `crew` varchar(100) DEFAULT NULL,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `files_url` text,
  `plannings` text,
  `building` text NOT NULL DEFAULT (_utf8mb4'{}'),
  `equipment` text,
  `check_list` text,
  `creator_id` varchar(100) DEFAULT NULL,
  `fault_data` text,
  `file_required` tinyint(1) DEFAULT '0',
  `background` tinyint(1) DEFAULT '0',
  `is_template` tinyint(1) DEFAULT '0',
  `is_reschedule` tinyint(1) DEFAULT '0',
  `creation_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `father_id` (`father_id`),
  KEY `status_id` (`status_id`),
  KEY `urgency_id` (`urgency_id`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `task_type` (`id`),
  CONSTRAINT `task_ibfk_2` FOREIGN KEY (`father_id`) REFERENCES `father_task` (`id`),
  CONSTRAINT `task_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `task_ibfk_4` FOREIGN KEY (`urgency_id`) REFERENCES `urgency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- relay_tasks_manager.task_scheduler definition

CREATE TABLE `task_scheduler` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `template_father_task_id` int NOT NULL,
  `start_date` date DEFAULT (curdate()),
  `end_date` date DEFAULT NULL,
  `freq` int DEFAULT NULL,
  `interval_value` int DEFAULT NULL,
  `specific_value` varchar(100) DEFAULT NULL,
  `next_date` date DEFAULT NULL,
  `creator_id` varchar(50) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- relay_tasks_manager.task_type definition

CREATE TABLE `task_type` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `equipment_required` tinyint(1) DEFAULT '0',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- relay_tasks_manager.urgency definition

CREATE TABLE `urgency` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- relay_tasks_manager.users definition

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `domain_id` int DEFAULT NULL,
  `permissions` varchar(30) NOT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;