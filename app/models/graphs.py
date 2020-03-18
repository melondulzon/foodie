import pygal
from pygal.style import LightenStyle
from app import db


class Graphs:

    # list of cuinas that I do not want to include in graphs
    unwanted_cuinas = ['north-african', 'english', 'cajun--creole', '']

    # ============================================ #

    @staticmethod
    def likes_chart():

        """
            Calculates the average likes and dislikes of each cuina group
        """

        # apply custom style to graph
        dark_blue_style = LightenStyle('#004466')

        # create chart type, labels, heading
        bar_chart = pygal.Bar(fill=True, interpolate='cubic', style=dark_blue_style, tooltip_border_radius=10, legend_at_bottom=True)
        bar_chart.title = 'Average Likes / Dislikes per cuina'
        bar_chart.x_labels = ['Likes', 'Dislikes']

        # query db for likes / dislikes and group by cuina
        cursor = db.recipes.aggregate([{"$group": {"_id": "$filters.cuina", "likes": {"$avg": '$users.likes'}, "dislikes": {"$avg": '$users.dislikes'}}}])

        # add a new bar to the graph for each group
        # dislikes are inverted for the bar chart visual aspect
        for item in cursor:
            if item['_id'] not in Graphs.unwanted_cuinas:
                bar_chart.add(item['_id'], [round(item['likes'], 0), round(item['dislikes'] * -1, 0)])

        # render as data uri
        return bar_chart.render_data_uri()

    # ============================================ #

    @staticmethod
    def kcal_chart():

        """
            Calculates the average kcal of each cuina group
        """

        # apply custom style to graph
        dark_blue_style = LightenStyle('#004466')

        # create chart type, labels, heading
        pie_chart = pygal.Pie(inner_radius=.4, fill=True, interpolate='cubic', style=dark_blue_style, tooltip_border_radius=10)
        pie_chart.title = 'Average KCAL per cuina'

        # nutrition is a 2d array and I had trouble with positional queries
        # For that reason two $project queries were used to unwind the 2d array
        cursor = db.recipes.aggregate([
            {"$project":
                {
                    "_id": "$filters.cuina",
                    "arr": {"$arrayElemAt": ["$nutrition", 0]}
                }
            },
            {"$project":
                {
                    "_id": "$_id",
                    "kcal": {"$arrayElemAt": ["$arr", 1]}
                }
            },
            {"$group": {
                "_id": "$_id",
                "avgKcal": {
                    "$avg": {
                        "$toInt": "$kcal"
                    }
                }
            }}
        ])

        # add a new pie section to the graph for each group
        for item in cursor:
            if item['_id'] not in Graphs.unwanted_cuinas:
                pie_chart.add(item['_id'], round(item['avgKcal'], 0), formatter=lambda x: '%s kcals' % x)

        # render as data uri
        return pie_chart.render_data_uri()
