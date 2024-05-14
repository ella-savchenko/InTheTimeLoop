import numpy as np
from datetime import datetime, timedelta
import csv
import pandas as pd
import os
import shutil

def analyse_case(file_name):

    case_a = []
    case_R1 = []
    case_R2 = []
    case_R3 = []
    case_R4 = []
    case_R5 = []
    case_R6 = []
    case_W1 = []
    case_W2 = []
    case_W3 = []

    log = open(file_name, "r", encoding='utf-8', errors='ignore')


    a = []
    R1 = []
    R2 = []
    R3 = []
    R4 = []
    R5 = []
    R6 = []
    W1 = []
    W2 = []
    W3 = []

    a_b = False
    next_a = False
    R1_b = False
    R2_b = False
    R3_b = False
    R4_b = False
    R5_b = False
    R6_b = False
    W1_b = False
    W2_b = False
    W3_b = False



    iterations = 0

    start_date = ""
    end_date = ""


    for line in log:
        line.strip()

        if "CET 202" in line:
            if start_date == "":
                start_date = line
            end_date = line


        if "End Iteration" in line:
            iterations += 1

        #last A
        if(next_a):
            a.append(line.strip())
            next_a = False
            a_b = False
            case_a.append(a)
            a = []

        if "done search grep R B1" in line:
            R1_b = False
            case_R1.append(R1)
            R1 = []

        if "done search grep R B2" in line:
            R2_b = False
            case_R2.append(R2)
            R2 = []

        if "done search grep R B3" in line:
            R3_b = False
            case_R3.append(R3)
            R3 = []


        if "done search grep R B4" in line:
            R4_b = False
            case_R4.append(R4)
            R4 = []

        if "done search grep R B5" in line:
            R5_b = False
            case_R5.append(R5)
            R5 = []

        if "done search grep R B6" in line:
            R6_b = False
            case_R6.append(R6)
            R6 = []

        if "done search grep A C1" in line:
            W1_b = False
            case_W1.append(W1)
            W1 = []

        if "done search grep A C2" in line:
            W2_b = False
            case_W2.append(W2)
            W2 = []

        if "done search grep A C3" in line:
            W3_b = False
            case_W3.append(W3)
            W3 = []

        if(a_b and "Written" not in line):
            if(len(line) == 12):
                a.append(line.strip())

        if(R1_b):
            line = line.replace(" ", "")
            R1.append(line)

        if (R2_b):
            line = line.replace(" ", "")
            R2.append(line)

        if (R3_b):
            line = line.replace(" ", "")
            R3.append(line)

        if (R4_b):
            line = line.replace(" ", "")
            R4.append(line)

        if (R5_b):
            line = line.replace(" ", "")
            R5.append(line)

        if (R6_b):
            line = line.replace(" ", "")
            R6.append(line)

        if (W1_b):
            line = line.replace(" ", "")
            W1.append(line)

        if (W2_b):
            line = line.replace(" ", "")
            W2.append(line)

        if (W3_b):
            line = line.replace(" ", "")
            W3.append(line)

        if "Written timestamps, iteration: 0" in line:
            a_b = True
        if (a_b and "Written timestamps, iteration: 99999" in line):
            next_a = True

        if "search grep R B1" in line and "done" not in line:
            R1_b = True

        if "search grep R B2" in line and "done" not in line:
            R2_b = True

        if "search grep R B3" in line and "done" not in line:
            R3_b = True

        if "search grep R B4" in line and "done" not in line:
            R4_b = True

        if "search grep R B5" in line and "done" not in line:
            R5_b = True

        if "search grep R B6" in line and "done" not in line:
            R6_b = True

        if "search grep A C1" in line and "done" not in line:
            W1_b = True

        if "search grep A C2" in line and "done" not in line:
            W2_b = True

        if "search grep A C3" in line and "done" not in line:
            W3_b = True

    print("Start: " + start_date)
    print("End: " + end_date)

    print("Calculate statistics")

    calculate_amounts_into_csv(case_a, case_R1, case_R2, case_R3, case_R4, case_R5, case_R6, case_W1, case_W2, case_W3, start_date)

    calculate_all_intersections(case_a, case_R1, case_R2, case_R3, case_R4, case_R5, case_R6, case_W1, case_W2, case_W3,start_date)

    calculate_c_intersections(case_a, case_R1, case_R2, case_R3, case_R4, case_R5, case_R6, case_W1, case_W2, case_W3,start_date)

    print("End evaluation")
    return iterations

