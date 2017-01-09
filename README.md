# osu-mapper
osu!mapper

## TODO

### osu Format File [Liwen]
- Slider end time
- Slider points((X, Y) in the path)
- v6 ~ v14(need to generalize, output format: v14)
- HitSounds
- Lines under editor


### Model [Jun]
Use RNN-like model. State h_0 = some hyper-parameters in osu file and features of music. Input X = features of music segmentations. Output = state h_1 .. h_n, which can be mapped to osu file(use a matrix and a tool).
- Space modeling
  - Map state to a 2d vector
- Model of slider(length should be legal)
  - Length don't need to be legal(velocity is not fixed)
- Model with more prior
  - e.g. points are related

### Music [Jiong]
- Basic concepts
  -  timbre 音色: 音色主要决定于声音频谱对人的刺激，但也决定于波形、声压、频谱的频率位置和频谱对人的时间性刺激
  -  rhythem 节奏:
  -  pitch information 音高:
- Process(how?)
  - Feature: MFCC ([Tutorial][MFCC-tutorial])
    - A [survey](http://ieeexplore.ieee.org/document/5664796/)
  - Relative Package:
    - [python speech features](https://github.com/jameslyons/python_speech_features)
    - [librosa](https://github.com/librosa/librosa)
    <del>- [pydub](https://github.com/jiaaro/pydub)</del>
- Music model(for machine learning)



[MFCC-tutorial]: http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/