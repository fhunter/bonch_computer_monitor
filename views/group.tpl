%include header
%import settings
<h1>Графики для группы {{attr}}</h1>
%include graph_menu path="group/" + attr, period=period

<h2>Нагрузка на процессор</h2>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_cpu1/{{period}}"><br/>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_cpu3/{{period}}">
<h2>Количество пользователей</h2>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_users/{{period}}"><br/>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_lpu/{{period}}">
<h2>Свободное место на scratch</h2>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_scratch/{{period}}">
<h2>Статус ansible</h2>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_ansible/{{period}}">
<h2>Время работы</h2>
<img src="{{settings.PREFIX}}/graph/g/{{attr}}_uptime/{{period}}"><br/>

<table border=1>
<thead>
<tr>
<th rowspan=2>Компьютер</th><th colspan=4>Пользователи</th>
</tr>
<tr>
%def myfunc(e):
%return e[1]
%end
%for i in [7,14,30,60,90,180]:
<th>{{i}} дней</th>
%end
</tr>
</thead>
%for i in hosts:
<tr>
<td>
{{i.hostname}}
</td>
%for j in [7,14,30,60,90,180]:
<td valign=top>
	<table border=1>
	<thead>
	<tr>
	<th>Пользователь</th><th>минуты</th>
	<tr>
	</thead>
	%popularity[i.hostname][j].sort(reverse=True,key=myfunc)
	%for k in popularity[i.hostname][j]:
	<tr>
	<td>{{k[0]}}</td><td>{{k[1]}}</td>
	</tr>
	%end
	</table>
</td>
%end
</tr>
%end
</table>
%include footer
