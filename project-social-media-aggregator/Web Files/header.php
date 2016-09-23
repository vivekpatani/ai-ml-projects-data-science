<?php
?>
<!DOCTYPE HTML>
<HTML lang="en">
	<head>
		<link href='http://fonts.googleapis.com/css?family=Oswald:400,300,700' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
		<link rel="stylesheet" type="text/css" href="css/header.css">
		<link rel="stylesheet" type="text/css" href="css/sub-header.css">
		<link rel="stylesheet" type="text/css" href="css/normalise.css">	
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
		<meta name="description" content="This is a police portal." />
		<meta name="keywords" content="police, portal, social, media, aggregator" />
		<meta name="author" content="Riya Patni, Vruksha Shah, Rhythm Shah, Vivek Patani" />
		<link rel="shortcut icon" href="../favicon.ico">
	</head>
	<body>
	
		<!-- Use to Display the top most line on a page -->
		<div id="top-line">
			<!-- Used to display name -->
			<p id="hi_name"> Hi, <?php echo $login_session; ?>! </p>
			<!-- Used to display the top menu -->
			<ul>
			  <li><a href="home.php"><i class="fa fa-home fa-fw"></i>Home&nbsp;</a></li>
			  <li><a href="contact-police.php"><i class="fa fa-phone-square fa-fw"></i>Contact&nbsp;</a></li>
			  <li><a href="developers.php"><i class="fa fa-code fa-fw"></i>Developers</a></li>
			</ul>
			<br>
		</div>
		
		<!-- Use to display the Police Portal header with Logo -->
		<div id="sub-header" style="background-color:#808080">
			<h1 align="center"><i class="fa fa-cog fa-spin"></i>&nbsp; Police Portal &nbsp;<i class="fa fa-cog fa-spin"></i></h1>
		</div>
		
		<!-- Use to display sub-menu -->
		<div id="sub-menu" align="center">
			<ul>
			  <li><a href="sensitiveWords.php"><i class="fa fa-globe fa-fw"></i>Sensitive Words</a></li>
			  <li><a href="trendingTopics.php"><i class="fa fa-bars fa-fw"></i>Trending Topics</a></li>
			  <li style="margin-left:-40px;"><a href="archives.php"><i class="fa fa-archive fa-fw"></i>Archives</a></li>
			  <li style="margin-left:-75px;"><a href="logout.php"><i class="fa fa-sign-out fa-fw"></i>Logout</a></li>
			</ul>
		</div>	
	</body>
</HTML>	