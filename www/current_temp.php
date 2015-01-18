<?php
$link = mysql_connect( 'localhost', 'root', '' );
if ( !$link ) {
  die( 'Could not connect: ' . mysql_error() );
}

$db = mysql_select_db( 'temp', $link );
if ( !$db ) {
  die ( 'Error selecting database \'test\' : ' . mysql_error() );
}

$query = "select temp from ds where time=(select max(time) from ds);";

$result = mysql_query( $query );

if ( !$result ) {
  $message  = 'Invalid query: ' . mysql_error() . "\n";
  $message .= 'Whole query: ' . $query;
  die( $message );
}

$row = mysql_fetch_assoc( $result );
echo $row['temp'];
?>
