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
      similar_words = model.wv.most_similar(positive=word, topn=10)
      similar_count = 0
      for similar_word, weight in similar_words:
          vocab_dict[similar_word] = 1
          if weight > 0.7:
             similar_count += 1
             ligne_2_write = ligne_2_write + "," + similar_word
      ligne_2_write = ligne_2_write + "\n"
      vocab_dict[word] = 1
      if similar_count > 1:
         ligne_2_write = ligne_2_write.replace('_', ' ')
         synfile.write(ligne_2_write)
synfile.close()
print("End of generation")

