import numpy as np
import pandas as pd
import os
import shutil
import ast 
import subprocess



def get_student_ids(move_dir,change_dir = True):
    '''
    This function will read inside the provided move_dir directory and will list out all the folders inside.
    We are assuming the folder inside has all the studentids.
    
    :params:
    move_dir : The given directory where the student ids are location
    Change_dir : Boolean to change the directory we are currently in (default is True)
    
    :returns:
    list of folder names (string) inside the directory 
    
    '''
    if not os.path.exists(move_dir):
        return 'Wrong Path'
    if change_dir == True:
        os.chdir(move_dir)
        current_dir = os.path.abspath(os.getcwd())
        x = [files for files in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, files))]
        unwanted = []
        for i in x:
            if '.' in i:
                unwanted.append(i) 
            else:
                pass
        return [ele for ele in x if ele not in unwanted]
    else:
        current_dir = os.path.join(move_dir)
        x = [files for files in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, files))]
        unwanted = []
        for i in x:
            if '.' in i:
                unwanted.append(i) 
            else:
                pass
        return [ele for ele in x if ele not in unwanted]

    
def make_grade_sheet(student_ids):
    
    """
    Makes a dataframe with respect to the number of student Ids and the number of questions.
    
    Requires an integer input of the number of questions.
    
    :params:
    student_ids : list of student ids inside the working directory
    
    :returns:
    grade_sheet : a dataframe made using pandas
    num_questions : the number of questions inputted by the user.
    
    """
    
    num_questions = int(input('Input the number of questions in this assignment: ')) # Input the number of questions
    cols = ['ID']  # Student Ids 
    for i in range(1,num_questions+1):
        cols.append(f'Q{i}')
    
    print('Initializaing the Points Tally for the Students')
    grade_sheet = pd.DataFrame()  # Pandas dataframe
    for i in cols:
        grade_sheet[i] = 0.0
    print('This is your grade sheet with all the Student Ids')
    grade_sheet['ID'] = student_ids
    grade_sheet[cols[1:]] = 0.0
    print(grade_sheet)
    return grade_sheet,num_questions

def week(student_id,week):
    '''
    Searches for the number of folders inside the designated student id folder. 
    We are assuming all folders inside are weeks.
    
    :returns:
    new path with the respective week folder
    '''
    
    print(f'\nYou are in the {week} Directory') 
    return os.path.join(student_id,week)


def homework_or_NTT(student_week_path,ASSIGNMENT_TYPE):
    '''
    Uses the provided path and joins it with the type of assignment provided if it exists
    
    :params:
    student_week_path : path that connects the student id folder and it's subdirectory
    assignment : name of the folder we want to add to our path.
    
    :returns:
    new path with the assignment folder joined
    '''
    if not os.path.exists(os.path.join(student_week_path,ASSIGNMENT_TYPE)):
        return 'No Folder Found'
    return os.path.join(student_week_path,ASSIGNMENT_TYPE)


def get_python_list(file_path):
    """
    Find all the .py files in the directory and append them to a raw_files list.

    :params:
    file_path = the path to the folder where the to-be read folders are.
    :returns:
    raw_files : list of all files ending with '.py' in the read folder.
    """
    python_files = []
    for file in os.listdir(file_path):
        if file.endswith(".py"):
            python_files.append(file)
    print('\nThese are all the .py files inside the folder: \n')
    for i in python_files:
        print(i)

    return python_files


