<?php
include('session.php');
?>
<!DOCTYPE html>
<html>
	<head>
	<link rel="stylesheet" href="css/sensitiveWords.css" type="text/css">
	<title>Sensitive Words | Social Media Agrregator</title>
	<h1 align="center"> Sensitive Word List </h1>
	<br \><br \><br \>

	<div id="bodyTable" align="center" style="font-size:100%; background-color:#000000;">
	
<?php
		
		//Establish a connection.
		//error_reporting(E_ERROR | E_PARSE);
		
		//Check connection
		if (mysqli_connect_errno())
		  {
		  echo "Failed to connect to MySQL: " . mysqli_connect_error();
		  } 
		$result = mysqli_query($connection,"SELECT Word FROM sensitive_words");
/*		echo "<table border='2' >
		<tr> 
		<th>Word</th>
		</tr>";
*/
		//Display the Data
		$i=3;
		while($row = mysqli_fetch_array($result))
		  {
			echo "<p id=cardHolder>";
			//echo "<tr>";
			//if($i%6==0){echo"<br>";}
	    	echo "<a href='WordDisplay.php?Word={$row['Word']}'>".$row['Word']."</a>";
			echo "&nbsp;";
	    	//echo "<td>" . $row['Word'] . "</td>";
			echo "";
			$i++;
			echo "</p>";
		  }
	//	echo "</table>";
		//Close after the work is complete and to avoid SQL Attacks.
		mysqli_close($connection);
	?>
	</div>
	</body>
</html>