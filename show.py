from pyecharts import options as opts
from pyecharts.charts import Bar
#柱状图的数据格式：x轴和y轴都是列表数据
#从mongodb中获取数据
x = getArea();
y= getAvgPrice();

def set_bar():
    #设置初始项，图表高width,宽height，以及网页的名称
    bar = Bar(init_opts=opts.InitOpts(width = '800px',height = '600px',page_title='柱状图'))
    #添加x轴数据
    bar.add_xaxis(xaxis_data = x)
    #添加y轴数据，加上series_name，表示图例
    bar.add_yaxis(series_name = '房价',y_axis = y)
    #设置全局项
    bar.set_global_opts(
        #设置图表主标题
        title_opts=opts.TitleOpts(title = '大连各地区二手房平均房价'),
        #添加坐标轴名称，位置以及大小，name_gap表示名称与x轴距离，font_size是字体大小
        xaxis_opts = opts.AxisOpts(name = '地区',name_location='center',name_gap=25,name_textstyle_opts=opts.TextStyleOpts(font_size = 15)),
        yaxis_opts = opts.AxisOpts(name = '房价(元/平)')
        )
    return bar

bar = set_bar()
#生成html文件
bar.render('柱状图.html')

from pyecharts import options as opts
from pyecharts.charts import Line

#折线图的数据格式：x轴和y轴都是列表数据
x = ['甘井子区','沙河口区','中山区','西岗区','高新区','开发区','金州区','旅顺口','普兰店','瓦房店']
y= [17977.41 ,17926.55 ,20316.50 ,17784.40 ,24974.40,11276.93,10089.91,8530.04 ,6487.92 ,7450.04 ]


def set_line():
    line = Line()
    line.add_xaxis(xaxis_data = x)
    #添加y轴数据，加上series_name，表示图例
    line.add_yaxis(series_name = '房价',y_axis = y)
    line.set_global_opts(
        #设置图例形状
        legend_opts=opts.LegendOpts(legend_icon='pin'),
        #设置图表主标题，副标题和标题位置
        title_opts=opts.TitleOpts(title = '大连各地区二手房平均房价'),
        #添加坐标轴名称，位置以及大小，name_gap表示名称与x轴距离，font_size是字体大小
        xaxis_opts = opts.AxisOpts(name = '地区',name_location='center',name_gap=25,name_textstyle_opts=opts.TextStyleOpts(font_size = 15)),
        yaxis_opts = opts.AxisOpts(name = '房价(元/平)')
        )
    return line

line = set_line()
line.render('折线图.html')

from pyecharts import options as opts
#导入Pie类
from pyecharts.charts import Pie

#饼图的数据类型，为列表的嵌套：[[key1, value1], [key2, value2]]
x = ['甘井子区','沙河口区','中山区','西岗区','高新区','开发区','金州区','旅顺口','普兰店','瓦房店']
y= [17977.41 ,17926.55 ,20316.50 ,17784.40 ,24974.40,11276.93,10089.91,8530.04 ,6487.92 ,7450.04 ]
#使用zip函数后
#再将其中的元组转换成列表
data_pair =  [list(i) for i in zip(x,y)]

def set_pie():
    pie = Pie()
    pie.add(
        series_name = '',
        data_pair = data_pair,
        color = 'red',
        #设置图表的标签(指示图表区域),formatter是设置标签内容格式，在饼图中：{a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
        label_opts = opts.LabelOpts(is_show=True,formatter='{b}:{c} \n ({d}%)'),
        # 是否展示成南丁格尔图，通过半径区分数据大小，有'radius'和'area'两种模式。
        # radius：扇区圆心角展现数据的百分比，半径展现数据的大小
        # area：所有扇区圆心角相同，仅通过半径展现数据大小
        rosetype = 'radius',
        # 饼图的半径，数组的第一项是内半径，第二项是外半径
        # 默认设置成百分比，相对于容器高宽中较小的一项的一半
        radius=['20%','75%']
    )
    pie.set_global_opts(
        #设置图例形状,位置,orient表示横向还是纵向，horizontal和vertical
        legend_opts=opts.LegendOpts(legend_icon='pin',orient='vertical',pos_right='10%'),
        #设置图表主标题，副标题和标题位置
        title_opts=opts.TitleOpts(title = '大连各地区二手房平均房价'),
    )
    #设置饼图的颜色，可选项，不设也有默认的颜色。
    pie.set_colors(['blue','red','orange','yellow','green','purple','black','brown','pink','grey'])
    return pie

pie = set_pie()
pie.render('饼图.html')

from pyecharts import options as opts
#导入Scatter类
from pyecharts.charts import Scatter

#散点图的数据类型：x轴和y轴结尾列表
#linspace(start,stop,num),在0-10中返回50个等间距的数
x = ['甘井子区','沙河口区','中山区','西岗区','高新区','开发区','金州区','旅顺口','普兰店','瓦房店']
y= [17977.41 ,17926.55 ,20316.50 ,17784.40 ,24974.40,11276.93,10089.91,8530.04 ,6487.92 ,7450.04 ]

def set_scatter():
    scatter = Scatter(init_opts=opts.InitOpts(width = '800px',height='600px',page_title='散点图'))
    #添加x轴数据
    scatter.add_xaxis(xaxis_data = x)
    #点的形状：symbol参数的取值：'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'
    scatter.add_yaxis(series_name = '房价(元/平)',y_axis = y,symbol='circle',label_opts=opts.LabelOpts(is_show=False))
    #为了让图更美观简洁，设置标签项不显示is_show = False
    scatter.set_global_opts(title_opts=opts.TitleOpts(title = '大连各地区二手房平均房价'),tooltip_opts=opts.TooltipOpts(trigger='axis',axis_pointer_type='cross'))
    return scatter

scatter = set_scatter()
scatter.render('散点图.html')