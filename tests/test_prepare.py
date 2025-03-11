import pandas as pd
import bar_chart_racer as bcr


class TestLoadData:
    """Test data loading functionality."""

    def test_load_urban_pop(self):
        """Test loading urban population dataset."""
        df = bcr.load_dataset('urban_pop')
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_covid(self):
        """Test loading COVID-19 dataset."""
        df = bcr.load_dataset('covid19')
        assert isinstance(df, pd.DataFrame)
        assert not df.empty


# Uncomment and update when test data is available
# class TestPrepareWideData:
#     """Test data preparation functionality."""

#     df_wide = pd.read_csv('tests/data/covid_test.csv', index_col='date', parse_dates=['date'])

#     def test_prepare_wide_data(self):
#         """Test wide data preparation."""
#         df_wide_values, df_wide_ranks = bcr.prepare_wide_data(self.df_wide)
#         df_wide_values_ans = pd.read_csv('tests/data/covid_test_values.csv',
#                                          index_col='date', parse_dates=['date'])
#         df_wide_ranks_ans = pd.read_csv('tests/data/covid_test_ranks.csv',
#                                         index_col='date', parse_dates=['date'])
#         pd.testing.assert_frame_equal(df_wide_values, df_wide_values_ans)
#         pd.testing.assert_frame_equal(df_wide_ranks, df_wide_ranks_ans)
