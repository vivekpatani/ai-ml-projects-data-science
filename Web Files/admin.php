<?php
include 'session.php';
?>
<!DOCTYPE HTML>
<HTML>
	<title> Admin Panel </title>
	<head>
		<link rel="stylesheet" type="text/css" href="css/admin.css">
	</head>
	<body>
	<div id="displayonly">
		<h1 align="center"> Hello, <?php echo $login_session; ?>! </h1>
	</div>	
	<div id="WordManip">
		<form action="" method="post" align="center">
			Enter Word To Be Added: <input type="text" name="wordadd"><br />
			<input type="submit" style="display">
		</form>
		
		<form action="" method="post" align="center">
			Enter Word To Be Deleted: <input type="text" name="worddel"><br />
			<input type="submit" style="display">
		</form>
		</div>
	</body>	
</html>		
		<?php
		if (mysqli_connect_errno())
		  {
		  echo "Failed to connect to MySQL: " . mysqli_connect_error();
		  }
		
		if(!empty($_POST['wordadd'])){
			$userInput=$_POST['wordadd'];
		//echo $userInput; //Used to test the input reading of keyword //remove once Code is up and running.
		$result = mysqli_query($connection,"INSERT INTO `swarnshi_sma`.`sensitive_words` (`ID`, `Word`) VALUES (NULL, '$userInput');");
		}
		
		if(!empty($_POST['worddel'])){
			$userInput2=$_POST['worddel'];
		//echo $userInput2; //Used to test the input reading of keyword //remove once Code is up and running.
		$result = mysqli_query($connection,"DELETE FROM `swarnshi_sma`.`sensitive_words` WHERE Word='$userInput2';");
		}
		
		echo "<p align='center'> Here is the list of Words" . ",/p>";
		$result1 = mysqli_query($connection,"SELECT * FROM sensitive_words"); 
		
		echo "<table border='2'  align='center'>
		<tr> 
		<th>ID</th>
		<th>Keywords</th>
		</tr>";

		//Display the Data
		while($row = mysqli_fetch_array($result1))
		  {
		echo "<tr>";
		  echo "<td>" . $row['ID'] . "</td>";
		  echo "<td>" . $row['Word'] . "</td>";
		 echo "</tr>";
		  }
		echo "</table>";
		
	mysqli_close($connection);
?>
