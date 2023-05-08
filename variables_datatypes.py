# variable stores value

# behaves as value it holds
# data types are below

int_var = 21
bool_var = True
float_var = 5.9
string_var = "string"

# each variable can be affected by the out comes of other variables in a conditional environment

# conditional variables
# the condition of the age affects the state of the other variable bool_var
if int_var == 21:
    bool_var = False
else:
    bool_var = True
