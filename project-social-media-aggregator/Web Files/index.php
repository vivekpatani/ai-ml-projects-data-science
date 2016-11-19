<?php
include('login.php'); // Includes Login Script

	if(isset($_SESSION['login_user'])){
	header("location: home.php");
	}
?>
<!DOCTYPE html>
<html>

<head>

  <meta charset="UTF-8">

  <title>Login | Police Portal</title>

    <link rel="stylesheet" href="css/style-login.css">
	<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>

</head>

	<body>
		
		<img src="images/logo.png" width ="125px" height="125px" alt="Logo" title="Logo" style="display:block; float:left; margin-top:25px;"/> <br />
		<img src="images/logo.png" width ="125px" height="125px" alt="Logo" title="Logo" style="display:block; float:right;"/> <br /></p>
		<p align="center" style="font-size:300%; color:white;"> Police Portal </p>
		
		<!--  <span href="#" class="button" id="toggle-login">Log in</span> -->
			<hr style="color:white; margin-top:20px; margin-bottom:20px;"> 
			<div id="login">
			<!--  <div id="triangle"></div> -->
			  <div id="main">
				  <div id="login">
				  <h1>Log In</h1>
					<form action="" method="post">
						<label>User Identification</label>
						<input id="name" name="username" placeholder="User Name" type="text">
						<label>Password</label>
						<input id="password" name="password" placeholder="**********" type="password">
						<input name="submit" type="submit" value=" Login " />
						<span><?php echo $error; ?></span>
					</form>
				</div>
			</div>
			<div id="registration"></div>
			
				
		<script src="js/index-login.js"></script>

	</body>

</html>