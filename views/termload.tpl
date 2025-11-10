<html><head>
<base href="/online/" >
<meta http-equiv="Content-Type" content="text/html;charset=utf8">
<meta http-equiv="refresh" content="30" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head><body>
<table width=100%>
<tr><td width=*>Сервер</td><td width=30%>Load avg</td><td width=15% align=right>Пользователей</td></tr>
%for i in servers:
<tr>
    <td>{{i["name"]}}</td>
    <td align=right>{{i["load"][2]}}</td>
    <td align=right>{{i["users"]}}</td>
</tr>
%end
</table>
</body>
</html>
