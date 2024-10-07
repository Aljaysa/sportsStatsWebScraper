import mpld3
import matplotlib.pyplot as plt

class StatsVisualizer():
    
    
    @staticmethod
    def makeScatterplotHTML(xData, yData, xLabel, yLabel, graphTitle, legendNames):
        fig, ax = plt.subplots()
        colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#c0392b', '#ecf0f1', '#95a5a6', '#e74c3c', 'blue', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#34495e', '#f39c12', '#95a5a6']
        colors = colors[:len(xData)]
        #ax.scatter(xData, yData, c=colors, label=legendNames)
        
        for x,y,name,color in zip(xData,yData,legendNames,colors):
            ax.scatter(x, y, c=color, label=name)
            
        ax.set_xlabel(xLabel, fontsize=15)
        ax.set_ylabel(yLabel, fontsize=15)
        ax.set_title(graphTitle)

        ax.grid(True)
        ax.legend(legendNames)
        fig.tight_layout()
        # def hover(event):
        #     ind = event.ind
        #     print(ind)
        # fig.canvas.mpl_connect('pick_event', hover)
        # plt.ion
        # fig.savefig("stats.svg")

        return mpld3.fig_to_html(fig)
        