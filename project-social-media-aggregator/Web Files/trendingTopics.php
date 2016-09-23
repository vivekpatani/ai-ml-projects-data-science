<?php
include('session.php');
?>
<!DOCTYPE html>
<html>
	<head>
	<title>Trending Topics | Social Media Aggregator</title>
	<link rel="stylesheet" href="css/trendingTopics.css" type="text/css">
	</head>
	<body>
	<h1 align="center"> Todays Trending Topics </h1>
	<p align="center"> These are intended to be 10 most important topics </p>
	<div id="displayBox" align="center">
<?php
		
		//Establish a connection.
		
		//error_reporting(E_ERROR | E_PARSE);
		$i=0;
		// Check connection
		if (mysqli_connect_errno())
		  {
		  echo "Failed to connect to MySQL: " . mysqli_connect_error();
		  } 
		//$userInput=$_POST['trend'];
		function make_links_clickable($text){
    	return preg_replace('!(((f|ht)tp(s)?://)[-a-zA-Zа-яА-Я()0-9@:%_+.~#?&;//=]+)!i', '<a href="$1">$1</a>', $text);
		}
		//echo $userInput; Used to test the input rading of keyword //remove once Code is up and running.
		$result = mysqli_query($connection,"SELECT * FROM trends");
		
		// Format the Display of Data
		echo "<table border='2' align='center'>
		<tr> 
		<th>Serial Number</th>
		<th>Link</th>
		</tr> </font> ";
		//$i=1;
		//Display the Data
		while($row = mysqli_fetch_array($result))
		  {
		  echo "<tr>";
		  $i++;
		  echo "<td>" . $i . "</td>";
		  $temp = $row['links'];
		  $temp1 = make_links_clickable($temp);
		  //$i++;
		  //echo "$temp1";
		  echo "<td>" . $temp1 . "</td>";
		  //echo "<a href='www.google.com?Word={$row['links']}'>".$row['links']."</a>";
		  //echo "<br>";
		  echo "</tr>";
		  }
		echo "</table>";

		//Close after the work is complete and to avoid SQL Attacks.
		mysqli_close($connection);
	?>
	</div>
	</body>
</html>