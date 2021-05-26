import matplotlib.pyplot as plt
import seaborn as sns
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import geopy
# from geopy.extra.rate_limiter import RateLimiter

plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('Set2')


# желательно знать, что рисует каждый график и какие данные принимает на входе
# тк если не правильно преобразованный датафрейм передать в функцию, то выдаст ошибку или отрисует не то, что надо
class Visual:

    def __init__(self, df, graph_number, save_path, file_name, form):
        self.df = df
        self.graph_number = graph_number

        self.save_path = save_path
        self.file_name = file_name
        self.form = form

    @staticmethod
    def save_image(save_path, figure, file_name, form):
        if save_path:
            figure.savefig(fr'{save_path}{file_name}.{form}')
        else:
            figure.savefig(fr'{file_name}.{form}')

    def barplot_(self, df, data_col, size=(25, 10),
                 fontsize_=16, labelsize_=14,
                 alp=0.5):

        count_plot = len(data_col)

        if count_plot > 1:
            figure, ax = plt.subplots(1, count_plot, sharey=True, figsize=size)
            for i, data in enumerate(data_col):
                sns.barplot(y=data[0], x=data[1], data=df, alpha=alp, ax=ax[i])
                ax[i].set_title(f'{data[1]}', fontsize=fontsize_)
        else:
            figure = plt.figure(figsize=size)
            plt.title(self.file_name, fontsize=fontsize_)
            plt.tick_params(labelsize=labelsize_)
            sns.barplot(y=df[data_col[0][0]], x=df[data_col[0][1]], alpha=alp)
            plt.show()

        if self.file_name:
            Visual.save_image(save_path=self.save_path, figure=figure, file_name=self.file_name, form=self.form)

    def stack_bar(self, df, size=(20, 15),
                  fontsize_=16, ylabel_=None,
                  xlabel_=None, stacked_=True,
                  title_size=18,
                  bbox_to_anchor_=(1.2, 1)):

        plt.figure(figsize=size)  # figure
        plot = df.plot.barh(
            figsize=size
            , fontsize=fontsize_
            , stacked=stacked_
            , title=self.file_name)
        plot.title.set_size(title_size)
        plot.legend(loc=1, bbox_to_anchor=bbox_to_anchor_, fontsize=fontsize_)
        plot.set(ylabel=ylabel_, xlabel=xlabel_)
        plt.show()

        if self.file_name:
            Visual.save_image(save_path=self.save_path, figure=plot.get_figure(),
                              file_name=self.file_name, form=self.form)

    def multi_bar(self, df, size=(20, 100), count=15,
                  fontsize_=18, rotation_=90):

        df = df.unstack(0)
        fig, ax = plt.subplots(count, 1, figsize=size)
        for i, elem in enumerate(df.columns):
            data_bar = df.iloc[:, i].dropna()
            ax[i].set_title(data_bar.name, fontsize=fontsize_)
            ax[i].set_xticklabels(data_bar.index, rotation=rotation_)
            ax[i].bar(data_bar.index, data_bar.values)
        plt.subplots_adjust(hspace=1)

        if self.file_name:
            Visual.save_image(save_path=self.save_path, figure=fig, file_name=self.file_name, form=self.form)

    def hist_(self, df, value, size=(10, 7), fontsize_=16):
        plt.rcParams['figure.figsize'] = size

        plt.title(self.file_name, fontsize=fontsize_)
        plot = df[value].hist()

        if self.file_name:
            Visual.save_image(save_path=self.save_path, figure=plot.get_figure(),
                              file_name=self.file_name, form=self.form)

    def distributions(self, df, value, size=(20, 10)):
        fig = plt.figure(figsize=size)
        sns.distplot(df[value])
        plt.show()

        if self.file_name:
            Visual.save_image(save_path=self.save_path, figure=fig, file_name=self.file_name, form=self.form)

    # -----------------------------------
    # def world_map(df, size=(40, 40), mark='o', linestyle_='', columns):
    #
    # 	fig = plt.figure(figsize=size)
    # 	ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    # 	for data in df[columns].values:
    # 		ax.plot(data[2][1], data[2][0],
    # 				marker=mark,
    # 				linestyle=linestyle_,
    # 				markersize=data[1],
    # 				label=data[0])
    # 		if data[1] > 15:
    # 			ax.text(x=data[2][1], y=data[2][0],
    # 					s=data[0],
    # 					color="red", fontsize=10)
    #
    # 	ax.stock_img()
    # 	ax.add_feature(cfeature.BORDERS)
    # 	ax.coastlines(resolution='110m')
    #
    # 	if self.file_name:
    #         Visual.save_image(save_path=self.save_path, figure=fig, title_=title_, form=form)
    # ---------------------------------------

    def run(self, params):

        if isinstance(params, list):
            if self.graph_number == 0:
                self.barplot_(df=self.df, data_col=params)
            else:
                raise Exception

        elif isinstance(params, str):
            if self.graph_number == 3:
                self.hist_(df=self.df, value=params)
            elif self.graph_number == 4:
                self.distributions(df=self.df, value=params)
            else:
                raise Exception

        else:
            if self.graph_number == 1:
                self.stack_bar(df=self.df)
            elif self.graph_number == 2:
                self.multi_bar(df=self.df)
            else:
                raise Exception


