<?php
declare(strict_types=1);

$host = 'localhost';
$user = 'root';
$password = '';
$database = 'lab6_webapp';

function create_connection(): mysqli
{
    global $host, $user, $password, $database;

    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

    $connection = new mysqli($host, $user, $password, $database);
    $connection->set_charset('utf8mb4');

    return $connection;
}
