<?php
	// Include in files which need connection, use $connection to connect.
	
	define('DB_NAME', 'swarnshi_sma');
	define('DB_USER', 'swarnshi_riya123');
	define('DB_PASSWORD', 'riya123');
	define('DB_HOST', 'localhost');
	
	
	$connection = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME);
	//echo "Connection Successful!"; //Defining the variable.
	//define('TITLE', 'sitetitle'); //Already there in HTML Code.
?>