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
        <th rowspan=2 colspan=2>Отчёт<br/>Ansible</th>
    </tr>
    <tr>
        <th>Включён</th>
        <th>Использовался</th>
        <th>%</th>
    </tr>
%for i in value["values"]:
    <tr>
        <td>{{i["id"]}}</td>
        <td><a href=./computer/{{i["machineid"]}}>{{i["ip"]}}</a></td>
        <td>{{i["hostname"]}}</td>
        <td>{{i["last_report"]}}</td>
        <td align=right>{{str(datetime.timedelta(seconds=int(i["since_update"]*60.0)))}}</td>
        <td>
            <font color="{{tpl_utils.time_to_color(i["since_update"])}}">{{tpl_utils.time_to_online(i["since_update"])}}</font>
        </td>
        <td>{{! '<br/>'.join(userslog[i["machineid"]])}}</td>
        <td align=right>{{str(datetime.timedelta(minutes=i["power_time"]))}}</td>
        <td align=right>{{str(datetime.timedelta(minutes=i["usage_time"]))}}</td>
        <td align=right>{{tpl_utils.usage_percent(i["usage_time"],i["power_time"])}}</td>
        <td>{{tpl_utils.scratch_data(i["scratch"])}}</td>
        <td>{{! tpl_utils.ansible_data(i["ansible"])}}</td>
        <td><font color="red">{{tpl_utils.is_ansible_ok(i["ansible"],i["last_report"])}}</font></td>
    </tr>
%end
%online = len([i["since_update"] for i in value["values"] if i["since_update"] < 10])
    <tr><td colspan=13><hr/></td></tr>
    <tr><td colspan=2></td><td>Всего:</td><td>{{value["total"]}}</td><td>Включено:</td><td>{{online}}</td></tr>
</table>
%end
%include footer
