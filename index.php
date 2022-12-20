<?php

// THIS CODE DO BE WILDIN', FR NO CAP
function signin()
{
    // curl
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'http://localhost:5000/signin');
    $payload = json_encode(array(
        'email' => 'aqmal.pratama81@gmail.com',
        'password' => 'ilkompjaya'
    ));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt(
        $ch,
        CURLOPT_HTTPHEADER,
        array('Content-Type:application/json')
    );
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, true);
    $signin = curl_exec($ch);
    // just to get the cookie from such request must gone trough this complex shit
    preg_match_all('/^Set-Cookie:\s*([^;]*)/mi', $signin, $matches);
    $cookies = array();
    foreach ($matches[1] as $item) {
        parse_str($item, $cookie);
        $cookies = array_merge($cookies, $cookie);
    }
    return $cookies;
}

$BASE_URL = 'http://localhost:5000/consultationSession/upcoming/';
// UNAUTHORIZE
$id = 0;
$response = '';
if (isset($_GET['submit'])) {
    $id = $_GET['userid'];
    $ch = curl_init();
    $cookie = signin()["session"];
    $strcookie = "session=$cookie;";
    curl_setopt($ch, CURLOPT_COOKIE, $strcookie);
    curl_setopt($ch, CURLOPT_URL, $BASE_URL . $id);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
}
$response = json_decode($response, true);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>testingID</title>
</head>
<body>
    <h1>Testing ID</h1>
    <!-- <span>
        <sub>
            <pre>
        The place to practice php
            </pre>
        </sub>
    </span> -->
    <form action="" method="get">
        <label for="">User ID </label>
        <input type="number" name="userid">
        <br />
        <input type="submit" value="Send" name="submit">
    </form>
    <?php if ($response != '') : ?>
        <h1>Data</h1>
        <div id="myDIV" style='display: none'>
            <table border="10">
                <thead>
                    <tr>
                        <th>Count</th>
                        <th>Key</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $no = 1;
                    foreach ($response as $key => $val) : ?>
                        <tr>
                            <td rowspan="8" align="center">
                                <?= $no++; ?>
                            </td>
                            <td>consultation_date</td>
                            <td><?= $val['consultation_date'] ?></td>
                        </tr>
                        <tr>
                            <td>end_time</td>
                            <td><?= $val['end_time'] ?></td>
                        </tr>
                        <tr>
                            <td>id</td>
                            <td><?= $val['id'] ?></td>
                        </tr>
                        <tr>
                            <td>is_accepted_mentor</td>
                            <td><?= $val['is_accepted_mentor'] ?></td>
                        </tr>
                        <tr>
                            <td>mentor_id</td>
                            <td><?= $val['mentor_id'] ?></td>
                        </tr>
                        <tr>
                            <td>payment_status</td>
                            <td><?= $val['payment_status'] ?></td>
                        </tr>
                        <tr>
                            <td>requestor_id</td>
                            <td><?= $val['requestor_id'] ?></td>
                        </tr>
                        <tr>
                            <td>start_time</td>
                            <td><?= $val['start_time'] ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>       
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>       
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <?php echo '<span style="color:#FFF;text-align:center;"><p>hello</p></span>'; ?>
        <button onclick="myFunction()">Booking Now!</button>
        <script>
        function myFunction() {
            var x = document.getElementById("myDIV");
            if (x.style.display === "block") {
                x.style.display = "none";
            } else {
                x.style.display = "block";
            }

        }
        </script>
    <?php endif; ?>
</body>
</html>
