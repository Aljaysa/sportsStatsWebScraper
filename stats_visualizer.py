import mpld3
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class ScatterplotInfo:
    xData: list[float]
    yData: list[float]
    xLabel: str 
    yLabel: str
    graphTitle: str 
    legendNames: list[str]

    

def makeScatterplotHTML(scatterplotInfo: ScatterplotInfo):
    fig, ax = plt.subplots()
    colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#c0392b', '#ecf0f1', '#95a5a6', '#e74c3c', 'blue', '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#34495e', '#f39c12', '#95a5a6']
    colors = colors[:len(scatterplotInfo.xData)]
    #ax.scatter(xData, yData, c=colors, label=legendNames)
    
    for x,y,name,color in zip(scatterplotInfo.xData,scatterplotInfo.yData,scatterplotInfo.legendNames,colors):
        ax.scatter(x, y, c=color, label=name)
        
    ax.set_xlabel(scatterplotInfo.xLabel, fontsize=15)
    ax.set_ylabel(scatterplotInfo.yLabel, fontsize=15)
    ax.set_title(scatterplotInfo.graphTitle)

    ax.grid(True)
    ax.legend(scatterplotInfo.legendNames)
    fig.tight_layout()
    # def hover(event):
    #     ind = event.ind
    #     print(ind)
    # fig.canvas.mpl_connect('pick_event', hover)
    # plt.ion
    # fig.savefig("stats.svg")

    return mpld3.fig_to_html(fig)
        
