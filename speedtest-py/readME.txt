pip install mysql-connector-python

CREATE TABLE `test-catma`.`devices` ( `id` INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY , `host` VARCHAR(100) NOT NULL , `ping` DOUBLE(10) NULL , `download` DOUBLE(10) NULL , `upload` DOUBLE(10) NULL , `execTime` DOUBLE(10) NULL ) ENGINE = InnoDB;

INSERT INTO `test-catma`.`devices` (`order`, `host`, `ping`, `download`, `upload`, `runTime`) VALUES (NULL, 'node3', '33.3', '3.333', '3.33', '33.3');


--------------------------------------------------
def test_var_args(f_arg, *argv):
    print "first normal arg:", f_arg
    for arg in argv:
        print "another arg through *argv :", arg

test_var_args('yasoob','python','eggs','test')
first normal arg: yasoob
another arg through *argv : python
another arg through *argv : eggs
another arg through *argv : test
--------------------------------------------------

UPDATE `test-catma`.`devices` SET `download` = '2.00' WHERE `devices`.`order`