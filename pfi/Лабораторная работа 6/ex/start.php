<?php
   // session_start();
   // $_SESSION['stop'] = 1;
if(isset($_POST["iterations"]))
{
    $iter = $_POST["iterations"];
}
require_once 'connection.php'; // подключаем скрипт
 
$link = mysqli_connect($host, $user, $password, $database) 
    or die("Ошибка " . mysqli_error($link)); 
     
$query ="SELECT ID FROM ServerNodes";
$result = mysqli_query($link, $query) or die("Ошибка " . mysqli_error($link)); 
if($result){
    $rows = mysqli_num_rows($result); // количество полученных строк
    $itervpc = $iter / $rows;
    for ($i = 0 ; $i < $rows ; ++$i)
    {
        $row = mysqli_fetch_row($result);
        $array[0][$i]= $row[0];
        $iterleft = $itervpc * $i;
        $iterright= $itervpc * ($i + 1) - 1;
        $array[1][$i] = $iterleft;
        $array[2][$i] = $itervpc * ($i + 1) - 1;
    }
    mysqli_free_result($result);
}
for ($i = 0 ; $i < $rows ; ++$i){
    $v1=$array[1][$i];
    $v2=$array[2][$i];
    $v0=$array[0][$i];
    $v3="0.0";
    $v7="1";
$sql = "UPDATE ServerNodes SET LEFTITER=$v1, RIGHTITER=$v2, CALCVALUE=$v3, CURITER=$v1, STAT=$v7 WHERE ID=$v0";
if ($link->query($sql) === TRUE){
echo "БД обновлена. Ждем ответа от вычислительного узла...";
} else {
echo "Error: ".$sql."<br>".$link->connect_error;
}
}
mysqli_close($link);
?>
