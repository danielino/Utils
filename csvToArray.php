#!/usr/bin/php
# Script per convertire un file csv 
# in un array biidimensionale
# array[linea][valore_testa] = [valore_colonna]


<?php
$file = $argv[1];
$asd = csvToArray($file);

function csvToArray($file){
	if(isset($file) && $file != "" && is_file($file)){
            
		$fp = fopen($file,'r');
		/* 2D array[riga][colonna][valore] */
		$csvArray = array(array(array()));
				
		/* contatore righe */
		$col_counter = 0;
		/* contatore colonne */
		$row_counter = 0;
		$headLine = fgetcsv($fp,10000,';');
		$csvArray[$row_counter][$col_counter] = array();
		while (($line = fgetcsv($fp,10000,';')) !== false) {
			foreach($line as $column){
				$pointerHeadLine = str_replace('ÿþ',"",$headLine[$col_counter]);
				$csvArray[$row_counter][$pointerHeadLine] = $column;
				$col_counter++;
			}
			$col_counter = 0;
			$row_counter++;
		}
	}
//var_dump($csvArray);
return $csvArray;
}
print_r($asd);

?>
