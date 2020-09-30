import BitGrading
import pandas as pd
import numpy as np
import os
import ast 
import shutil
import subprocess

grading_done = False
initialize = False

DIRECTORY = 'DigitalHistory/Assignments_To_Be_Graded'

while not grading_done:
    while not initialize:
        student_ids = BitGrading.get_student_ids(DIRECTORY,change_dir=False)
        print(f"These are all the student Id's in our Directory : {student_ids}\n")
        print(f"These are the Weeks inside {student_ids[0]}: {os.listdir(f'DigitalHistory/Assignments_To_Be_Graded/{student_ids[0]}')}")
        WEEK_NUM = 'Week_Two'#input('Enter the name of the folder you want to grade: ')
        print(f"\nThese are the Assignment Types inside {student_ids[0]}: {os.listdir(f'DigitalHistory/Assignments_To_Be_Graded/{student_ids[0]}/{WEEK_NUM}')}")
        ASSIGNMENT_TYPE = 'Now_Try_This'#input('Enter the name of the assignment type you want to grade: ')

        Grading_Sheet,num_questions = BitGrading.make_grade_sheet(student_ids)
        manual = 'Y'
        correct_answer_key = [["e","m","m"],['[0,0,0]',"[1, 2, [3, 4, 'goodbye']]",'[1, 3, 4, 5, 6]]'],
                  [["<type 'tuple'>"]],[["hello"],["hello"],["hello"],["hello"]],[["MacDonald"]],
                          [["NA"]]]

        #correct_answer_key,manual = BitGrading.make_answer_key(num_questions)
        initialize = True
        if manual == 'Y':
            print(correct_answer_key)
            

            
    manual_grading_check = False        
    student_ids = BitGrading.get_student_ids(DIRECTORY,change_dir=True)
    week_path = BitGrading.week(student_ids[0],WEEK_NUM)
    file_path = BitGrading.homework_or_NTT(week_path,ASSIGNMENT_TYPE)

    assignment_list = BitGrading.get_python_list(file_path)
    print(f'Currently Grading {student_ids[0]} -> {WEEK_NUM} - > {ASSIGNMENT_TYPE} Section.')
    os.chdir(file_path)


    correct_answer_key,manually_graded_questions = BitGrading.questions_to_manually_grade(correct_answer_key)
    for man_grade in range(0,len(assignment_list)):
        if assignment_list[man_grade] == f'{man_grade}.py':
            assignment_list.pop(man_grade)
    
    for i in range(0,len(assignment_list)-1):
        print('SANITY CHECK----------------------------------------1') 
        output = subprocess.check_output(['python', f'{i+1}.py']) # executes the file and saves the output

        answers = output.decode('utf-8').split('\n')[:-1] # deletes an empty element at the end

        print(f'The Student Answered: {answers}\n')

        if manual == 'N':
            correct_answer_key,question = BitGrading.mannual_answer_key(1)
            print(f'\n The correct answer key for {question} is {correct_answer_key}')
            BitGrading.grade_question(f'Q{i+1}',student_ids,Grading_Sheet,answers,correct_answer_key[i],)
            print(f'\n{Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0]]}')
        else:   
            BitGrading.grade_question(f'Q{i+1}',student_ids,Grading_Sheet,answers,correct_answer_key[i],)
            Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0]]
    
    
    BitGrading.manual_grade_question(manually_graded_questions,Grading_Sheet,student_ids)
    print('SANITY CHECK----------------------------------------2') 

    GRADED_FOLDER = 'Assignments_Graded'
    remaining_students = BitGrading.move_graded_student(GRADED_FOLDER,student_ids)
    
    
    if remaining_students == 0:
        print('SANITY CHECK----------------------------------------3') 
        Grading_Sheet['Total_Score'] = Grading_Sheet.iloc[:, 1:].sum(axis=1)
        export_file_path = f'{WEEK_NUM}_Grades'
        Grading_Sheet.to_csv (export_file_path, index = True, header=True)
        grading_done = True
        
     