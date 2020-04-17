<?php
if($_POST["message"]) {
    mail("shivamrana706@gmail.com", "Form to email message", $_POST["message"], "From: shivamrana706@gmail.com");
}
?>

