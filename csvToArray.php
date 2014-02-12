#!/usr/bin/php
# Script per convertire un file csv 
# in un array biidimensionale
# array[linea][valore_testa] = [valore_colonna]


<?php
$file = $argv[1];

print_r(csvToArray($file));



function csvToArray($filename='', $delimiter=',')
{
        if(!file_exists($filename) || !is_readable($filename))
            return false;
        
        $header = NULL;
        $data = array();

        if ( $fp = fopen($filename, 'r') )
        {
            while ( $row = fgetcsv($handle, 1000, $delimiter) )
            {
                if(count($row) < 1)
                    continue;

                if(!$header)
                    $header = $row;
                 else
                    $data[] = array_combine($header, $row);
            }
            fclose($fp);
        }
        return $data;
}


?>
