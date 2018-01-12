%include header
<h1>Статус компьютеров</h1>
%include menu
Сегодня: {{date}}
<br/>
Включено компьютеров: {{online}}
<br/>

%for key,value in data.items():
<h2><a href="./group/{{value['link']}}">{{value['name']}}</a></h2>
<table border=1>
<tr>
<th>№</th><th>IP</th><th>Hostname<br/>по DNS</th>
<th>Последнее обновление<br/>(GMT)</th><th>Время<br/>с последнего обновления<br/>минут</th><th>Статус</th><th>Пользователи<br/>(за 10 минут)</th>
</tr>
%online = 0
%for i in value["values"]:
<tr>
<td>{{i[0]}}</td>
<td><a href=./computer/{{i[2]}}>{{i[1]}}</a></td>
<td>{{i[2]}}</td>
<td>{{i[3]}}</td>
<td>{{i[4]}}</td>
<td>
%if i[4] < 5:
<font color="green">Online</font>
%online = online + 1
%elif i[4] < 10:
%online = online + 1
<font color="orange">Delay</font>
%else:
<font color="grey">Offline</font>
%end
</td>
<td>
%if i[1] in userslog:
{{userslog[i[1]]}}
%end
</td>
</tr>
%end
<tr><td colspan=7><hr/></td></tr>
<tr><td colspan=2></td><td>Всего:</td><td>{{value["total"]}}</td><td>Включено:</td><td>{{online}}</td></tr>
</table>
%end
%include footer
