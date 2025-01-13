%include header
<h1>Поиск пользовательских сессий</h1>
%include menu
%import datetime
%import settings
%import tpl_utils
<a href="{{settings.PREFIX}}/"><button>Назад</button></a>
<br/>
<form method="post" action="{{settings.PREFIX }}/search/user/" name="usersearch">
<table>
<tr>
<td><label for="usernm">Имя пользователя:</label></td>
<td align=right><input type="string" id="usernm" name="usernm" value="{{username}}"/></td>
</tr>
<tr>
<td><label for="computername">Имя компьютера:</label></td>
<td align=right><input type="string" id="computername" name="computername" value="{{computername}}"/></td>
</tr>
<tr>
<td><label for="startdate">Начальная дата:</label></td>
<td align=right><input type="date" id="startdate" name="startdate" value="{{startdate}}" min="1970-01-01" max="2077-12-31"/></td>
</tr>
<tr>
<td><label for="enddate">Конечная дата:</label></td>
<td align=right><input type="date" id="enddate" name="enddate" value="{{enddate}}" min="1970-01-01" max="2077-12-31"/></td>
</tr>
</table>
<input type="submit" value="Поиск">
</form>
<br/>
%if defined('query'):
<h2>Результаты поиска пользователи:</h2>
<table border=1>
<tr><th>Компьютер</th><th>Пользователь</th><th>Начало</th><th>Конец</th><th>Длительность</th></td>
%for i in query:
<tr><td>{{i[1].hostname}}</td><td>{{i[0].username}}</td><td>{{i[0].session_start}}</td><td>{{i[0].session_end}}</td>
<td>
%if i[0].session_end:
    {{i[0].session_end - i[0].session_start}}
%else:
    {{datetime.datetime.now() - i[0].session_start}}
%end
</td></tr>
%end
</table>
%end

%include footer
