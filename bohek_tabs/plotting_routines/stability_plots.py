import pandas as pd
import hvplot
import hvplot.pandas
import holoviews as hv
# hv.extension('bohek')
import numpy as np
import matplotlib.pyplot as plt
def make_dataframe_for_gradients(jsp):

    pre_grad = np.diff(jsp["PRE"].values) / np.diff(jsp["R"].values)
    te_grad = np.diff(jsp["TE"].values) / np.diff(jsp["R"].values)
    ne_grad = np.diff(jsp["NE"].values) / np.diff(jsp["R"].values)
    ti_grad = np.diff(jsp["TI"].values) / np.diff(jsp["R"].values)
    r = (jsp["R"])[0:-1]
    time = jsp["time"].values
    dict = {"R": r, "pre_grad": pre_grad,"te_grad":te_grad,"ne_grad":ne_grad,"ti_grad":ti_grad,"time":time}
    df = pd.DataFrame(dict)

    return df

def pressure_gradient(jetto_class):
    jsp, jsp_mishka = jetto_class["JSP"], jetto_class["JSP_mishka"]

    # unstable times
    unstable_times = (jsp_mishka.coords["time"])

    # select last three time slices
    jsp = jsp.sel(time=unstable_times[-3:])

    df_time1 = make_dataframe_for_gradients(jsp.isel(time=0))
    df_time2 = make_dataframe_for_gradients(jsp.isel(time=1))
    df_time3 = make_dataframe_for_gradients(jsp.isel(time=2))

    df_time1.append(df_time2,ignore_index=True)
    df_time1.append(df_time3,ignore_index=True)

    t1 = df_time1.hvplot(x="R",y=["pre_grad","te_grad","ne_grad"],hover_cols = ["pre_grad","te_grad","ne_grad"],label=jetto_class.label,
                              width=350, height=300, subplots=True, shared_axes=False,title='T minus 2',
                         line_color=jetto_class.color,legend='bottom').cols(3)

    t1["pre_grad"].opts(ylabel='pre grad')
    t1["te_grad"].opts(ylabel='te grad')
    t1["ne_grad"].opts(ylabel='ne grad')

    t2 = df_time2.hvplot(x="R", y=["pre_grad", "te_grad", "ne_grad"], label=jetto_class.label,
                              width=350, height=300, subplots=True, shared_axes=False,title='T minus 1',
                         line_color=jetto_class.color,legend='bottom').cols(3)

    t2["pre_grad"].opts(ylabel='pre grad')
    t2["te_grad"].opts(ylabel='te grad')
    t2["ne_grad"].opts(ylabel='ne grad')

    t3 = df_time3.hvplot(x="R", y=["pre_grad", "te_grad", "ne_grad"], label=jetto_class.label,
                              width=350, height=300, subplots=True, shared_axes=False,title='T minus 0',
                         line_color=jetto_class.color,legend='bottom').cols(3)

    t3["pre_grad"].opts(ylabel='pre grad')
    t3["te_grad"].opts(ylabel='te grad')
    t3["ne_grad"].opts(ylabel='ne grad')

    return t1,t2,t3



def make_j_alpha_plot(jetto_class,mishka_data):
    jst = jetto_class['JST']
    # Get out dataArrays from DataSet to make Pandas dataframe
    alpha_pd = jst['ALFM'].to_pandas()
    alpha_pd.name = 'ALFM'
    j_boot_pd = jst['CUBS'].to_pandas()
    j_boot_pd.name = 'CUBS'
    mishka_pd = jst['unstable_mode'].to_pandas()
    mishka_pd.name = 'unstable_mode'

    # Make dataframe, from dataabove.
    dataFrame = pd.concat([alpha_pd, j_boot_pd, mishka_pd], axis=1)

    alpha=dataFrame.hvplot.line(y='ALFM',hover_cols='unstable_mode',label=jetto_class.label,
                                line_color=jetto_class.color)
    j_bootstrap=dataFrame.hvplot.line(y='CUBS',hover_cols='unstable_mode',label=jetto_class.label,
                                      line_color=jetto_class.color)

    # Make vertical lines
    for time in (mishka_data["time"].values):

        alpha = alpha* hv.VLine(time)
        j_bootstrap = j_bootstrap*hv.VLine(time)

    return alpha,j_bootstrap

