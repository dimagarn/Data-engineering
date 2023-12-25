import os
import matplotlib.pyplot as plt
import seaborn as sns

SAMPLE_SIZE = 1000
PLOTS_DIRECTORY = 'plots'


def save_plot(plt, name):
    if not os.path.exists(PLOTS_DIRECTORY):
        os.makedirs(PLOTS_DIRECTORY)
    plt.savefig(os.path.join(PLOTS_DIRECTORY, f'{name}.png'))
    plt.close()


def plot_line(data, x, y, name):
    plt.title(name)
    sns.lineplot(data=data.sample(SAMPLE_SIZE), x=x, y=y, errorbar=None)
    save_plot(plt, name)


def plot_strip(data, x, y, name):
    plt.title(name)
    sns.stripplot(data=data.sample(SAMPLE_SIZE), x=x, y=y, dodge=True)
    save_plot(plt, name)


def plot_box(df, x, y, name):
    plt.title(name)
    sns.boxplot(data=df.sample(SAMPLE_SIZE), x=x, y=y)
    save_plot(plt, name)


def plot_hist(df, x, y, name):
    plt.title(name)
    sns.histplot(data=df.sample(SAMPLE_SIZE), x=x, y=y)
    save_plot(plt, name)