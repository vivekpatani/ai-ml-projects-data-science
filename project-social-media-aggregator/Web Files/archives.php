<?php
include('session.php');
?>
<!DOCTYPE html>
<html>
	<head>
	<title> Archive | Social Media Aggregator </title>
	<script src="js/datetimepicker_css.js"></script>
	<link rel="stylesheet" type="text/css" href="css/button.css">
	<link rel="stylesheet" type="text/css" href="css/archives.css">
	</head>
	<body>
		<div id="title-page" align="center">
			<h1> Archive Retrieval </h1>
		</div>
		<!-- The Date Picker Form and Calling the JS -->
		<div style="text-align:center;" align="center">
		 <form action="" method="POST" style="margin-top:20px;">
			 <label for="demo3">Please enter a date here: </label>
			 <input name="demo3" type="Date" id="demo3"/>
			 <img src="images/cal.gif" onclick="javascript:NewCssCal ('demo3','yyyyMMdd','arrow')" style="cursor:pointer"/>
			 <br \><br \>
			 <input name="Submit" type="submit" value="Submit">
		 </form>
		</div>
		<div id="archiveList">
<?php
		
		//Require this file to connect, make any database changes in the config.php file nothing here.
		//$userInput = NULL;
		// Check connection
		if (mysqli_connect_errno())
		  {
		  echo "Failed to connect to MySQL: " . mysqli_connect_error();
		  }
		function make_links_clickable($text){
    	return preg_replace('!(((f|ht)tp(s)?://)[-a-zA-Zа-яА-Я()0-9@:%_+.~#?&;//=]+)!i', '<a href="$1">$1</a>', $text);
		}	
		
		if(!empty($_POST['demo3'])){
			$userInput=$_POST['demo3'];
		echo $userInput; //Used to test the input reading of keyword //remove once Code is up and running.
		$result = mysqli_query($connection,"SELECT * FROM links where date='$userInput'");
		
		// Format the Display of Data
		echo "<table border='2' align='center'>
		<tr> 
		<th>Serial Number</th>
		<th>Keyword</th>
		<th>Link</th>
		<th>Date of Crawling</th>
		</tr> </font> ";

		//Display the Data
		while($row = mysqli_fetch_array($result))
		  {
		  echo "<tr>";
		  echo "<td>" . $row['sr_no'] . "</td>";
		  echo "<td>" . $row['keyword'] . "</td>";
		  $temp = $row['link'];
		  $temp1 = make_links_clickable($temp);
		  echo "<td>" . $temp1 . "</td>";
		  echo "<td>" . $row['date'] . "</td>";
		  echo "</tr>";
		  }
		echo "</table>";
		}
		//Close after the work is complete and to avoid SQL Attacks.
		mysqli_close($connection);
	?>
	</div>
	</body>
</html>
