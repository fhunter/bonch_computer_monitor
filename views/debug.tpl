<html>
<body>
<h1>Пользовательские сессии</h1>
%for i in users:
{{i}} </br>
%end
<h1>Комнаты</h1>
%for i in rooms
{{i}}</br>
%end
<h1>Сессии компьютеров</h1>
%for i in computers:
{{i}}</br>
%end
<h1>Компьютеры</h1>
%for i in computer:
{{i}} </br>
%end
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
