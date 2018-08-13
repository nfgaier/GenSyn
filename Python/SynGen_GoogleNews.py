#!/usr/bin/python

import sys, getopt

def main(argv):
   max_cluster_size = 0
   similarity_level = 0.0
   model_type = ''
   model_filename = ''
   output_filename = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:m:l:t",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'SynGen.py -i <inputfile> -o <outputfile> -m <max_cluster_size> -l <similarity_level> -t <model_type>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         model_filename = arg
      elif opt in ("-o", "--ofile"):
         output_filename = arg
      elif opt in ("-m", "--max"):
         max_cluster_size = arg
      elif opt in ("-l", "--level"):
         similarity_level = arg
      elif opt in ("-t", "--type"):
         model_type = arg
   print 'Input file is "', model_filename
   print 'Output file is "', model_type
   print 'Output file is "', output_filename
   print 'Output file is "', max_cluster_size
   print 'Output file is "', similarity_level
   

if __name__ == "__main__":
   main(sys.argv[1:])

from gensim.models import KeyedVectors



# load the google word2vec model
filename = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)
# display vocabulary size
vocab_size = len(model.wv.vocab)
print("There is ", vocab_size, " words to process")
vocab_dict = dict([(word, 0) for (word, vobj) in model.wv.vocab.items()])
#print(len(vocab_dict))
#print(vocab_dict[:10])
#print(vocab_dict['the'])

print("Generating cluster of synonyms ...")
synfile = open("google_word2vec_syn.txt", "w")
current = 0
for word in vocab_dict:
#   print(word)
   current = current + 1
   print('Current word vec [%d]\r'%current, end = "")
#   print(current)
   ligne_2_write = word
   if not vocab_dict[word]:
      similar_words = model.wv.most_similar(positive=word, topn=max_cluster_size)
      similar_count = 0
      for similar_word, weight in similar_words:
          vocab_dict[similar_word] = 1
          if weight > similarity_level:
             similar_count += 1
             ligne_2_write = ligne_2_write + "," + similar_word
      ligne_2_write = ligne_2_write + "\n"
      vocab_dict[word] = 1
      if similar_count > 1:
         ligne_2_write = ligne_2_write.replace('_', ' ')
         synfile.write(ligne_2_write)
synfile.close()
print("End of generation")

