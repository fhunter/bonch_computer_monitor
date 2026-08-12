%include('header')
%import settings
%import tpl_utils
<table border=1>
    <tr>
        <th>Ключ</th>
        <th>Значение</th>
    </tr>
    <tr>
        <td>machineid</td>
        <td>{{machineid}}</td>
    </tr>
    <tr>
        <td>Последние данные</td>
        <td>{{computer.last_report}}</td>
    </tr>
    <tr>
        <td>Hostname</td>
        <td>{{computer.hostname}}</td>
    </tr>
    <tr>
        <td>IP</td>
        <td>{{computer.ip}}</td>
    </tr>
    <tr>
        <td>Комната</td>
        <td>
            {{room.name}}<br/>
            <form method="post">
            <select name="room" id="room" required=true>
%for i in rooms:
%selected=""
%if i.id == room.id:
%selected="selected=true"
%end
                <option value={{i.id}} {{selected}}>{{i.name}}</option>
%end            
            </select>
            <input type="submit" value="Обновить">
            </form>
        </td>
    </tr>
</table>
<hr/>
<a href="{{settings.PREFIX}}/"><button>Назад</button></a>
%include('footer')
