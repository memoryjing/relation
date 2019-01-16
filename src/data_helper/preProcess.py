from nltk.tokenize import sent_tokenize,word_tokenize
import nltk

sentence="Possible Therapeutic Uses of Salvia triloba and Piper nigrum in Alzheimer's Disease-Induced Rats.	Abstract This study aimed to investigate the role of Salvia triloba L. and Piper nigrum extracts in ameliorating neuroinflammatory insults characteristic of Alzheimer's disease (AD) in an experimentally induced rat model. Adult male Sprague-Dawley rats were classified into Group 1 (n=10): normal healthy animals serving as the negative control group; Group 2 (n=60): the AD-induced group. After AD induction, animals in the AD-induced group were divided randomly and equally into 6 subgroups. The first subgroup served as AD control; the second one, which served as positive control, was treated orally with the conventional therapy for AD (rivastigmine) at a dose of 0.3 mg/kg body weight (b.w.) daily for 3 months. The third and fourth subgroups were, respectively, treated orally with the S. triloba extract at a dose of 750 and 375 mg/kg b.w. daily for 3 months. The fifth and sixth subgroups were, respectively, treated orally with the P. nigrum extract at a dose of 187.5 and 93.75 mg/kg b.w. daily for 3 months. Levels of brain acetylcholine (Ach), serum and brain acetylcholinesterase (AchE) activity, C-reactive protein (CRP), total nuclear factor kappa-B (NF-κB), and monocyte chemoattractant protein-1 (MCP-1) were estimated. The results showed that administration of AlCl3 resulted in a significant elevation in the levels of AchE activity, CRP, NF-κB, and MCP-1 accompanied with a significant depletion in the Ach level. Treatment of AD rats with each of the selected medicinal plant extracts caused marked improvement in the measured biochemical parameters. In conclusion, S. triloba and P. nigrum methanolic extracts have potent anti-inflammatory effects against neuroinflammation characterizing AD."
print(sentence)

sentences=sent_tokenize(sentence,language='english')
for i,sentence in enumerate(sentences):
    print("{}:{}".format(i,sentence))

sentence=sentences[11]
print("\nexample-sentences:\n{}".format(sentence))
print("\nencoding:\n{}".format(sentence.encode("utf-8").decode('utf-8')))

# print("{0}".format(' '.join(word)))