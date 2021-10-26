import io
import base64
import numpy as np
import matplotlib.pyplot as plotter


def save(obj):
    buffer = io.BytesIO()
    obj.savefig(buffer, format='png')
    obj.clf()
    obj.close()
    buffer.seek(0)
    fig_png = base64.b64encode(buffer.getvalue())
    data = str(fig_png, 'utf-8')
    buffer.close()
    return data


def picture(wedgeLables, ngramPercent, type='pie'):
    figureObject, axesObject = plotter.subplots(figsize=(10, 5), ncols=2)
    ax1, ax2 = axesObject.ravel()

    if type.lower() == 'pie':
        explode = (0, 0.1, 0.1)
        patches, texts, autotexts = ax1.pie(ngramPercent,
                                             labels=wedgeLables,
                                             shadow=True,
                                             frame=True,
                                             explode=explode,
                                             startangle=60,
                                             autopct='%.1f%%',
                                             wedgeprops={
                                                 'linewidth': 1,
                                                 'edgecolor': 'orange'
                                             }

                                             )


        ax1.axis('off')
        ax1.set_title("Compare summary graph", loc='center')
        ax2.axis('off')
        ax2.legend(patches, wedgeLables, loc='upper left')

    elif type == 'bar':
        patches = ax1.bar(
            range(len(ngramPercent)),
            ngramPercent,
            tick_label=wedgeLables,
            width=0.4,
            alpha=0.8,
            align='center'
        )
        patches[0].set_color('g')
        patches[1].set_color('r')
        patches[2].set_color('orange')

        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        for x, y in enumerate(ngramPercent):
            ax1.text(x, y + 0.1, '%s' % y, ha='center', va='bottom', fontsize=10)

        ax1.set_title('Compare summary graph', loc='center')
        ax2.axis('off')
        ax2.legend(patches, wedgeLables, loc='upper center')
    else:
        raise ValueError('仅支持pie（饼状图）和bar（柱状图）')
    data = save(plotter)
    return data
