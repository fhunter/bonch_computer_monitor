%include header_graphs
<h1>Графики для группы </h1>
        <div class="chartRangeControl">
            <form>
                <div>
                    <span class="timerange_control custom">
                        <img src="/jarmon/assets/icons/calendar.png" width="16" height="16" alt="calendar" class="from_custom"
                             title="Click to choose a custom start date" />
                        <input name="from_custom" type="text" readonly="readonly"
                               title="Time range start" />
                        <img src="/jarmon/assets/icons/calendar.png" width="16" height="16" alt="calendar" class="to_custom"
                             title="Click to choose a custom end date" />
                        <input name="to_custom" type="text" readonly="readonly"
                               title="Time range end" />
                    </span>
                    <span class="timerange_control standard">
                        <select name="from_standard"
                                title="Time range shortcuts - click to select an alternative time range" >
                        </select>
                    </span>
                    <input name="from" type="hidden"  />
                    <input name="to" type="hidden"  />
                    <select name="tzoffset"
                            title="Timezone offset - click to choose a custom timezone offset" ></select>
                    <input name="action" value="Update" type="button"
                           title="Graph update - click to update all graphs" />
                </div>
                <div class="range-preview"
                     title="Time range preview - click and drag to select a custom timerange" ></div>
            </form>
        </div>
<br/>
	<script type="text/javascript" src="../graph.js?attribute={{attr}}&isgroup={{group}}"></script>
        <script type="text/javascript">
        $(function() {
            jarmon.buildTabbedChartUi(
                $('.chart-container').remove(),
                jarmon.CHART_RECIPES_COLLECTD,
                $('.tabbed-chart-interface'),
                jarmon.TAB_RECIPES_STANDARD,
                $('.chartRangeControl')
            );
        });
        </script>
	<br/>
        <div class="tabbed-chart-interface"></div>
        <div class="chart-container">
            <div class="chart-header">
                <h2 class="title"></h2>
            </div>
            <div class="error"></div>
            <div class="chart"></div>
            <div class="graph-legend"></div>
        </div>

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
