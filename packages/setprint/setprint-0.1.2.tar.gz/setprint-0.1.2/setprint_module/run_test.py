# your_module __init__.py
from setprint import Myint, set_txt,set_txts, set_number,set_numbers, slice_blocks, setprint
import numpy as np


# test_list = [[[0],[10,20]],[[1],[10,20]],[[2],[10,20]],[[3,3],[10,20]]]

test_list =  [

                ['[0][0]','[0][1]','[0][2]','[0][3]'],
                ['[1][0]','[1][1]',['[1][2][0]','[1][2][1]'],'[1][3]'],
                ['[2][0]','[2][1]','[2][2]',['[2][3][0]',['[2][3][1][0]','[2][3][1][1]']],'[2][4]','[2][5]'],
                ['[3][0]','[3][1]','[3][2]','[3][3]','[3][4]'],
                '[4]'
                
               ]


# for line in samplelist:
#     print(line)

[ 'R','G','B' ]

test_array = np.zeros((31,15,3),dtype='i8')

test_array = test_array.tolist()
bug = 'bug'

test_array[5][0][0] = [bug,bug,bug] #
test_array[8][1][0] = [bug,bug,bug] #

test_array[9][3]  = '' #
test_array[15][3] = bug #
test_array[30][3] = bug #

test_array[10][5][0] = [bug,[bug,[bug]]] ###
test_array[15][5][1] = [bug,[bug,bug]]   #
test_array[20][5][2] = [bug,bug,bug]     #
test_array[21][5][0] = [bug,bug,bug]     #

test_array[5][14][0] = [bug,bug,bug] # 
test_array[8][9][0] = [bug,bug,bug]  #

test_array[10][8][0] = [bug,bug,bug]  #
test_array[15][7][0] = [bug,bug,bug]  #
test_array[20][12][0] = [bug,bug,bug] #
test_array[21][10][0] = [bug,bug,bug] #

list_data = setprint(test_list)
answer = list_data.set_list(guide=True,keep_start=2,keeplen=10)

with open('output_path.txt','w') as f:
    for line in answer['grid_slice']:
        f.write(line)

list_data.pick_guidePrint('output_path.txt')

# b = pick_guidePrint(answer,'/Users/matsuurakenshin/WorkSpace/development/set_data/Make_txtfile/test_SetData_GuidePrint.txt')
# b.execute()


# output_path = '/Users/matsuurakenshin/WorkSpace/development/set_data/Make_txtfile/SET_list.txt'

# All_blocks = [ 
#                [ ['title','1line','2line'], ['1_2','1_txt','2_txt'] ],
#                [ ['2_1','1_data','2_data'], ['2_2','1_line','2_line','3_line'], ['title','1_txt','2_txt']],
#                [ ['3_1','1_txt','2_txt']],

#                ]
# list_data = setprint( All_blocks)
# grid_slice = list_data.blocks_border_print(guide=True)

# with open(output_path,'w') as f:
#     for line in grid_slice:
#         f.write(line)
