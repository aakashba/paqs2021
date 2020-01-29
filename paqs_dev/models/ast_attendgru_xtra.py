from keras.models import Model
from keras.layers import Input, Maximum, Dense, Embedding, Reshape, GRU, merge, LSTM, Dropout, BatchNormalization, Activation, concatenate, multiply, MaxPooling1D, Conv1D, Flatten, Bidirectional, CuDNNGRU, RepeatVector, Permute, TimeDistributed, dot
from keras.backend import tile, repeat, repeat_elements
from keras.optimizers import RMSprop, Adamax
import keras
import keras.utils
import tensorflow as tf

# Much thanks to LeClair et al. for providing the open source implementation of their model.
# https://arxiv.org/abs/1902.01954
# https://github.com/mcmillco/funcom

class AstAttentionGRUModel:
    def __init__(self, config):
        
        config['conlen'] = 50
        
        self.config = config
        self.convocabsize = config['convocabsize']
        self.ansvocabsize = config['ansvocabsize']
        self.quesvocabsize = config['quesvocabsize']
        self.conlen = config['conlen']
        self.anslen = config['anslen']
        self.queslen = config['queslen']
        
        self.embdims = 100
        self.quesdims = 10
        self.recdims = 100
        self.findims = 100

        self.config['batch_maker'] = 'ast'
        self.config['num_input'] = 3
        self.config['num_output'] = 1

    def create_model(self):
        
        con_input = Input(shape=(self.conlen,))
        ans_input = Input(shape=(self.anslen,))
        ques_input = Input(shape=(self.queslen,))
        
        ee = Embedding(output_dim=self.embdims, input_dim=self.convocabsize, mask_zero=False)(con_input)
        se = Embedding(output_dim=self.quesdims, input_dim=self.quesvocabsize, mask_zero=False)(ques_input)

        se_enc = CuDNNGRU(self.recdims, return_state=True, return_sequences=True)
        seout, state_ques = se_enc(se)

        enc = CuDNNGRU(self.recdims, return_state=True, return_sequences=True)
        encout, state_h = enc(ee, initial_state=state_ques)

        
        de = Embedding(output_dim=self.embdims, input_dim=self.ansvocabsize, mask_zero=False)(ans_input)
        dec = CuDNNGRU(self.recdims, return_sequences=True)
        decout = dec(de, initial_state=state_h)

        attn = dot([decout, encout], axes=[2, 2])
        attn = Activation('softmax')(attn)

        ast_attn = dot([decout, seout], axes=[2, 2])
        ast_attn = Activation('softmax')(ast_attn)

        context = dot([attn, encout], axes=[2, 1])
        ast_context = dot([ast_attn, seout], axes=[2, 1])

        context = concatenate([context, decout, ast_context])


        out = TimeDistributed(Dense(self.findims, activation="relu"))(context)

        out = Flatten()(out)
        out = Dense(self.ansvocabsize, activation="softmax")(out)
        
        model = Model(inputs=[con_input, ans_input, ques_input], outputs=out)

        if self.config['multigpu']:
            model = keras.utils.multi_gpu_model(model, gpus=2)
        
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return self.config, model
