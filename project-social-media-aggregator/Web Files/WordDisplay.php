<?php
include('session.php');
?>
<!DOCTYPE html>
<html>
	<head>
	<link rel="stylesheet" href="css/wordDisplay.css" type="text/css">
	<title>Sensitive Word | Social Media Aggregator</title>
	</head>
	<body>
	
	<div id="wordDisplay">
<?php
		echo "<p align='center'> Your intended Keyword is: " . $_GET['Word'] . ".</p>";
		//Establish a connection.
		//$connection = mysqli_connect("localhost","root","","sma");
		
		//error_reporting(E_ERROR | E_PARSE);
		
		// Check connection
		if (mysqli_connect_errno())
		  {
		  echo "Failed to connect to MySQL: " . mysqli_connect_error();
		  } 
		//$userInput=$_POST['userInput'];
		function make_links_clickable($text){
    	return preg_replace('!(((f|ht)tp(s)?://)[-a-zA-Zа-яА-Я()0-9@:%_+.~#?&;//=]+)!i', '<a href="$1">$1</a>', $text);
		}

		
		//echo $userInput; Used to test the input rading of keyword //remove once Code is up and running.
		$result = mysqli_query($connection,"SELECT * FROM links WHERE keyword='{$_GET['Word']}'");
		// Format the Display of Data
		echo "<table border='2' align='center'>
		<tr> 
		<th>Serial Number</th>
		<th>Link</th>
		<th>Intended Keyword</th>
		<th>Time of Crawling</th>
		</tr> </font> ";

		//Display the Data
		while($row = mysqli_fetch_array($result))
		  {
		echo "<tr>";
		  echo "<td>" . $row['sr_no'] . "</td>";
		  $temp = $row['link'];
		  $temp1 = make_links_clickable($temp);
		  echo "<td>" . $temp1 . "</td>";
		  echo "<td>" . $row['keyword'] . "</td>";
		  //echo "<td>" . $row['link'] . "</td>";
		  echo "<td>" . $row['date'] . "</td>";
		  echo "</tr>";
		  }
		echo "</table>";

		//Close after the work is complete and to avoid SQL Attacks.
		mysqli_close($connection);
?>
	</body>
</html>