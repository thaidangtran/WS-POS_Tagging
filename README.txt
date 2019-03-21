Run program:
python main.py [input_file] [output_file] [option]

option = "ws": running only word segmentation.
example: python main.py sample.txt sample.ws.txt ws
option = "pos": runing word segmentation, after that run part-of-speech tagging.
example: python main.py sample.txt sample.pos.txt pos

=================================================================================
training HMM model
python train.py [training_file]
example: python train.py sample.pos.txt
The generated files
+ pos_bigram.txt
+ pos_emission.txt
+ pos_lexicons.txt
+ pos_tagset.txt
+ pos_trigram.txt
+ pos_unigram.txt
if you want to use new trained model copy all files above to folder pos_data.