def make_answer_key(num_questions):
    ''' This question provides the user the opportunity to set up all the answer keys by answer with 'Y' 
        or to set up the answer key manually when grading the questions with 'N'.
        
        If 'Y' we will further be asked the following for every question.
        - Does the question have subparts?
        - What is the type of answer i.e integer (int), decimal (float), string (str), list (list), tuple (tuple)
        
        :params:
        num_questions : The number of question to create answer keys for
        
        
        :returns:
        if make_answer_keys == 'N' : None
        if make_answer_keys == 'Y' : A dynamic list of lists with the number of columns for every question depending on 
                                     the number of subparts.
        
        
        '''
    
    correct_answer = []
    per_question_answers = []
    
    make_answer_keys = input(' Would you like to set up the Correct Answers for the Questions right now\n or would you prefer setting them up manually?\n Pleae answer with Y or N respectively [Y/N]: ')
    
    while make_answer_keys != 'Y' and make_answer_keys != 'N':
        make_answer_keys = input(' Would you like to set up the Correct Answers for the Questions right now\n or would you prefer setting them up manually?\n Pleae answer with Y or N respectively [Y/N]: ')

    if make_answer_keys == 'Y':
        print('\n If there is a question you want to grade manually please enter "NaN"')
        print(f' There are {num_questions} Questions in this assignment,\n you will be asked to enter the answers for the sub parts depending on the question')
        
        for i in range(1,num_questions+1):
            while True:
                try:
                    sub_parts = int(input(f' Please enter the number of subparts for Q{i}: '))
                except ValueError:
                    print("Sorry, I didn't understand that.")
                    #better try again... Return to the start of the loop
                    continue
                else:
                    break
            for j in range(1,sub_parts+1):
                while True:
                    try:
                        answer = input(f' Enter the answer for Q{i} part {j}: ')
                        answer_type = input('Is this answer is : \ninteger (int), \ndecimal (float), \nstring (str), \nlist (list), \ntuple (tuple): ')
                        if answer_type == 'int':
                            per_question_answers.append(int(answer))
                        elif answer_type == 'float':
                            per_question_answers.append(float(answer))
                        elif answer_type == 'str':
                            per_question_answers.append(str(answer))
                        elif answer_type == 'list':
                            per_question_answers.append(ast.literal_eval(answer))
                        elif answer_type == 'tuple':
                            per_question_answers.append(eval(answer))
                        elif answer_type != 'tuple' and answer_type != 'list' and answer_type != 'str' and answer_type == 'float' and answer_type == 'int':
                            print('Incorrect input')
                            return
                    except ValueError:
                        print("Sorry, I didn't understand that.")
                        #better try again... Return to the start of the loop
                        continue
                    else:
                        break
            correct_answer.append(per_question_answers)
            per_question_answers = []
                
    elif make_answer_keys == 'N':
        print(' You will be manually entering the answers below for each question')
        
    return correct_answer,make_answer_keys

####################################### If Auto Grading #####################################################################
def grade_question(Question,student_ids,Grading_Sheet,answer,correct_answer):
    ''' 
    This function selects the designated question number, and the first student id in the studen_ids and modifies the grades 
    for the selected in the dataframe. 
    
    
   
    
    
    :params:
    Question       : 
    student_ids    :
    Grading_Sheet  :
    answer         :
    correct_answer : 
    
    :returns:
    Grading sheet for the student being graded - Updated with the present score
    '''
    if len(answer) != len(grading_sh
    for a in range(0,len(answer)): 
        if answer[a] != correct_answer[a]:
            print(f'{answer[a]} is incorrect, correct answer is {correct_answer[a]}')
            Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0],f'{Question}'] += 0
        elif answer[a] == correct_answer[a]:
            print(f'{answer[a]} is correct')
            Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0],f'{Question}'] += (1/len(answer))
           
    return Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0]] 




####################################### If Manual Grading #####################################################################

