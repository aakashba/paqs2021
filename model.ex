We walk through the actual Keras implementation of our model to maximize clarity and reproducibility, following the example of LeClair et al.

```
qe = Embedding(output_dim=self.embdims,input_dim=self.quesvocabsize)(ques_input)
ce = Embedding(output_dim=self.embdims,input_dim=self.codevocabsize)(code_input) 
```
The first step is to create a word embedding space for the question and code encoder inputs.
The question vocabulary size we used was 20K, but we used a much larger vocabulary of 100K for the source code context for domain specific words. 
Vocabulary sizes are curated to fit GPU resource limitations through trial and error. 
```
ques_enc = CuDNNGRU(self.rnndims, return_state=True, return_sequences=False)
quesout, qs = ques_enc(qe)
code_enc = CuDNNGRU(self.rnndims, return_state=True, return_sequences=True) 
codeout, cs = enc(ce, initial_state=qs)
```
We use a GRU to encode the question and source code, with the question and source code embedding spaces serving as input. 
We set the initial state of the code encoder to the end state of the question encoder,
in line with other neural QA model designs in which the question state is used to start the state of the context encoding. 
```
ae = Embedding(output_dim=self.embdims, input_dim=self.ansvocabsize)(ans_input) 
aec = CuDNNGRU(self.rnndims, return_sequences=True) 
aout = aec(ae, initial_state=cs)
```
The decoder follows the same basic structure: an embedding space as input to a GRU. 
The decoder input is the answer. The answer vocabulary size is 20K. 
```
ques_attn = dot([aout, quesout], axes=[2, 2]) 
ques_attn = Activation(’softmax’)(ques_attn) 
ques_context=dot([ques_attn, quesout],axes=[2, 1]) 
code_attn = dot([aout, codeout], axes=[2, 2]) 
code_attn = Activation(’softmax’)(code_attn) 
code_context=dot([code_attn, codeout], axes=[2, 1])
```
Our attention mechanism consists of attention applied from the decoder (aout) to both the question and source code context. 
The attention to code context is especially important because this is how the model emphasizes context features.
This is chiefly what papers mean when they say that the model “learns to comprehend” the context. 
We show in our experimental results in the paper how the model learns different code features relevant to different questions. 
```
context = concatenate([ques_context, code_context, aout])
out = TimeDistributed(Dense(self.rnndims, activation="relu"))(context) 
```
The next step is to create a context matrix by combining the attended question and context matrices with the answer context from the decoder. 
Then, the models uses the combined context matrix to predict the next word in the answer. 
