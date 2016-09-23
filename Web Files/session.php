
<?php
	include_once("analyticstracking.php");
	include('config.php');
	session_start();// Starting Session
	
	
	
	// Storing Session
	$user_check = $_SESSION['login_user'];
	
	// SQL Query To Fetch Complete Information Of User
	$ses_sql = mysqli_query($connection,"select username from login where username='$user_check'");
	$row = mysqli_fetch_assoc($ses_sql);
	$login_session = $row['username'];
	
	include('header.php');
	
	if(!isset($login_session)){
		mysqli_close($connection); // Closing Connection
		header('Location: index.php'); // Redirecting To Home Page
	}
?>