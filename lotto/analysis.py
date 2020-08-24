import pandas as pd
import downloader
import sys
import os
from itertools import combinations
import numpy as np
import random
import warnings


class MyAnalysis():
    """
    Engine for calculate the best numbers
    """
    def __init__(self):
        """Initialize df variable as a new empty dataframe"""
        self.df = pd.DataFrame()
        self.df_extra = pd.DataFrame()
        pd.set_option('mode.chained_assignment', None)
        warnings.filterwarnings('ignore')

    def process_input(self):
        """Read csv file"""
        # read data.csv file, select last 7 columns
        self.df = pd.read_csv(downloader.get_from_config('csv_file_name'),
                              delimiter=";",
                              usecols=[27, 28, 29, 30, 31, 32, 33],
                              names=['N1', 'N2', 'N3', 'N4', 'N5', 'E1', 'E2'])

    def split_extra_numbers(self):
        """split extra numbers into a new dataframe"""
        # Copy extra numbers to a new dataframe
        self.df_extra = self.df[['E1', 'E2']].copy()
        # Remove extra numbers columns
        self.df = self.df.drop(columns=['E1', 'E2'])
        # Sum by rows for extra numbers
        self.df_extra['Sum of rows'] = self.df_extra.sum(axis=1)


    def odd_even_calculation_extra(self):
        """
        Calculate Odd/Even numbers by every single draw
        :return: stat_odd_even, occurence_odd_even
        """
        # Odd-Even calculation by rows (in the original order)
        def odd_even_func(row):
            return "".join(str(row[0] % 2) + str(row[1] % 2))

        self.df_extra['Odd(1) Even(0)'] = self.df_extra
                                                    .apply(odd_even_func, axis=1)
        # Put the statistics of how many Odd and Even number pair drawn, Series
        stat_odd_even_extra = self.df_extra.groupby('Odd(1) Even(0)') \
            .size().sort_values(ascending=False)\
            .to_frame(name="Odd(1) Even(0) statistic")
        # summarize of occurence of odd-even pairs

        def sort_values_func(row):
            return "".join(sorted([*row]))

        # sort strings like "01011" in rows then count them
        occurence_odd_even_extra = self.df_extra['Odd(1) Even(0)'] 
                                            .apply(sort_values_func) 
                                            .to_frame().groupby('Odd(1) Even(0)') 
                                            .size()
                                            .to_frame(name="Odd(1) Even(0) occurence")
        return stat_odd_even_extra, occurence_odd_even_extra


    def high_low_calculation_extra(self):
        """
        Calculate high and low numbers by draw, create new column
        """

        # Count high-low numbers
        def high_low_calc_func(row):
            whigh, wlow = 0, 0
            for i in range(2):
                if row[i] <= 4:
                    wlow += 1
                else:
                    whigh += 1
            return whigh, wlow


        #Convert tuple to string
        def format_column(row):
            return ",".join([str(row[0]), str(row[1])])

        # Create new column and put how many high-low numbers are by drawn
        self.df_extra['High-Low numbers'] = \
            self.df_extra.iloc[:, :2].apply(high_low_calc_func, axis=1)
        #self.df_extra['High-Low numbers'] = \
            #self.df_extra['High-Low numbers'].apply(format_column)


    def sum_calculation_extra(self):
        """Sum numbers, create new column"""
        # Sum E1 and E2 by rows
        self.df_extra['Sum of rows'] = self.df_extra.iloc[:, :2].sum(axis=1)


    def print_best_template_extra(self):
        """
        Gives back only rows with best template
        :return: dataframe
        """
        extra_numbers = \
            pd.DataFrame([i for i in combinations(range(1, 11), 2)], \
                         columns=['E1', 'E2'])
        mask1 = extra_numbers['E1'] % 2 != 0
        mask2 = extra_numbers['E2'] % 2 == 0
        return extra_numbers[mask1 & mask2].reset_index().drop(columns='index')

    # Odd-Even calculation by rows (in the original order)
    def odd_even_func(self, row):
        return "".join(str(row[0] % 2) + str(row[1] % 2) + \
                        str(row[2] % 2) + str(row[3] % 2) + str(row[4] % 2))


    # summarize of occurence of odd-even pairs and sort them
    def sort_values_func(self, row):
        return "".join(sorted([*row]))

    def odd_even_calculation(self):
        """
        Calculate Odd/Even numbers by every single draw
        :return: stat_odd_even, occurence_odd_even
        """
        self.df['Odd(1) Even(0)'] = self.df.apply(self.odd_even_func, axis=1)
        # Put the statistics of how many Odd and Even number pair drawn, Series
        stat_odd_even = self.df.groupby('Odd(1) Even(0)') \
            .size().sort_values(ascending=False)\
            .to_frame(name="Odd(1) Even(0) statistic")
        """
        Odd(1) Even(0)
        10110    13
        01010    13
        10100    13
        10010    13
        10000    13
        10111    12
        10001    12
        """


        # sort strings like "01011" in rows then count them
        occurence_odd_even = self.df['Odd(1) Even(0)'] \
                                    .apply(self.sort_values_func) \
                                    .to_frame().groupby('Odd(1) Even(0)') \
                                    .size()\
                                    .to_frame(name="Odd(1) Even(0) occurence")
        """
        Odd(1) Even(0)
        00000      9
        00001     39
        00011    103
        00111     81
        01111     50
        11111      7
        """
        return stat_odd_even, occurence_odd_even


    def high_low_calc_func(self, row):
        whigh, wlow = 0, 0
        for i in range(len(row)):
            if row[i] <= 25:
                wlow += 1
            else:
                whigh += 1
        return whigh, wlow


    #Convert tuple to string
    def format_column(self, row):
        return ",".join([str(row[0]), str(row[1])])


    def high_low_calculation(self):
        """
        Calculate high and low numbers by draw, create new column
        """
        # Create new column and put how many high-low numbers are by drawn
        self.df['High-Low numbers'] = \
            self.df.iloc[:, :5].apply(self.high_low_calc_func, axis=1)
        self.df['High-Low numbers'] = \
            self.df['High-Low numbers'].apply(self.format_column)
        return self.df.groupby('High-Low numbers').size()\
                                    .sort_values(ascending=False) \
                                    .to_frame(name='High-Low numbers statistic')

    def sum_calculation(self):
        """Sum numbers, create new column"""
        # Sum by rows
        self.df['Sum of rows'] = self.df.sum(axis=1)


    def print_best_template(self):
        """
        Gives back only rows with best template
        :return: dataframe
        """
        mask1 = (self.df['N1'] >= 1) & (self.df['N1'] <= 9)
        mask2 = (self.df['N2'] >= 10) & (self.df['N2'] <= 19)
        mask3 = (self.df['N3'] >= 20) & (self.df['N3'] <= 29)
        mask4 = (self.df['N4'] >= 30) & (self.df['N4'] <= 39)
        mask5 = (self.df['N5'] >= 40) & (self.df['N5'] <= 50)
        return self.df[mask1 & mask2 & mask3 & mask4 & mask5]


    def generate_numbers(self):
        df = self.count_drawn_numbers()
        a, b, c = list(df[:17].index), list(df[17:34].index), \
                                                        list(df[34:].index)
        a = random.sample(a, 5)
        b = random.sample(b, 5)
        c = random.sample(c, 5)
        df = pd.DataFrame(combinations(a + b + c, 5), \
                                        columns=['N1', 'N2', 'N3', 'N4', 'N5'])
        df = pd.DataFrame(np.sort(df.to_numpy(), axis=1), \
                          columns=['N1', 'N2', 'N3', 'N4', 'N5'])
        df['High-Low numbers'] = \
                df.apply(self.high_low_calc_func, axis=1)
        df['High-Low numbers'] = \
                df['High-Low numbers'].apply(self.format_column)
        df['Odd(1) Even(0)'] = df.apply(self.odd_even_func, axis=1)
        df['Odd(1) Even(0)'] = df['Odd(1) Even(0)'].apply(self.sort_values_func)
        df['Sum'] = df.sum(axis=1)
        mask1 = (df['Odd(1) Even(0)'] == '00111')
        mask2 = (df['High-Low numbers'] == '2,3')
        mask3 = (df['High-Low numbers'] == '3,2')
        mask4 = (df['Sum'] < 130)
        mask5 = (df['Sum'] > 118)
        df2 =  df[mask1 & mask4 & mask5]
        return df2[mask2 | mask3]


    def count_drawn_numbers(self):
        return pd.DataFrame(dict({'A' : list(self.df['N1']) +
                                list(self.df['N2']) + list(self.df['N3']) + \
                                list(self.df['N4']) + list(self.df['N5'])})) \
                                ['A'].value_counts()\
                                    .to_frame(name='Occurences of numbers')


# print(df.iloc[:,:5])
