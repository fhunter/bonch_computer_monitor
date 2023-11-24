%include header
%import settings
<h1>Графики для {{machine}}</h1>
%include graph_menu path="computer/" + machine

<h2>Нагрузка на процессор</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu1/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu2/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu3/{{period}}>
<h2>Количество пользователей</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_users/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_lpu/{{period}}>
<h2>Свободное место на scratch</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_scratch/{{period}}>
<h2>Статус ansible</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_ansible/{{period}}>
<h2>Время работы</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_uptime/{{period}}>


<table border=1 width=75%>
<thead>
<tr>
<th>Дней</th><th>Пользователи</th>
</tr>
</thead>
%def myfunc(e):
%return e[1]
%end
%for i in [7,14,30,60,90,180]:
<tr><td>{{i}}</td>
<td valign=top>
	<table border=1 width=100%>
	<thead>
	<tr>
	<th>Пользователь</th><th>минуты</th>
	<tr>
	</thead>
	%popularity[i].sort(key=myfunc,reverse=True)
	%for k in popularity[i]:
	<tr>
	<td>{{k[0]}}</td><td>{{k[1]}}</td>
	</tr>
	%end
	</table>
</td></tr>
%end
</table>
%include footer
