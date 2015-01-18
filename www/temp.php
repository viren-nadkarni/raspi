<?php
$link = mysql_connect( 'localhost', 'root', '' );
if ( !$link ) {
  die( 'Could not connect: ' . mysql_error() );
}

$db = mysql_select_db( 'temp', $link );
if ( !$db ) {
  die ( 'Error selecting database \'test\' : ' . mysql_error() );
}

// Current temperature and recorded timestamp
$query = "SELECT time, temp FROM ds WHERE time=(SELECT MAX(time) FROM ds);";
$result = mysql_query( $query );
if ( !$result ) {
  $message  = 'Invalid query: ' . mysql_error() . "\n";
  $message .= 'Whole query: ' . $query;
  die( $message );
}
$row = mysql_fetch_assoc( $result );
$now_temp = $row['temp'];
$now_temp_timestamp = $row['time'];

// Min, max temp in last 24 hours
$time_now = time();
$time_24hr_ago = $time_now - 86400;
$query = "SELECT min(temp) mn, max(temp) mx FROM ds WHERE time > $time_24hr_ago;";
$result = mysql_query( $query );
if ( !$result ) {
  $message  = 'Invalid query: ' . mysql_error() . "\n";
  $message .= 'Whole query: ' . $query;
  die( $message );
}
$row = mysql_fetch_assoc( $result );
$min_24hr = $row['mn'];
$max_24hr = $row['mx'];

echo "{\n";
echo "  \"min\": $min_24hr,\n";
echo "  \"max\": $max_24hr,\n";
echo "  \"now\": $now_temp,\n";
echo "  \"time\": $now_temp_timestamp\n";
echo "}";

?>
