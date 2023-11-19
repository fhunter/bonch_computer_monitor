<html>
<body>
<h1>Пользовательские сессии</h1>
{{users}} </br>
<h1>Комнаты</h1>
{{rooms}}
<h1>Сессии компьютеров</h1>
{{computers}}
<h1>Компьютеры</h1>
{{computer}}
<h1>Графики ansible</h1>
%for i in graphs:
<h2>{{i}}</h2>
<img src=../graph/{{i}}_ansible/w width=881 height=168 ><img src=../graph/{{i}}_cpu1/w  width=881 height=168></br>
<img src=../graph/{{i}}_scratch/w  width=881 height=168><img src=../graph/{{i}}_uptime/w  width=881 height=168></br>
<img src=../graph/{{i}}_users/w  width=881 height=168><img src=../graph/{{i}}_lpu/w  width=881 height=168></br>
<hr/>
%end
</body>
</html>
