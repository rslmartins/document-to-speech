import streamlit as st
import sympy as sym
st.title("Equation Solver")
@st.cache(allow_output_mutation=True)
def variables():
	return []

menu = ["Derivative", "Integration"]
choice = st.sidebar.selectbox("Operation",menu)

text_input = st.text_input(label='Enter parameters')
if st.button("Submit parameters"):
	variables().append(text_input)
	variables_list = [x for x in variables() if x]
	st.success(variables_list)

if st.button("Clear parameters"):
	variables().clear()
	variables_list = [x for x in variables() if x]
	st.success('No parameters')
 
if len(variables())>0:
	variables_list = [x for x in variables() if x]
	selected_variables = st.multiselect(label= 'Enter variable:', options= variables_list, default=[])
	
	function_string = st.text_input(label='Enter function')
	dict_variables = {variable:sym.symbols(variable) for variable in variables_list}
	
	for variable in variables_list:
		function_string.replace(variable, "dict_variables['"+variable+"']")
	if function_string!= '': st.latex(sym.sympify(function_string))
	if st.button("Submit function"):
		function_operated = sym.sympify(function_string)
		for selected_variable in selected_variables:
			if choice == "Derivative": function_operated = sym.diff(function_operated,dict_variables[selected_variable])
			if choice == "Integration": function_operated = sym.integrate(function_symbolic,dict_variables[selected_variable])
		st.latex(function_operated)	
