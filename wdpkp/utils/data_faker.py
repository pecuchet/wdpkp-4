import wdpkp.settings as settings


def get(date):
    import ast
    with open(settings.DIR + '/data_tmp/' + date + '/results-selection.log', 'r') as f:
        s = f.read()
        return ast.literal_eval(s)