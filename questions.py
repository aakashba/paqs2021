
import pickle

Q1 = [	"What is the return type for method?",
	"What is method return type?",
	"What does method return?",
	"Return type ?",
	"Give me the return type for method",
	"Tell me method's return type",
	"Type of return for method",
	"What is the return type?",
	"Method returns?",
	"Method return type ? ",
	"Return of method ?",
	"Method returns? ",
	"Does it return anything?" ]
	
Q2 = [	"What are the arguments taken by this method?",
	"method parameters",
	"method arguments",
        "argument list",
        "Method argument list ",
        "Method parameter list",
        "Parameter list",
        "Parameters",
        "Arguments",
        "Parameters of the method",
        "Arguments of the method",
	"what are the Parameters of the  method",
	"What does method take as argument?",
	"What arguments does the method take?",
	"What arguments does the method accept?",
        "what parameters does the method accept?",
	"How many arguments does method accept?",
	"What are the parameters ?",
	"What are the arguments for the method?",
	"Does it take any parameters?",
	"Method has the parameters",
	"Give the parameters this method takes",
        "Tell me the parameters this method takes",
	"Arguments accepted by method",
	"Number of parameters accepted",
	"Parameters accepted by method",
	"Parameters method accepts",
	"Give me all accepted parameters" ] 
	

Q3 = [ 	"Show definition",
	"Show method definition for func", 
	"Give definition for func",
	"Method definition",
	"Method overview",
	"Give definition",
	"Everything about method",
	"Show me the original text for method",
	"Tell me more about func ",
	"Show me everything about func",
	"Can you give me complete documentation about method?",
	"Can you show me method ?",
	"Show me the source code for method",
	"Show me declaration for method",
	"Show me an overview of method" ]
	
	

Q4 = [	"What method takes f_arg as input and return f_ret?",
	"method f_arg f_ret",
	"input f_arg output f_ret",
	"take f_arg give f_ret",
	"parameter f_arg return f_ret",
	"argument f_arg return f_ret",
	"What function accepts f_arg and returns f_ret?",
	"What method argument f_arg and returns f_ret?",
        "What method takes parameter f_arg and gives f_ret?",
	"Method that accepts f_arg and returns f_ret",
	"Give me the method that accepts f_arg and returns f_ret",
	"Is there a method that returns f_ret and accepts f_arg?",
	"Accepts arg and returns f_ret",
	"tell me what method takes f_arg returning f_ret",
	"How do I get f_ret from f_arg?",
	"How do I use f_arg to get f_ret?" ]

Q5 = [	"What is the signature ?",
	"What's the method signature?",
	"Method signature",
	"signature method",
	"signature for method",
	"Give me the signature for method?",
	"How do I call this method?",
	"Show me method signature",
	"Tell me how to create an instance of this method?",
	"What are the properties of this method ?",
	"Can you tell me how to call this?",
	"The signature of this method" ]

Q6 = [	"What does this method do?",
	"What can I use this method for?",
	"What can you tell me about this method?",
	"Tell me what this method does",
	"Give me header for method",
	"How can this method help me?",
	"Tell me the purpose of this method",
	"How is this method useful?",
	"method used",
	"What is this method",
	"Method  header",
	"Use for this method ",
	"What can I do with this method?" ]

Q7 = [ "What method does_this?",
	"does_this method name",
	"How can I do_this?",
	"How do I do_this?",
	"Which method does_this?",
	"Method that does_this",
	"Tell me how to do_this",
	"Give me method name to do_this",
	"Help me do_this",
	"I need to do_this",
	"Is there a method that can do_this",
	"do this, how?",
	"method which does_this" ]

Q8 = [ "Can func do_this?",
	"Can I use func to do_this ?",
	"Does func do_this",
	"func does_this, correct?",
	"Could func be used to do_this?",
	"Is func best way to do_this?",
	"Can I do_this using func?",
	"Is func the method that does_this?" ]



Questions = dict()
Questions.update({'Q1':Q1, 'Q2':Q2, 'Q3':Q3, 'Q4':Q4, 'Q5':Q5, 'Q6':Q6, 'Q7':Q7, 'Q8':Q8})
pickle.dump(Questions, open("questions.pkl","wb"))




	
