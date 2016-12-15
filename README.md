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
- Process(how?)
- Music model(for machine learning)
