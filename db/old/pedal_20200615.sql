-- MySQL Script generated by MySQL Workbench
-- Mon Jun 15 14:09:50 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema pedal_dev_v_0
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `pedal_dev_v_0` ;

-- -----------------------------------------------------
-- Schema pedal_dev_v_0
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pedal_dev_v_0` DEFAULT CHARACTER SET utf8 ;
USE `pedal_dev_v_0` ;

-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`study`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`study` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`study` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `code` VARCHAR(45) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`study_version`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`study_version` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`study_version` (
  `id` INT NOT NULL,
  `study_id` INT NOT NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`, `study_id`),
  INDEX `fk_study_version_study1_idx` (`study_id` ASC),
  CONSTRAINT `fk_study_version_study1`
    FOREIGN KEY (`study_id`)
    REFERENCES `pedal_dev_v_0`.`study` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`arm`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`arm` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`arm` (
  `id` INT NOT NULL,
  `version_id` INT NOT NULL,
  `study_id` INT NOT NULL,
  `code` VARCHAR(45) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_arm_study_version1_idx` (`version_id` ASC, `study_id` ASC),
  CONSTRAINT `fk_arm_study_version1`
    FOREIGN KEY (`version_id` , `study_id`)
    REFERENCES `pedal_dev_v_0`.`study_version` (`id` , `study_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`site`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`site` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`site` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`treatment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`treatment` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`treatment` (
  `id` INT NOT NULL,
  `level_code` VARCHAR(45) NULL,
  `level_display` VARCHAR(128) NULL,
  `description` VARCHAR(512) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`criterion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`criterion` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`criterion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(45) NULL,
  `display_name` VARCHAR(128) NULL,
  `description` VARCHAR(512) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`elegibility_criteria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`elegibility_criteria` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`elegibility_criteria` (
  `id` INT NOT NULL,
  `arm_id` INT NOT NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`, `arm_id`),
  INDEX `fk_elegibility_criteria_arm1_idx` (`arm_id` ASC),
  CONSTRAINT `fk_elegibility_criteria_arm1`
    FOREIGN KEY (`arm_id`)
    REFERENCES `pedal_dev_v_0`.`arm` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`el_criteria_has_criterion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`el_criteria_has_criterion` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`el_criteria_has_criterion` (
  `criterion_id` INT NOT NULL,
  `elegibility_criteria_id` INT NOT NULL,
  `arm_id` INT NOT NULL,
  `code` VARCHAR(45) NOT NULL,
  `display_name` VARCHAR(45) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`criterion_id`, `elegibility_criteria_id`, `arm_id`),
  INDEX `fk_criterion_criterion_list1_idx` (`criterion_id` ASC),
  INDEX `fk_el_criteria_has_criterion_elegibility_criteria1_idx` (`elegibility_criteria_id` ASC, `arm_id` ASC),
  CONSTRAINT `fk_criterion_criterion_list1`
    FOREIGN KEY (`criterion_id`)
    REFERENCES `pedal_dev_v_0`.`criterion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_el_criteria_has_criterion_elegibility_criteria1`
    FOREIGN KEY (`elegibility_criteria_id` , `arm_id`)
    REFERENCES `pedal_dev_v_0`.`elegibility_criteria` (`id` , `arm_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`value`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`value` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`value` (
  `id` INT NOT NULL,
  `code` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `display_value` VARCHAR(45) NULL,
  `upper_threshold` DECIMAL(19,4) NULL,
  `lower_threshold` DECIMAL(19,4) NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`arm_treatment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`arm_treatment` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`arm_treatment` (
  `arm_id` INT NOT NULL,
  `treatment_id` INT NOT NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`arm_id`, `treatment_id`),
  INDEX `fk_arm_has_treatment_treatment1_idx` (`treatment_id` ASC),
  INDEX `fk_arm_has_treatment_arm1_idx` (`arm_id` ASC),
  CONSTRAINT `fk_arm_has_treatment_arm1`
    FOREIGN KEY (`arm_id`)
    REFERENCES `pedal_dev_v_0`.`arm` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_arm_has_treatment_treatment1`
    FOREIGN KEY (`treatment_id`)
    REFERENCES `pedal_dev_v_0`.`treatment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`algorithm_engine`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`algorithm_engine` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`algorithm_engine` (
  `id` INT NOT NULL,
  `version` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `link` VARCHAR(256) NULL,
  `description` VARCHAR(512) NULL,
  `function` VARCHAR(512) NULL,
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`study_algorithm_engine`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`study_algorithm_engine` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`study_algorithm_engine` (
  `study_version_id` INT NOT NULL,
  `algorithm_engine_id` INT NOT NULL,
  `study_id` INT NOT NULL,
  `date from` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`study_version_id`, `algorithm_engine_id`, `study_id`),
  INDEX `fk_study_version_has_algorithm_engine_algorithm_engine1_idx` (`algorithm_engine_id` ASC),
  INDEX `fk_study_algorithm_engine_study_version1_idx` (`study_version_id` ASC, `study_id` ASC),
  CONSTRAINT `fk_study_version_has_algorithm_engine_algorithm_engine1`
    FOREIGN KEY (`algorithm_engine_id`)
    REFERENCES `pedal_dev_v_0`.`algorithm_engine` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_study_algorithm_engine_study_version1`
    FOREIGN KEY (`study_version_id` , `study_id`)
    REFERENCES `pedal_dev_v_0`.`study_version` (`id` , `study_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`site_has_study`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`site_has_study` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`site_has_study` (
  `site_id` INT NOT NULL,
  `study_id` INT NOT NULL,
  `create_date` DATETIME NULL,
  `active` TINYINT NULL,
  PRIMARY KEY (`site_id`, `study_id`),
  INDEX `fk_site_has_study_study1_idx` (`study_id` ASC),
  INDEX `fk_site_has_study_site1_idx` (`site_id` ASC),
  CONSTRAINT `fk_site_has_study_site1`
    FOREIGN KEY (`site_id`)
    REFERENCES `pedal_dev_v_0`.`site` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_site_has_study_study1`
    FOREIGN KEY (`study_id`)
    REFERENCES `pedal_dev_v_0`.`study` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pedal_dev_v_0`.`criterion_has_value`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pedal_dev_v_0`.`criterion_has_value` ;

CREATE TABLE IF NOT EXISTS `pedal_dev_v_0`.`criterion_has_value` (
  `criterion_id` INT NOT NULL,
  `value_id` INT NOT NULL,
  PRIMARY KEY (`criterion_id`, `value_id`),
  INDEX `fk_criterion_has_value_value1_idx` (`value_id` ASC),
  INDEX `fk_criterion_has_value_criterion1_idx` (`criterion_id` ASC),
  CONSTRAINT `fk_criterion_has_value_criterion1`
    FOREIGN KEY (`criterion_id`)
    REFERENCES `pedal_dev_v_0`.`criterion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_criterion_has_value_value1`
    FOREIGN KEY (`value_id`)
    REFERENCES `pedal_dev_v_0`.`value` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;