<html><head>
<base href="/online/" >
<meta http-equiv="Content-Type" content="text/html;charset=utf8">
<meta http-equiv="refresh" content="30" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" type="text/css" href="style.css" />
</head><body>
<h1>Нагрузка на терминальные сервера</h1>
<table>
<tr><td>Сервер</td><td>Load avg</td><td>Пользователей</td></tr>
%for i in servers:
<tr><td>{{i["name"]}}</td><td>{{i["load"]}}</td><td>{{i["users"]}}</td></tr>
%end
</table>
</body>
</html>
