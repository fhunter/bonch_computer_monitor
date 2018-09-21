%include header_graphs
<h1>Графики для {{machine}}</h1>
%include menu

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
