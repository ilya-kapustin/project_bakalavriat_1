import pandas as pd
pd.options.mode.chained_assignment = None  # чтобы пандас не кидал ошибки во время преобразования фрейма


class AggregateException(Exception):
    pass


class Aggregator:

    @staticmethod
    def aggregate(data_frame, filter=None, columns=None, group_name=None, agg_name=None, as_index=True):
        if columns:
            if isinstance(columns, list):
                data_frame = data_frame[columns]
            else:
                raise AggregateException("Columns must be List")

        if filter:
            data_frame.query(filter, inplace=True)

        if group_name:
            if isinstance(group_name, list):
                data_frame = data_frame.groupby(by=group_name, as_index=as_index)
            else:
                raise AggregateException("agg_name is not dict {'col': ['min', 'max']} or group_name is not names list")

        if agg_name:
            if isinstance(agg_name, dict):
                data_frame = data_frame.agg(agg_name)
            else:
                raise AggregateException("agg_name is not dict {'col': ['min', 'max']} or group_name is not names list")

        return data_frame
