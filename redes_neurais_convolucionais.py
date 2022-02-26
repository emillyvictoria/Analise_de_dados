# -*- coding: utf-8 -*-
"""Redes Neurais Convolucionais.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ezU_35C4dxMb3z2S4L23sbWdn4M0qByH
"""

!pip3 install -q kaggle

import numpy as np
import pandas as pd
import os
import random 
from shutil import copyfile
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread
from sklearn.utils import shuffle
import seaborn as sns

from tqdm import tqdm

from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from tensorflow.keras import backend as K 
K.set_image_data_format('channels_last')

"""#Obtenção de dados"""

kjson = pd.read_json('kaggle.json', typ='series')

os.environ['KAGGLE_USERNAME']= "emillyvictoria"
os.environ['KAGGLE_KEY']= kjson.key
#login para fazer o download diretamente de datasets

!kaggle datasets download --force tourist55/alzheimers-dataset-4-class-of-images

!unzip alzheimers-dataset-4-class-of-images.zip

"""#Separação e Visualização"""

testpath ='/content/Alzheimer_s Dataset/test'
trainpath = '/content/Alzheimer_s Dataset/train'
#copiando o caminho

os.listdir(trainpath)
#os: biblioteca que conversa com o SO de forma mais inteligente que o python
#a função listdir lista tudo que tem na pasta que especificamos

os.listdir(trainpath + '/NonDemented')

example_path = trainpath + '/NonDemented/nonDem882.jpg'
example_img = cv2.imread(example_path)
#cv2: biblioteca que lida muito bem com imagens 2d 

plt.imshow(example_img)
plt.title('Non Demented')
plt.show()

example_img.shape
#208x176 e 3 é a escala de cor RGB
#obs: quando a escala é 1 significa que a imagem é preto e branco somente

example_img
#números por trás da imagem

example_folder_path = trainpath + '/VeryMildDemented'
example_path = example_folder_path + "/" + os.listdir(example_folder_path)[0]
example_img = cv2.imread(example_path)

plt.imshow(example_img)
plt.title('Very Mild Demented')
plt.show()

train_path_list = []
test_path_list = []

ytrain = []
ytest =[]
#esse código cria uma lista de caminhos para treino e teste e depois definimos as targets

for i in os.listdir(trainpath + '/NonDemented'):
  path = trainpath + '/NonDemented' + '/' + i
  train_path_list.append
  ytrain.append(0)
#percorre todos os itens da pasta "trainpath + '/NonDemented'"
#o i é sempre um item do jpeg
#path = trainpath + '/NonDemented' + '/' + i --> camonho até as imagens de treino
#train_path_list.append --> vai add na lista


for i in os.listdir(trainpath + '/ModerateDemented'):
  path = trainpath + '/ModerateDemented' + '/' + i
  train_path_list.append
  ytrain.append(1)

for i in os.listdir(trainpath + '/MildDemented'):
  path = trainpath + '/MildDemented' + '/' + i
  train_path_list.append
  ytrain.append(2)

for i in os.listdir(trainpath + '/VeryMildDemented'):
  path = trainpath + '/VeryMildDemented' + '/' + i
  train_path_list.append
  ytrain.append(3)

for i in os.listdir(testpath + '/NonDemented'):
  path = testpath + '/NonDemented' + '/' + i
  test_path_list.append
  ytest.append(0)

for i in os.listdir(testpath + '/ModerateDemented'):
  path = testpath + '/ModerateDemented' + '/' + i
  test_path_list.append
  ytest.append(1)

for i in os.listdir(testpath + '/MildDemented'):
  path = testpath + '/MildDemented' + '/' + i
  test_path_list.append
  ytest.append(2)

for i in os.listdir(testpath + '/VeryMildDemented'):
  path = testpath + '/VeryMildDemented' + '/' + i
  test_path_list.append
  ytest.append(3)

for i,j in enumerate (['a','b','c']):
  print (i,j)

train_path_list = []
test_path_list = []

ytrain = []
ytest =[]

for num_classe,classe in enumerate(os.listdir(trainpath)):

  for jpg in os.listdir(trainpath + '/' + classe):
    path = trainpath + '/' + classe +  '/' + jpg
    train_path_list.append(path)
    ytrain.append(num_classe)

for num_classe,classe in enumerate(os.listdir(testpath)):
  
  for jpg in os.listdir(testpath + '/' + classe):
    path = testpath + '/' + classe +  '/' + jpg
    test_path_list.append(path)
    ytest.append(num_classe)

len(train_path_list)

len(test_path_list)

"""#Shuffle"""

#o shuffle randomiza um pouco os dados que listamos
train_path_list, ytrain = shuffle(train_path_list, ytrain, random_state = 42)
test_path_list, ytest = shuffle(test_path_list, ytest, random_state= 42)

ytrain [:20]

