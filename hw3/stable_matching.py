# Zora Che with adaptations from Gavin Brown
# CS330, Fall 2021
# Stable Matching Algorithm Starter Code
#
# Collaborators:
# - Malik Baker
# - Huy Phan
# - Dominic Maglione
# - Mikky Steinberg
#

import sys
import time


def read_prefs(pref_1_filename, pref_2_filename):
    # This function reads preferences from two files
    # and returns two-dimensional preference lists and the length of a list.
    with open(pref_1_filename, "r") as f:
        hospital_raw = f.read().splitlines()
    with open(pref_2_filename, "r") as f:
        student_raw = f.read().splitlines()
    N = int(student_raw[0])
    hospital_prefs = [[int(id) for id in x.split(",")] for x in hospital_raw[1:]]
    student_prefs = [[int(id) for id in x.split(",")] for x in student_raw[1:]]
    return N, hospital_prefs, student_prefs


def inverse_prefs(N, prefs):
    ############################################################
    # Implement inverse preference lists as described in lecture
    ############################################################
    ranks = [
        [0 for i in range(N)] for j in range(N)
    ]  # initialize ranks for N * N inputs

    # loop through every student
    for i, student in enumerate(prefs):
        # loop through their preference list...
        for j, hospital in enumerate(student):
            # each index in list is a hospital, its value is the hopsital's rank
            ranks[i][hospital] = j

    return ranks  # return inverted preferences


def run_GS(N, hospital_prefs, student_prefs, out_name):
    free_hospital = list(range(N))
    count = N * [
        0
    ]  # stores a pointer to each hospital's next unproposed student, going from the left of hospital's preference list
    current = N * [
        None
    ]  # stores current assignment; index -> student, value -> hospital

    # inverse student preference array
    student_prefs = inverse_prefs(N, student_prefs)

    # algorithm - Hospital giving offer to student
    while free_hospital:  # returns True if list is nonempty
        # print('--------')
        # print('current:', current)
        # print('free hospital', free_hospital)
        hospital = free_hospital.pop(0)
        student = hospital_prefs[hospital][count[hospital]]
        # print(hospital, 'proposing to', student)
        count[hospital] += 1
        if current[student] is None:  # student is not paired
            current[student] = hospital
            # print('student is not paired')
        else:
            # O(1) because of inverse preference array
            if (
                student_prefs[student][current[student]]
                < student_prefs[student][hospital]
            ):
                free_hospital.append(hospital)
            else:
                # student switches to new hospital, old hospital becomes free
                # print('student prefers', hospital)
                free_hospital.append(current[student])
                current[student] = hospital
    # write out matches
    with open(out_name, "w") as f:
        for student, hospital in enumerate(current):
            f.write(str(hospital) + "," + str(student) + "\n")


############################################################
# PART 2 STARTER CODE
############################################################

# not done
def check_stable(N, hospital_prefs, student_prefs, match_file):
    # Implement checking of stable matches from output

    # inverse student and hospital preference lists
    inverse_student_prefs = inverse_prefs(N, student_prefs)
    inverse_hospital_prefs = inverse_prefs(N, hospital_prefs)

    # get pairings from match_file
    f = open(match_file, "r")
    pairings = f.readlines()

    # create 2D array in the form of  [[hospital, student] ... [hospital, student]]
    pairings = [[int(x) for x in pair.strip().split(",")] for pair in pairings]

    # create hash table to keep track of hospital's current student assignment
    hospital_to_student = {pair[0]: pair[1] for pair in pairings}

    # iterate through all pairings
    for pair in pairings:
        hospital = pair[0]  # first item in pair is hospital
        student = pair[1]  # second item in pair is student

        # find the ranking of the hospital according to the student
        hospital_rank = inverse_student_prefs[student][hospital]

        # get all hospitals student prefers to the current hospital
        student_preferred_hospitals = student_prefs[student][:hospital_rank]

        # for each preferred hospital...
        for preferred_hospital in student_preferred_hospitals:
            # get the wishful student's rank
            student_rank = inverse_hospital_prefs[preferred_hospital][student]

            # get current pairing of the preferred hospital
            current_student = hospital_to_student[preferred_hospital]

            # get the rank of the current student
            current_student_rank = inverse_hospital_prefs[preferred_hospital][
                current_student
            ]

            # if they prefer the student we're checking to their current assignment...
            if student_rank < current_student_rank:
                print(0)  # it's unstable, print 0 and return
                return

    print(1)  # all checks passed, it's stable


############################################################
# PART 3 STARTER CODE
############################################################


def check_unique(N, hospital_prefs, student_prefs):
    # Implement checking of a unique stable matching for given preferences

    # run GS for hospital and student proposing
    run_GS(N, hospital_prefs, student_prefs, "hospital_optimal")
    run_GS(N, student_prefs, hospital_prefs, "student_optimal")

    # create arrays from hospital and student optimal pairing requests
    hospital_optimal = [
        h_pairing.strip().split(",") for h_pairing in open("hospital_optimal")
    ]
    student_optimal = [
        s_pairing.strip().split(",") for s_pairing in open("student_optimal")
    ]

    # iterate through all student_optimal pairings
    for student in student_optimal:
        # if the student and hopsital pairings aren't the same, then there is no
        # unique stable matching print 0 and return
        if student[1] != hospital_optimal[int(student[0])][0]:
            print(0)
            return

    print(1)  # else all pairings are the same, print 1


############################################################
# Main function. (Do not modify for submission.)
############################################################


def main():
    # Do not modify main() other than using the commented code snippet for printing
    # running time for Q1, if needed
    if len(sys.argv) < 5:
        return "Error: the program should be called with four arguments"
    hospital_prefs_raw = sys.argv[1]
    student_prefs_raw = sys.argv[2]
    match_file = sys.argv[3]
    # NB: For part 1, match_file is the file to which the *output* is wrtten
    #     For part 2, match_file contains a candidate matching to be tested.
    #     For part 3, match_file is ignored.
    question = sys.argv[4]
    N, hospital_prefs, student_prefs = read_prefs(hospital_prefs_raw, student_prefs_raw)
    if question == "Q1":
        # start = time.time()
        run_GS(N, hospital_prefs, student_prefs, match_file)
        # end = time.time()
        # print(end-start)
    elif question == "Q2":
        check_stable(N, hospital_prefs, student_prefs, match_file)
    elif question == "Q3":
        check_unique(N, hospital_prefs, student_prefs)
    else:
        print(
            "Missing or incorrect question identifier (it should be the fourth argument)."
        )
    return


if __name__ == "__main__":
    # example command: python stable_matching.py pref_file_1 pref_file_2 out_name Q1

    # stable_matching.py: filename; do not change this
    # pref_file_1: filename of the first preference list (proposing side)
    # pref_file_2: filename of the second preference list (proposed side)
    # out_name: desired filename for output matching file
    # Q1: desired question for testing
    main()
