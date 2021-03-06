import os
import downloader
import analysis
from output_writer import write_to_xls_file as wxls
from datetime import datetime as dt
import time


def main():
    """Main function"""
    start_time = time.perf_counter()
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
            wxls(calc_session.print_best_template(), stat_odd_even,
                 calc_session.count_drawn_numbers(), occurence_odd_even,
                 calc_session.high_low_calculation(), stat_odd_even_extra,
                 occurence_odd_even_extra,
                 calc_session.print_best_template_extra(),
                 calc_session.generate_numbers()
                 )
        else:
            print(f"Error!{downloader.get_from_config('csv_file_name')} "
                  f"file couldn't be found.")
    end_time = time.perf_counter() - start_time
    if str(end_time)[0] == '0':
        print(f'Executed in {(end_time * 100):.3f} ms')
    else:
        print(f'Executed in {end_time:.3f} s')


if __name__ == '__main__':
    main()
