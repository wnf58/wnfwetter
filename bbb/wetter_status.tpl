<html>
<head>
    <title>{{title or 'No title'}}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta http-equiv="refresh" content="60">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, user-scalable=yes"/>

    <link href="./img/favicon.ico" rel="icon" type="image/x-icon"/>
    <link href="./img/favicon.ico" rel="shortcut icon" type="image/x-icon"/>
    <!-- erstellt von https://www.ionos.de/tools/favicon-generator -->
    <link rel="apple-touch-icon" sizes="57x57" href="./img/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="./img/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="./img/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="./img/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="./img/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="./img/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="./img/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="./img/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="./img/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192" href="./img/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="./img/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="./img/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="./img/favicon-16x16.png">
    <link rel="manifest" href="./manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="/img/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">

    <link rel="stylesheet" href="./css/ls_status.css"/>
    <script src="./js/we_status.js" type="text/javascript"></script>

</head>
<body>
<div class="bg-div">
    <img class="logo-img" height="40" alt="dsp-logo" src="./img/wetter_logo.png"/>
    <div class="logo-text">wnf Wetterserver</div>
</div>
<hr/>
<div class="AktuelleTemeratur">{{AktuelleTemperatur}}</div>
<hr/>
<table>
    %for row in WetterStatus:
    <tr>
        %for col in row:
        <td>{{col}}</td>
        %end
    </tr>
    %end
    <tr><td><a href="./100">Die letzten 100 Werte</a></td><td><a href="./24h">Die letzten 24 Stunden</a></td></tr>
    <tr><td><a href="./48h">Die letzten 48 Stunden</a></td><td><a href="./07d">Die letzten 7 Tage</a></td></tr>
    <tr><td><a href="./28d">Die letzten 4 Wochen</a></td><td><a href="./">Liste aller Werte</a></td></tr>
</table>
<hr/>
<h3>{{WetterCount}} Wetterdaten</h3>
<table>
    <tr>
        %for col in WetterKopf:
        <th>{{col}}</th>
        %end
    </tr>
    %for row in WetterDaten:
    <tr>
        %for col in row:
        <td>{{col}}</td>
        %end
    </tr>
    %end
</table>
<hr/>
</body>