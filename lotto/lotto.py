import os
import downloader
import analysis
from output_writer import write_to_xls_file as wxls
from datetime import datetime as dt


def main():
    """Main function"""
    start_time = dt.now()
    if downloader.download(downloader.get_from_config('url')) == 0:
        if os.path.exists(downloader.get_from_config('csv_file_name')):
            print(f'Analysing data...', end='')
            calc_session = analysis.MyAnalysis()
            calc_session.process_input()
            calc_session.split_extra_numbers()
            calc_session.high_low_calculation()
            calc_session.high_low_calculation_extra()
            stat_odd_even, occurence_odd_even = \
                                calc_session.odd_even_calculation()
            calc_session.sum_calculation()
            calc_session.sum_calculation_extra()
            stat_odd_even_extra, occurence_odd_even_extra = \
                calc_session.odd_even_calculation_extra()
            print(f'Done.')
            wxls(calc_session.print_best_template(), stat_odd_even, \
                 calc_session.count_drawn_numbers(), occurence_odd_even, \
                 calc_session.high_low_calculation(), stat_odd_even_extra, \
                 occurence_odd_even_extra, \
                 calc_session.print_best_template_extra(), \
                 calc_session.generate_numbers()
                 )
        else:
            print(f"Error!{downloader.get_from_config('csv_file_name')} file couldn't be found.")
    elapsed_time_seconds, elapsed_time_mseconds = (dt.now() - start_time).seconds, (dt.now() - start_time).microseconds
    print(f'Program executed within {" ".join([str(elapsed_time_seconds), "seconds"]) if elapsed_time_seconds != 0 else " ".join([str(elapsed_time_mseconds / 100), "miliseconds"])}.')
if __name__ == '__main__':
    main()
