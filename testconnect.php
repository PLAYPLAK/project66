<?php
// Retrieve form data
$servername = $_POST['servername'];
$username = $_POST['username'];
$password = $_POST['password'];
$dbname = $_POST['dbname'];

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data from the database
$sql = "SHOW TABLES";
$result = $conn->query($sql);


//กรณีที่รู้ตัวข้อมูล
if ($result->num_rows > 0) {
    // Output data of each row

    //กรณีที่รู้ตัวข้อมูล
    /*
    while ($row = $result->fetch_assoc()) {
        echo "Name: " . $row["name"] . " - Age: " . $row["age"] . " - Email: " . $row["email"] . "<br>";
    }
    */
    //กรณีที่ต้องการแสดงทั้งหมด
    
    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        foreach ($row as $columnName => $columnValue) {
            echo "<td>" . $columnValue . "</td>";
        }
        echo "</tr>";
    }
        
} else {
    echo "No data found";
}



// Close connection
$conn->close();
?>