def convert_to_a_time(pattern):

        match = pattern.replace(" ", "")
        time_stamp = match[32:48]
        first = time_stamp[0:2]
        second = time_stamp[2:4]
        third = time_stamp[4:6]
        fourth = time_stamp[6:8]
        fiveth = time_stamp[8:10]
        sixth = time_stamp[11:12]

        hex_big = sixth + fiveth + fourth + third + second + first
        try:
            conv = int(hex_big, 16)
        except:
            return 0

        return conv

def conv_a(p):
    try:
        conv = int(p, 16)
    except:
        return 0

    return conv


def calculate_c_intersections(a_l, R1_l, R2_l, R3_l, R4_l, R5_l, R6_l, W1_l, W2_l, W3_l, start_date):
    name = "results_csv/c_intersections.csv"
    start_date = start_date.strip()
    # a = A; R2 = B; W1 = C

    with open(name, mode='a') as csv_results:

        # per each exp, e.g. 3 it; each iteration contains all dumps
        # rem only within one exp

        # for each exp
        for i in range(len(a_l)):
            sets = []
            R1 = {}
            R2 = {}
            R3 = {}
            R4 = {}
            R5 = {}
            R6 = {}
            W1 = {}
            W2 = {}
            W3 = {}

            intersection_bis = {}
            lost = {}

            # not for first exp
            if i > 0:


                iteration = "i=" + str(i + 1) + "; date: " + start_date
                a_conv = list(map(lambda x: conv_a(x), a_l[i]))
                a_without_0 = list(filter(lambda x: x > 0, a_conv))
                a = set(a_without_0)


                # for each set
                for j in range(9):

                    # R1
                    if j == 0:
                        R1_conv = list(map(lambda x: convert_to_a_time(x), R1_l[i]))
                        R1 = set(R1_conv)
                        sets.append(R1)

                    # R2
                    if j == 1:
                        R2_conv = list(map(lambda x: convert_to_a_time(x), R2_l[i]))
                        R2 = set(R2_conv)
                        sets.append(R2)

                    # R3
                    if j == 2:
                        R3_conv = list(map(lambda x: convert_to_a_time(x), R3_l[i]))
                        R3 = set(R3_conv)
                        sets.append(R3)

                    # R4
                    if j == 3:
                        R4_conv = list(map(lambda x: convert_to_a_time(x), R4_l[i]))
                        R4 = set(R4_conv)
                        sets.append(R4)

                    # R5
                    if j == 4:
                        R5_conv = list(map(lambda x: convert_to_a_time(x), R5_l[i]))
                        R5 = set(R5_conv)
                        sets.append(R5)

                    # R6
                    if j == 5:
                        R6_conv = list(map(lambda x: convert_to_a_time(x), R6_l[i]))
                        R6 = set(R6_conv)
                        sets.append(R6)


                    # W1 = b7
                    if j == 6:
                        W1_conv = list(map(lambda x: convert_to_a_time(x), W1_l[i]))
                        W1 = set(W1_conv)
                        sets.append(W1)

                        W1_notR1 = W1 - R1
                        W1and_R1 = W1.intersection(R1)
                        W1_notR2 = W1 -R2
                        W1and_R2 = W1.intersection(R2)
                        W1and_R3 = W1.intersection(R3)
                        W1and_R4 = W1.intersection(R4)
                        W1and_R5 = W1.intersection(R5)
                        W1and_R6 = W1.intersection(R6)

                        csv_results.write(iteration + ',W1' + ',R1notW1,' + str(len(W1_notR1)) + '\n')
                        csv_results.write(iteration + ',W1' + ',R1andW1,' + str(len(W1and_R1)) + '\n')

                        csv_results.write(iteration + ',W2' + ',R1notW2,' + str(len(W1_notR2)) + '\n')

                        csv_results.write(iteration + ',W2' + ',R1andW2,' + str(len(W1and_R2)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R1andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R1andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W4' + ',R1andW4,' + str(len(W1and_R4)) + '\n')
                        csv_results.write(iteration + ',W5' + ',R1andW5,' + str(len(W1and_R5)) + '\n')
                        csv_results.write(iteration + ',W6' + ',R1andW6,' + str(len(W1and_R6)) + '\n')




                    # W2 = b8
                    if j == 7:
                        W2_conv = list(map(lambda x: convert_to_a_time(x), W2_l[i]))
                        W2 = set(W2_conv)
                        sets.append(W2)

                        W1_notR1 = W2 - R1
                        W1and_R1 = W2.intersection(R1)
                        W1_notR2 = W2 - R2
                        W1and_R2 = W2.intersection(R2)
                        W1and_R3 = W2.intersection(R3)
                        W1and_R4 = W2.intersection(R4)
                        W1and_R5 = W2.intersection(R5)
                        W1and_R6 = W2.intersection(R6)

                        csv_results.write(iteration + ',W1' + ',R2notW1,' + str(len(W1_notR1)) + '\n')
                        csv_results.write(iteration + ',W1' + ',R2andW1,' + str(len(W1and_R1)) + '\n')
                        csv_results.write(iteration + ',W2' + ',R2notW2,' + str(len(W1_notR2)) + '\n')
                        csv_results.write(iteration + ',W2' + ',R2andW2,' + str(len(W1and_R2)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R2andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R2andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W4' + ',R2andW4,' + str(len(W1and_R4)) + '\n')
                        csv_results.write(iteration + ',W5' + ',R2andW5,' + str(len(W1and_R5)) + '\n')
                        csv_results.write(iteration + ',W6' + ',R2andW6,' + str(len(W1and_R6)) + '\n')

                    # W3 = b9
                    if j == 8:
                        W3_conv = list(map(lambda x: convert_to_a_time(x), W3_l[i]))
                        W3 = set(W3_conv)
                        sets.append(W3)


                        W1_notR1 = W3 - R1
                        W1and_R1 = W3.intersection(R1)

                        W1_notR2 = W3 - R2

                        W1and_R2 = W3.intersection(R2)
                        W1and_R3 = W3.intersection(R3)
                        W1and_R4 = W3.intersection(R4)
                        W1and_R5 = W3.intersection(R5)
                        W1and_R6 = W3.intersection(R6)

                        csv_results.write(iteration + ',W1' + ',R3notW1,' + str(len(W1_notR2)) + '\n')
                        csv_results.write(iteration + ',W1' + ',R3andW1,' + str(len(W1and_R2)) + '\n')
                        csv_results.write(iteration + ',W2' + ',R3notW2,' + str(len(W1_notR2)) + '\n')
                        csv_results.write(iteration + ',W2' + ',R3andW2,' + str(len(W1and_R2)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R3andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W3' + ',R3andW3,' + str(len(W1and_R3)) + '\n')
                        csv_results.write(iteration + ',W4' + ',R3andW4,' + str(len(W1and_R4)) + '\n')
                        csv_results.write(iteration + ',W5' + ',R3andW5,' + str(len(W1and_R5)) + '\n')
                        csv_results.write(iteration + ',W6' + ',R3andW6,' + str(len(W1and_R6)) + '\n')


def calculate_all_intersections(a_l, R1_l, R2_l, R3_l, R4_l, R5_l, R6_l, W1_l, W2_l, W3_l, start_date):
    name = "results_csv/all_intersections.csv"
    start_date = start_date.strip()
    # a = A; R2 = B; W1 = C

    with open(name, mode='a') as csv_results:

        # per each exp, e.g. 3 it; each iteration contains all dumps
        # rem only within one exp

        # for each exp
        for i in range(len(a_l)):
            sets = []
            R1 = {}
            R2 = {}
            R3 = {}
            R4 = {}
            R5 = {}
            R6 = {}
            W1 = {}
            W2 = {}
            W3 = {}

            intersection_bis = {}
            lost = {}

            # not for first exp
            if i > 0:

                iteration = "i=" + str(i + 1) + "; date: " + start_date
                a_conv = list(map(lambda x: conv_a(x), a_l[i]))
                a_without_0 = list(filter(lambda x: x > 0, a_conv))
                a = set(a_without_0)


                # for each set
                for j in range(9):

                    # R1
                    if j == 0:
                        R1_conv = list(map(lambda x: convert_to_a_time(x), R1_l[i]))
                        R1 = set(R1_conv)
                        sets.append(R1)

                        a_not_b = a - R1
                        r_not_a= R1 -a

                        csv_results.write(iteration + ',W1' + ',W1notA,' + str(len(r_not_a)) + '\n')
                        csv_results.write(iteration + ',W1' + ',AnotBi:lost,' + str(len(a_not_b)) + '\n')


                    # W2
                    if j == 1:
                        R2_conv = list(map(lambda x: convert_to_a_time(x), R2_l[i]))
                        R2 = set(R2_conv)
                        sets.append(R2)

                        a_not_b = a - R2
                        a_not_bi = a - R2
                        a_not_bi.difference_update(R1)



                        csv_results.write(iteration + ',W2' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',W2'+ ',inBis:grounds,' + str(len(R2)) + '\n')


                    # W3
                    if j == 2:
                        R3_conv = list(map(lambda x: convert_to_a_time(x), R3_l[i]))
                        R3 = set(R3_conv)
                        sets.append(R3)

                        a_not_b = a - R3
                        a_not_bi = a - R3
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)

                        intersection_b_b = R3.intersection(R2)

                        w1_notw_3 = R1 - R3

                        csv_results.write(iteration + ',W1' + ',W1notW3,' + str(len(w1_notw_3)) + '\n')
                        csv_results.write(iteration + ',W3' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',W3' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')


                    # R4
                    if j == 3:
                        R4_conv = list(map(lambda x: convert_to_a_time(x), R4_l[i]))
                        R4 = set(R4_conv)
                        sets.append(R4)

                        a_not_b = a - R4
                        a_not_bi = a - R4
                        a_not_bi.difference_update(R3)
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)

                        intersection_b_b = R4.intersection(R2, R3)
                        csv_results.write(iteration + ',W4' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',W4' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')


                    # R5
                    if j == 4:
                        R5_conv = list(map(lambda x: convert_to_a_time(x), R5_l[i]))
                        R5 = set(R5_conv)
                        sets.append(R5)

                        a_not_b = a - R5
                        a_not_bi = a - R5
                        a_not_bi.difference_update(R4)
                        a_not_bi.difference_update(R3)
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)

                        intersection_b_b = R5.intersection(R2, R3, R4)

                        csv_results.write(iteration + ',W5' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(
                            iteration + ',W5' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')

                    # R6
                    if j == 5:
                        R6_conv = list(map(lambda x: convert_to_a_time(x), R6_l[i]))
                        R6 = set(R6_conv)
                        sets.append(R6)

                        a_not_b = a - R6
                        a_not_bi = a - R6 -R5-R4-R3-R2-R1
                        test = a -(R6| R5 | R4 | R3 | R2| R1)


                        intersection_b_b = R6.intersection(R2, R3, R4, R5)

                        intersection_bis = intersection_b_b
                        lost = a_not_bi

                        csv_results.write(iteration + ',W6' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(
                            iteration + ',W6' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')

                    # W1 = b7
                    if j == 6:
                        W1_conv = list(map(lambda x: convert_to_a_time(x), W1_l[i]))
                        W1 = set(W1_conv)
                        sets.append(W1)

                        a_not_b = a - W1
                        a_not_bi = a - W1
                        a_not_bi.difference_update(R6)
                        a_not_bi.difference_update(R5)
                        a_not_bi.difference_update(R4)
                        a_not_bi.difference_update(R3)
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)



                        intersection_b_b = W1.intersection(R2, R3, R4, R5, R6)


                        #not in grounds but in c
                        c_in_a = W1.intersection(a)

                        notG = W1 - intersection_bis
                        notR2 = W1- R2
                        notR3 = W1- R3
                        notR4 = W1 - R4
                        notR5 = W1 - R5
                        notR6 = W1 - R6

                        # not in bis but in c
                        lost_and_found = W1.intersection(lost)

                        csv_results.write(iteration + ',R1' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotGrounds,' + str(len(notG)) + '\n')
                        csv_results.write(iteration + ',R1' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotR2,' + str(len(notR2)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotR3,' + str(len(notR3)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotR4,' + str(len(notR4)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotR5,' + str(len(notR5)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotR6,' + str(len(notR6)) + '\n')
                        csv_results.write(iteration + ',R1' + ',CnotBi,' + str(len(notR6)) + '\n')



                    # W2 = b8
                    if j == 7:
                        W2_conv = list(map(lambda x: convert_to_a_time(x), W2_l[i]))
                        W2 = set(W2_conv)
                        sets.append(W2)

                        a_not_b = a - W2
                        a_not_bi = a - W2
                        a_not_bi.difference_update(W1)
                        a_not_bi.difference_update(R6)
                        a_not_bi.difference_update(R5)
                        a_not_bi.difference_update(R4)
                        a_not_bi.difference_update(R3)
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)

                        intersection_b_b = W2.intersection(R2, R3, R4, R5, R6, W1)

                        # not in grounds but in c
                        c_in_a = W2.intersection(a)

                        notG = W2 - intersection_bis
                        notR2 = W2 - R2
                        notR3 = W2 - R3
                        notR4 = W2 - R4
                        notR5 = W2 - R5
                        notR6 = W2 - R6

                        # not in bis but in c
                        lost_and_found = W2.intersection(lost)

                        csv_results.write(iteration + ',R2' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotGrounds,' + str(len(notG)) + '\n')
                        csv_results.write(iteration + ',R2' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotR2,' + str(len(notR2)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotR3,' + str(len(notR3)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotR4,' + str(len(notR4)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotR5,' + str(len(notR5)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotR6,' + str(len(notR6)) + '\n')
                        csv_results.write(iteration + ',R2' + ',CnotBi,' + str(len(notR6)) + '\n')

                    # W3 = b9
                    if j == 8:
                        W3_conv = list(map(lambda x: convert_to_a_time(x), W3_l[i]))
                        W3 = set(W3_conv)
                        sets.append(W3)

                        a_not_b = a - W3
                        a_not_bi = a - W3
                        a_not_bi.difference_update(W2)
                        a_not_bi.difference_update(W1)
                        a_not_bi.difference_update(R6)
                        a_not_bi.difference_update(R5)
                        a_not_bi.difference_update(R4)
                        a_not_bi.difference_update(R3)
                        a_not_bi.difference_update(R2)
                        a_not_bi.difference_update(R1)

                        intersection_b_b = W3.intersection(R2, R3, R4, R5, R6, W1, W2)

                        # not in grounds but in c
                        c_in_a = W3.intersection(a)

                        notG = W3 - intersection_bis
                        notR2 = W3 - R2
                        notR3 = W3 - R3
                        notR4 = W3 - R4
                        notR5 = W3 - R5
                        notR6 = W3 - R6

                        # not in bis but in c
                        lost_and_found = W3.intersection(lost)

                        csv_results.write(iteration + ',R3' + ',AnotBi:lost,' + str(len(a_not_bi)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotGrounds,' + str(len(notG)) + '\n')
                        csv_results.write(iteration + ',R3' + ',inBis:grounds,' + str(len(intersection_b_b)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotR2,' + str(len(notR2)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotR3,' + str(len(notR3)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotR4,' + str(len(notR4)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotR5,' + str(len(notR5)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotR6,' + str(len(notR6)) + '\n')
                        csv_results.write(iteration + ',R3' + ',CnotBi,' + str(len(notR6)) + '\n')


def calculate_amounts_into_csv(a, R1, R2, R3, R4, R5, R6, W1, W2, W3, start_date):
    name = "results_csv/numbers_patterns.csv"
    start_date = start_date.strip()

    with open(name, mode='a') as csv_results:
        fieldnames = ['exp', 'set', 'amount']

        # per each exp, e.g. 3 it; each iteration contains all dumps
        for i in range(len(a)):
            # skip first experiment
            if i > 0:
                iteration = "i="+ str(i+1)+"; date: "+start_date

                csv_results.write(iteration +',A,'+ str(len(a[i]))+'\n')
                csv_results.write(iteration + ',W1,' + str(len(R1[i]))+'\n')
                csv_results.write(iteration + ',W2,' + str(len(R2[i]))+'\n')
                csv_results.write(iteration + ',W3,' + str(len(R3[i]))+'\n')
                csv_results.write(iteration + ',W4,' + str(len(R4[i]))+'\n')
                csv_results.write(iteration + ',W5,' + str(len(R5[i]))+'\n')
                csv_results.write(iteration + ',W6,' + str(len(R6[i]))+'\n')
                csv_results.write(iteration + ',R1,' + str(len(W1[i]))+'\n')
                csv_results.write(iteration + ',R2,' + str(len(W2[i]))+'\n')
                csv_results.write(iteration + ',R3,' + str(len(W3[i]))+'\n')



if __name__ == '__main__':

    path= "../logs/not_evaluated"
    path_evaluated = "../logs/evaluated"
    logs = os.listdir(path)
    iterations = 0
    for log in logs:
        log_path= os.path.join(path, log)
        iterations+= analyse_case(log_path)
        shutil.move(log_path, path_evaluated)

    print("Exp. amounts")
    print(iterations)

