def mannual_answer_key(question_num,correct_answer_key= None):
    
    if question_num == 1:
        correct_answer_key = []
    per_question_answers = []
    for i in range(question_num,question_num+1):
        while True:
            try:
                sub_parts = int(input(f' Please enter the number of subparts for Q{question_num}: '))
            except ValueError:
                print("Sorry, I didn't understand that.")
                #better try again... Return to the start of the loop
                continue
            else:
                break
        for j in range(1,sub_parts+1):
            while True:
                try:
                    answer = input(f' Enter the answer for Q{question_num} part {j}: ')
                    answer_type = input('Is this answer is : \ninteger (int), \ndecimal (float), \nstring (str), \nlist (list), \ntuple (tuple): ')
                    if answer_type == 'int':
                        per_question_answers.append(int(answer))
                    elif answer_type == 'float':
                        per_question_answers.append(float(answer))
                    elif answer_type == 'str':
                        per_question_answers.append(str(answer))
                    elif answer_type == 'list':
                        per_question_answers.append(ast.literal_eval(answer))
                    elif answer_type == 'tuple':
                        per_question_answers.append(eval(answer))
                    elif answer_type != 'tuple' and answer_type != 'list' and answer_type != 'str' and answer_type == 'float' and answer_type == 'int':
                        print('Incorrect input')
                        return

                except ValueError:
                    print("Sorry, I didn't understand that.")
                    #better try again... Return to the start of the loop
                    continue
                else:
                    break
        correct_answer_key.append(per_question_answers)
        per_question_answers = []
    return correct_answer_key,question_num



def manual_grade_question(q,correct_answer_key,Grading_Sheet,student_ids,student_answers = None):
    #for j in range(len(manually_graded_questions)):
        #output = subprocess.check_output(['python', f'{manually_graded_questions[j]}.py']) # executes the file and saves the output
        #answers = output.decode('utf-8') # deletes an empty element at the end
    print(f"\nThis is the answer for Q{q} vs What the student answered: \n")
    
    if student_answers:
        for ans in range(len(correct_answer_key)):
            if len(correct_answer_key) == len(student_answers):
                print(f"The correct answer is {correct_answer_key[ans]} : The student answered {student_answers[ans]}")
            else:
                print('length not equal')
                break
            
    for i in correct_answer_key:
        r_or_w = input(f"Is this answer : '{i}' correct?")
        if r_or_w == 'Y':
            Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0],f'Q{q}'] += (1/len(correct_answer_key))
            print(Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0]])
        elif r_or_w == 'N':
            Grading_Sheet.loc[Grading_Sheet.ID == student_ids[0],f'Q{q}'] += 0

    return Grading_Sheet

    

###################################### Steps after grading ####################################################################


def move_graded_student(Graded_folder,student_ids):
    '''
    Moves the folder graded student_id to the Grade folder. One the folder has been moved the student id is removed from the 
    student_ids list.
    
    :params:
    Graded_folder: Name of the graded folder where the student id folder will be moved.
    student_ids : The student Id folder to be moved. Assumed to be the first
    
    :returns:
    if remaining student_ids == 0 : returns message that we are done grading
    else : returns the count of remaining students.
    
    '''
    os.chdir('../../../')
    print(os.path.abspath(os.getcwd()))
    if not os.path.exists(f'../{Graded_folder}'):
        os.mkdir(f'../{Graded_folder}')
        print('Successfully Created Directory, Lets get started')
    else:
        print('Directory Already Exists')

    shutil.move(f'{student_ids[0]}',f'../{Graded_folder}')
    student_ids.pop(0)        
    if len(student_ids) == 0:
        x = "You are Done Grading!"
        os.chdir('../../')
        return len(student_ids)
    else: 
        print(f"Number of Students Left: {len(student_ids)}")
        print(f"Ids Left: {student_ids}")
        os.chdir('../../')
        return len(student_ids)
    
    
    
    
    
##### FUNCTIONS IN TESTING PHASE ###############


    
def questions_to_manually_grade(correct_answer_key):
    manually_grade_questions = []
    for i in range(0,len(correct_answer_key)):
        if correct_answer_key[i][0][0] == 'NA':
            manually_grade_questions.append([i+1][0])
            #print("This is NA You'll have to grade the question manually")
            correct_answer_key.pop([i][0])
            #answer.pop(i-1)
        else:
            pass
    return correct_answer_key,manually_grade_questions

