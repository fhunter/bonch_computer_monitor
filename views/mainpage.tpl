%include header
<h1>Статус компьютеров</h1>
%include menu
%import datetime
%import settings
%import tpl_utils
Сегодня: {{date}}
<br/>
Включено компьютеров: {{online}}
<br/>

%for key,value in data.items():
<h2><a href="./group/{{value['link']}}">{{value['name']}}</a></h2>
<table border=1>
    <tr>
        <th rowspan=2>№</th><th rowspan=2>IP</th><th rowspan=2>Hostname<br/>по DNS</th>
        <th rowspan=2>Последнее обновление<br/>(GMT)</th><th rowspan=2>С последнего<br/> обновления<br/>чч:мм:сс</th>
        <th rowspan=2>Статус</th><th rowspan=2>Пользователи<br/>(за 10 минут)</th>
        <th colspan=3>Использование за месяц<br/> часов:минут:секунд</th>
        <th rowspan=2>Объём /scratch </th>
        <th rowspan=2>Отчёт<br/>Ansible</th>
    </tr>
    <tr>
        <th>Включён</th>
        <th>Использовался</th>
        <th>%</th>
    </tr>
%for i in value["values"]:
    <tr>
        <td>{{i[0]}}</td>
        <td><a href=./computer/{{i[10]}}>{{i[1]}}</a></td>
        <td>{{i[2]}}</td>
        <td>{{i[3]}}</td>
        <td align=right>{{str(datetime.timedelta(seconds=int(i[4]*60.0)))}}</td>
        <td>
            <font color="{{tpl_utils.time_to_color(i[4])}}">{{tpl_utils.time_to_online(i[4])}}</font>
        </td>
        <td>{{' '.join(userslog[i[10]])}}</td>
        <td align=right>{{str(datetime.timedelta(minutes=i[5]))}}</td>
        <td align=right>{{str(datetime.timedelta(minutes=i[6]))}}</td>
        <td align=right>{{tpl_utils.usage_percent(i[6],i[5])}}</td>
        <td>{{tpl_utils.scratch_data(i[8])}}</td>
        <td>{{! tpl_utils.ansible_data(i[7])}}</td>
    </tr>
%end
%online = len([i[4] for i in value["values"] if i[4] < 10])
    <tr><td colspan=13><hr/></td></tr>
    <tr><td colspan=2></td><td>Всего:</td><td>{{value["total"]}}</td><td>Включено:</td><td>{{online}}</td></tr>
</table>
%end
%include footer