"""#Dimensão e Visualização"""

dimensao_1 = []
dimensao_2 = []
#gera uma array de dimensão

for image_filename in tqdm(train_path_list):
    img = imread(image_filename)
    try:
      eixo_1, eixo_2 = img.shape
    except:
      eixo_1, eixo_2, cor = img.shape
    dimensao_1.append(eixo_1)
    dimensao_2.append(eixo_2)
#percorre as imagens de teste
#tqdm é a barrinha de %

sns.jointplot(dimensao_1,dimensao_2)
#cria um scaterplot com a dimensão de um histograma
#de acordo com o gráfico, infere-se que todos os dados tem a mesma dimensaõ pois só tem uma bolinha no centro

"""#Transfromar path em arrays"""

# Vale a pena testar diferentes shapes e ver a diferença de resultados.
# Muitas vezes dimensões reduzidas reduzem a quantidade de parâmetros necessários sem perder performance no modelo.

#dim1 = 208
#dim2 = 176

dim1 = 64
dim2 = 64

#transforma os caminhos em imagens em si
Xtrain = []
Xtest = []

for i in train_path_list:
  image = cv2.imread(i) #transforma o i (caminho) em imagem
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #muda a cor da imagem para cinza
  image = cv2.resize(image, (dim1, dim2)) #muda o tamanho das imagens para as dimensões acima

  Xtrain.append(image)

for i in test_path_list:
  image = cv2.imread(i)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  image = cv2.resize(image, (dim1, dim2))

  Xtest.append(image)

Xtrain = np.array(Xtrain)/255
Xtest = np.array(Xtest)/255

Xtrain.shape

Xtrain = Xtrain.reshape(-1,dim1,dim2,1)
Xtest = Xtest.reshape(-1,dim1,dim2,1)
#adicionando o 1 (COR)

Xtrain.shape

"""#Multiclass y"""

ytrain[:5]

ycat_train = to_categorical(ytrain,4)
ycat_test = to_categorical(ytest,4)
#transoforma em categoria

ycat_train[6]

"""#CNN"""

#adicionando camadas
model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3,3),input_shape=(dim1,dim2,1), activation='relu'))#convolução: filtro que passa pelos pixels da imagem
model.add(MaxPooling2D(pool_size=(2, 2))) #reduz a dimensão capturando as features mais importantes, ou seja, as maiores

model.add(Flatten()) #transforma tudo em uma dimensão somente

model.add(Dense(256))
model.add(Activation('relu'))

model.add(Dense(4))
model.add(Activation('softmax'))

model.compile(optimizer='adam', #indica oq o modelo pode fazer para melhorar
    loss='categorical_crossentropy',
    metrics=['accuracy'])

# categorico: softmax -> loss = 'categorical_crossentropy'
# binario: sigmoid -> loss = 'binary_crossentropy'

model.summary()

bs = 16
results = model.fit(Xtrain, ycat_train, epochs=3, validation_data=(Xtest,ycat_test), batch_size=bs)

"""#Melhorando o modelo"""



model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3,3),input_shape=(dim1,dim2,1), activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2)) #modelo esquece oq ele aprendeu
model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=(dim1,dim2,1), activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(256))


model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(4))
model.add(Activation('softmax'))

model.compile(optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

model.summary()

image_gen = ImageDataGenerator(rotation_range=5,
                               width_shift_range=0.05,
                               height_shift_range=0.05,
                               shear_range=0.05, 
                               zoom_range=0.1, 
                               fill_mode='nearest' 
                              )
#altera levemente a imagem para o modelo treinar com mais dados

#callback
#early_stop = EarlyStopping(monitor='val_loss',patience=10) --> monitora o loss da validação
#se o modelo não melhorar ele simplesmente para quando alcançar seu patience

reduce_lr = ReduceLROnPlateau(monitor = 'val_loss', patience = 20, verbose = 1, factor = 0.5, min_lr = 0.00001)
#aqui ele diminui o fator de aprendizado dps que alcança o seu patience

BS = 16
results = model.fit_generator(image_gen.flow(Xtrain, ycat_train, batch_size=BS),
                              steps_per_epoch=len(Xtrain)/BS, epochs=150,
                              validation_data=(Xtest,ycat_test), callbacks = [reduce_lr])

model.metrics_names

losses = pd.DataFrame(model.history.history)

losses[['loss','val_loss']].plot()
plt.show()

losses[['accuracy','val_accuracy']].plot()
plt.show()

pred = model.predict_classes(Xtest)

prob = model.predict(Xtest)

from sklearn.metrics import classification_report
print(classification_report(ytest, pred))

from sklearn.metrics import confusion_matrix
confusion_matrix(ytest, pred)

!pip install scikit-plot

import scikitplot as skplt
skplt.metrics.plot_roc_curve(ytest, prob, figsize=(8,8), curves='each_class')