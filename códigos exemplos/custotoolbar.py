import numpy as np
import Tkinter as tk
import matplotlib as mpl
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

# custom toolbar with lorem ipsum text
class MyCustomToolbar(NavigationToolbar2Wx): 
    ON_CUSTOM_LEFT  = wx.NewId()
    ON_CUSTOM_RIGHT = wx.NewId()

    def __init__(self, plotCanvas):
        # create the default toolbar
        NavigationToolbar2Wx.__init__(self, plotCanvas)
        # add new toolbar buttons 
        self.AddSimpleTool(self.ON_CUSTOM_LEFT, _load_bitmap('stock_left.xpm'),
                           'Pan to the left', 'Pan graph to the left')
        wx.EVT_TOOL(self, self.ON_CUSTOM_LEFT, self._on_custom_pan_left)
        self.AddSimpleTool(self.ON_CUSTOM_RIGHT, _load_bitmap('stock_right.xpm'),
                           'Pan to the right', 'Pan graph to the right')
        wx.EVT_TOOL(self, self.ON_CUSTOM_RIGHT, self._on_custom_pan_right)

    # pan the graph to the left
    def _on_custom_pan_left(self, evt):
        ONE_SCREEN = 1
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = x2 - x1
        axes.set_xlim(x1 - ONE_SCREEN, x2 - ONE_SCREEN)
        self.canvas.draw()

    # pan the graph to the right
    def _on_custom_pan_right(self, evt):
        ONE_SCREEN = 1
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = x2 - x1
        axes.set_xlim(x1 + ONE_SCREEN, x2 + ONE_SCREEN)
        self.canvas.draw()

class MyApp(object):
    def __init__(self,root):
        self.root = root
        self._init_app()

    # here we embed the a figure in the Tk GUI
    def _init_app(self):
        self.figure = mpl.figure.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure,self.root)
        self.toolbar = CustomToolbar(self.canvas,self.root)
        self.toolbar.update()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.show()

    # plot something random
    def plot(self):
        self.ax.imshow(np.random.normal(0.,1.,size=[100,100]),cmap="hot",aspect="auto")
        self.figure.canvas.draw()

def main():
    root = tk.Tk()
    app = MyApp(root)
    app.plot()
    root.mainloop()

if __name__ == "__main__":
    main()