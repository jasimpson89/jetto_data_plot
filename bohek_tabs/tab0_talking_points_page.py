import panel as pn
pn.extension()


def markdown_talking_points(input_data):

    TALKING_POINTS = input_data

    pane = (pn.pane.Markdown(TALKING_POINTS))
    text = pn.Row(pane)

    return text
