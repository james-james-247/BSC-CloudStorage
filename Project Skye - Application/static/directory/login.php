<?php

    #There are three main functions of this file:

    #1. Connecting to the database:
    #SQL database consists of:
    #Username, Password, Directory
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "home_grown_cloud";
    session_start();

    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);

    #2. Checking if the user has logged in correctly 
    if(isset($_POST["username"])){
        $username = mysqli_real_escape_string($conn, $_POST["username"]);
        $password = mysqli_real_escape_string($conn, $_POST["password"]);

        $sql = "SELECT username, password FROM account WHERE username = '{$username}' && password = '{$password}'";
        $result = mysqli_query($conn, $sql);
        $rows = $result->num_rows;

        if($rows == 1){
            $_SESSION["loggedin"] = true;
            $_SESSION["id"] = $username;
            header("Location: success/home.php");
        }
        else{
            header("Location: index.php?loggedin=Incorrect Details");
        }
    }

    #3. Creating a new account for the user
    else if(isset($_POST["addUsername"])){
        $username = mysqli_real_escape_string($conn, $_POST["addUsername"]);
        $password = mysqli_real_escape_string($conn, $_POST["addConfirmPassword"]);

        $sql = "SELECT username FROM account WHERE username = '{$username}'";
        $result = mysqli_query($conn, $sql);
        $rows = $result->num_rows;

        if($rows === 0){
            $_SESSION["loggedin"] = true;
            
            $directory = "directory/" . $username;

            mkdir("./success/" . $directory);

            $sql = "INSERT INTO account VALUES ('$username', '$password', '$directory')";
            $result = mysqli_query($conn, $sql);

            $_SESSION["id"] = $username;
            header("Location: success/home.php");
        }
        else{
            header("Location: index.php?loggedin=Username In Use");
        }
    }

?>