import os
import csv
import math


def extract_from_file(file_path):
    result = []
    with open(file_path) as f:
        file_lines = f.readlines()
        for i in range(0, len(file_lines)):
            if 'Round' in file_lines[i]:
                round = file_lines[i].split()[-1]
                weighted_sum = file_lines[i+1].split()[-1]
                avg_response_time = file_lines[i+2].split()[-1]
                evolution_cost = file_lines[i+3].split()[-1]
                result.append((round, weighted_sum, avg_response_time, evolution_cost))
    return result


def extract_from_result_dir(dir_path):
    result_dict = {}
    for result_file_name in os.listdir(dir_path):
        # file name example: nsgaii-2500-400-200-false-false.log
        print(result_file_name)
        split_r = result_file_name.split('-')
        if len(split_r) != 6:
            continue
        if split_r[0] not in result_dict:
            result_dict[split_r[0]] = {}

        if split_r[4] not in result_dict[split_r[0]]:
            result_dict[split_r[0]][split_r[4]] = {}

        result_dict[split_r[0]][split_r[4]][split_r[1]] = extract_from_file(os.path.join(dir_path, result_file_name))
    return result_dict


def result_to_csv(result_dict, csv_file_path):
    headers = ['user',
               'nsgaii-false-ws',
               'nsgaii-false-avgT',
               'nsgaii-false-eCost',
               'nsgaii-true-ws',
               'nsgaii-true-avgT',
               'nsgaii-true-eCost',
               'wsga-false-ws',
               'wsga-false-avgT',
               'wsga-false-eCost',
               'wsga-true-ws',
               'wsga-true-avgT',
               'wsga-true-eCost',
               'moead-false-ws',
               'moead-false-avgT',
               'moead-false-eCost',
               'moead-true-ws',
               'moead-true-avgT',
               'moead-true-eCost',
               ]
    with open(csv_file_path, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        user_size_list = sorted([x for x in result_dict['nsgaii']['false']])
        for user_size in user_size_list:
            user_size = str(user_size)
            nsgaii_false_r = get_min_wsum(result_dict['nsgaii']['false'][user_size])
            nsgaii_true_r = get_min_wsum(result_dict['nsgaii']['true'][user_size])
            wsga_false_r = get_min_wsum(result_dict['wsga']['false'][user_size])
            wsga_true_r = get_min_wsum(result_dict['wsga']['true'][user_size])
            moead_false_r = get_min_wsum(result_dict['moead']['false'][user_size])
            moead_true_r = get_min_wsum(result_dict['moead']['true'][user_size])
            row = [
                user_size,
                nsgaii_false_r[1],
                nsgaii_false_r[2],
                nsgaii_false_r[3],
                nsgaii_true_r[1],
                nsgaii_true_r[2],
                nsgaii_true_r[3],
                wsga_false_r[1],
                wsga_false_r[2],
                wsga_false_r[3],
                wsga_true_r[1],
                wsga_true_r[2],
                wsga_true_r[3],
                moead_false_r[1],
                moead_false_r[2],
                moead_false_r[3],
                moead_true_r[1],
                moead_true_r[2],
                moead_true_r[3],
            ]
            f_csv.writerow(row)


def get_converge_csv(result_info_dict, size, csv_file_path):
    headers = ['round', 'nsgaii-false', 'nsgaii-true', 'wsga-false', 'wsga-true', 'moead-false', 'moead-true']
    last_row = None
    with open(csv_file_path, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for round in range(0, len(result_info_dict['nsgaii']['false'][size])):
            if not last_row:
                row = [
                    round+1,
                    result_info_dict['nsgaii']['false'][size][round][1],
                    result_info_dict['nsgaii']['true'][size][round][1],
                    result_info_dict['wsga']['false'][size][round][1],
                    result_info_dict['wsga']['true'][size][round][1],
                    result_info_dict['moead']['false'][size][round][1],
                    result_info_dict['moead']['true'][size][round][1],
                ]
            else:
                row = [
                    round+1,
                    min(result_info_dict['nsgaii']['false'][size][round][1], last_row[1]),
                    min(result_info_dict['nsgaii']['true'][size][round][1], last_row[2]),
                    min(result_info_dict['wsga']['false'][size][round][1], last_row[3]),
                    min(result_info_dict['wsga']['true'][size][round][1], last_row[4]),
                    min(result_info_dict['moead']['false'][size][round][1], last_row[5]),
                    min(result_info_dict['moead']['true'][size][round][1], last_row[6]),
                ]
            last_row = row
            f_csv.writerow(row)


def get_min_wsum(r_list):
    r = r_list[0]
    for r_l in r_list:
        if r[1] > r_l[1]:
            r = r_l
    return r


if __name__ == '__main__':
    r = extract_from_result_dir('/home/hexiang/workspace/idea/run/vizualization/common')
    result_to_csv(r, '/home/hexiang/workspace/idea/run/common.csv')
    # get_converge_csv(r, '3000', '/home/hexiang/workspace/idea/run/3000-converge.csv')