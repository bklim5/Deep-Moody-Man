# Deep-Moody-Man
Deep Q-Learning Network with Keras (Theano backend) to play the Moody Man.

I refer a lot to yanpanlau's code here https://github.com/yanpanlau/Keras-FlappyBird/blob/master/README.md. Thanks yanpanlau!

You can refer to some info about Q-learning in my blog: https://blog.bkbklim.com/2017/10/11/deep-moody-man/

```
Python 2.7
Keras==2.0.3
pygame==1.9.3
scikit-image==0.13.1
Theano==0.9.0
```

I have the following config in my ~/.keras/keras.json to run Theano as backend
```
{
    "epsilon": 1e-07,
    "floatx": "float32",
    "image_data_format": "channels_last",
    "backend": "theano",
    "image_dim_ordering": "th"
}
```

# How to use this repo
clone this repo and cd into it, then
```
to run: python dqlearning -m Run
to train: python dqlearning -m Train
```

you can also specify a model file to be use for running. If the mode flag is Train it will continue to train based on the loaded model weight. 
```
python dqlearning -m Train -f "models/model-90000.h5"
```

I don't have a GPU machine so I didn't try the GPU version before, sorry.. 

