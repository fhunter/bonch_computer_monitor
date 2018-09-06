%include header
<h1>Статус компьютеров</h1>
%include menu
%import settings
Сегодня: {{date}}
<br/>
Включено компьютеров: {{online}}
<br/>

%for key,value in data.items():
<h2><a href="./group/{{value['link']}}">{{value['name']}}</a></h2>
<table border=1>
<tr>
<th>№</th><th>IP</th><th>Hostname<br/>по DNS</th>
<th>Последнее обновление<br/>(GMT)</th><th>Время<br/>с последнего<br/> обновления<br/>минут</th>
<th>Статус</th><th>Пользователи<br/>(за 10 минут)</th>
<th>Включен<br/>за месяц<br/>минут</th><th>Использовался<br/>за месяц<br/>минут</th>
<th>Процент<br/> использования</th>
<th>Отчёт<br/>Ansible</th>
</tr>
%online = 0
%for i in value["values"]:
<tr>
<td>{{i[0]}}</td>
<td><a href=./computer/{{i[2]}}>{{i[1]}}</a></td>
<td>{{i[2]}}</td>
<td>{{i[3]}}</td>
%import datetime
<td align=right>{{str(datetime.timedelta(seconds=int(i[4]*60.0)))}}</td>
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
<td align=right>
{{i[5]}}
</td>
<td align=right>
{{i[6]}}
</td>
<td align=right>
%if i[5] == 0:
0 %
%else:
<!--<img src={{settings.PREFIX}}image?full={{i[6]}}&use={{i[5]}} /> -->
{{int(100.0*i[6]/i[5])}} %
%end
</td>
<td>
%if i[7]:
{{i[7][0]}}
<font color="green">{{i[7][1]}}</font>
/
<font color="orange">{{i[7][2]}}</font>/
<font color="black">{{i[7][3]}}</font>/
<font color="red">{{i[7][4]}}</font>
%else:
N/A
%end
</td>
</tr>
%end
<tr><td colspan=11><hr/></td></tr>
<tr><td colspan=2></td><td>Всего:</td><td>{{value["total"]}}</td><td>Включено:</td><td>{{online}}</td></tr>
</table>
%end
%include footer
