%include header
%import settings
%import tpl_utils
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

%def myfunc(e):
%return e[1]
%end
<h2> Использование за {{tpl_utils.period_to_days(period)}} дней</h2>
<table border=1>
<thead>
<tr>
%for i in hosts:
<th>
{{i.hostname}}
</th>
%end
</tr>
<tr>
</tr>
</thead>
<tr>
%for i in hosts:
<td valign=top>
	<table border=1>
	<thead>
	<tr>
	<th>Пользователь</th><th>минуты</th>
	<tr>
	</thead>
	%popularity[i.hostname].sort(reverse=True,key=myfunc)
	%for k in popularity[i.hostname]:
	<tr>
	<td>{{k[0]}}</td><td>{{k[1]}}</td>
	</tr>
	%end
	</table>
</td>
%end
</tr>
</table>
%include footer
