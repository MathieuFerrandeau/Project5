SET NAMES utf8;

-- Table category
CREATE TABLE IF NOT EXISTS category (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Table product
CREATE TABLE IF NOT EXISTS product (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  name varchar(200) NOT NULL,
  store varchar(100) NOT NULL,
  link text NOT NULL,
  nutriscore varchar(1) NOT NULL,
  category smallint(3) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Table substitue
CREATE TABLE IF NOT EXISTS substitute (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  id_product_to_substitute smallint(3) NOT NULL,
  id_substitute_product smallint(3) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

ALTER TABLE product ADD CONSTRAINT fk_product FOREIGN KEY (category) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE substitute ADD CONSTRAINT fk_substitute_product FOREIGN KEY (id_substitute_product) REFERENCES product (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE substitute ADD CONSTRAINT fk_product_to_substitute FOREIGN KEY (id_product_to_substitute) REFERENCES product (id) ON DELETE CASCADE ON UPDATE CASCADE;
