from motion_detector import df #importing dataframe from motion_detector module
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S") #create new column in strftime format
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


cds = ColumnDataSource(df)

p = figure(x_axis_type = "datetime", height = 100, width = 500, sizing_mode='scale_width', title = "Motion Graph")
p.yaxis.minor_tick_line_color = None
#p.ygrid[0].ticker.desired_num_ticks = 1 #clearing background horizontal grid lines in graph

hover = HoverTool(tooltips = [("Start", "@Start_string"), ("End", "@End_string")])
#creating hover window with Start column of csv and End column of csv
p.add_tools(hover) #adding hover window to p(graph)

q = p.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "Green", source = cds)

output_file(("Graph1.html"))
show(p)