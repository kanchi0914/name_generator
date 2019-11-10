import numpy as np
import requests
from scraper import Scraper
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import LambdaCallback

scraper = Scraper()
datas = scraper.load_csv("csv/en_jp_names_test.csv")
names = [data[1] + "." for data in datas]
# print(names[:10])

first_num_of_katakana = 12448
num_of_katakana = 83

char_to_index = dict((chr(i+first_num_of_katakana), i) for i in range(1,num_of_katakana + 1))
char_to_index[' '] = 0
char_to_index['ー'] = num_of_katakana + 1
char_to_index['.'] = num_of_katakana + 2

index_to_char = dict((i, chr(i+first_num_of_katakana)) for i in range(1,num_of_katakana + 1))
index_to_char[0] = ' '
index_to_char[num_of_katakana + 1] = 'ー'
index_to_char[num_of_katakana + 2] = '.'

max_char = len(max(names, key=len))
m = len(names)
char_dim = len(char_to_index)

X = np.zeros((m, max_char, char_dim))
Y = np.zeros((m, max_char, char_dim))

for i in range(m):
    name = list(names[i])
    for j in range(len(name)):
        X[i, j, char_to_index[name[j]]] = 1
        if j < len(name)-1:
            Y[i, j, char_to_index[name[j+1]]] = 1

model = Sequential()
model.add(LSTM(256, input_shape=(max_char, char_dim), return_sequences=True))
model.add(Dense(char_dim, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

def make_name(model):
    name = []
    x = np.zeros((1, max_char, char_dim))
    end = False
    i = 0

    while end == False:
        probs = list(model.predict(x)[0, i])
        probs = probs / np.sum(probs)
        index = np.random.choice(range(char_dim), p=probs)
        if i == max_char - 2:
            character = '.'
            end = True
        else:
            character = index_to_char[index]
        name.append(character)
        x[0, i + 1, index] = 1
        i += 1
        if character == '.':
            end = True

    print(''.join(name))


def generate_name_loop(epoch, _):
    if epoch % 25 == 0:

        print('Names generated after epoch %d:' % epoch)

        for i in range(10):
            make_name(model)

        print()

name_generator = LambdaCallback(on_epoch_end = generate_name_loop)
model.fit(X, Y, batch_size=128, epochs=1000, callbacks=[name_generator], verbose=0)