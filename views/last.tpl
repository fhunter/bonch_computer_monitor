<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
</head>
<body>
%import datetime
<h1>Пользователи за {{ period / (24 * 60) }} дней</h1>
<a href=./d>День</a> <a href=./w>Неделя</a> <a href=./m>Месяц</a> <a href=./y>Год</a>
<h2>Суммарное время для всех пользовалей</h2>
{{ datetime.timedelta(minutes = sum([i[1] for i in users]) * 5) }} часов
<h2>Время залогиненное</h2>
<table border=1>
<tr><th>Пользователь</th><th>Время,<br/> часов</th></tr>
%for i in users:
<tr><td>{{ i[0] }}</td><td>{{ datetime.timedelta(minutes = i[1]*5) }} </td></tr>
%end
</table>
</body>
</html>
