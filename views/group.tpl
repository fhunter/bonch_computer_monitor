%include header_graphs
<h1>Графики для группы {{attr}}</h1>

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
{{i[0]}}
</td>
%for j in [7,14,30,60,90,180]:
<td valign=top>
	<table border=1>
	<thead>
	<tr>
	<th>Пользователь</th><th>минуты</th>
	<tr>
	</thead>
	%popularity[i[0]][j].sort(reverse=True,key=myfunc)
	%for k in popularity[i[0]][j]:
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
