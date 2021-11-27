
# Cats and dogs classifier

The dataset contains 3000 images. There are 1500 images of cats and 1500 images of dogs in separate folders.  
The task is to classify these images into either cats or dogs. I used Jupyter notebook to run the code.

## Authors

- [@Qianhua Ma](https://github.com/munakima)


## Requirements

Note: There will not offer any dataset to download.

This code is designed to run Windows system. You would have to install tensorflow by yourself. Tensorflow you can install using pip.
```bash
  pip install tensorflow
```
visualization    
```bash
  pip install opencv-python
```
       
## Split into train, test, and evaluation sets
   
Split data into 70% train, 15% test, and 15% evaluation sets. Seperated copy 1050 cats and dogs images into training dog images dir and training cat images dir respectly, copy 225 cat images and dogs images into validation cat images dir and validation dog images dir respectly, and copy 225 cat images and dogs images into test cat images dir and test dog images dir respectly.
   
## Model building    
Building a convolutional neural network(CNN)     
Layers: Conv2D, MaxPooling2D,Flatten, Dropout,Dense   
Activation: Relu   
   
## Compile and train model   
loss function:binary_crossentropy   
optimizer: RMSprop   
metrics: accuracy

Training the convnet using dataaugmentation generators

## Visualize model training history
    
    
## Prediction
