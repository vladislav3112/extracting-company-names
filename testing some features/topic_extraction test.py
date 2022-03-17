import nltk
import pandas as pd
import gensim
from nltk.corpus import stopwords  #stopwords
from nltk.stem import WordNetLemmatizer  
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
stop_words=set(nltk.corpus.stopwords.words('english'))
nltk.download('wordnet')
article = "Microsoft Corp (MSFT.O) will begin selling its ""Kinect"" motion-sensing game system on Nov. 4, before the crucial holiday season, hoping to lure new and casual players to the Xbox and steal a march on rivals Nintendo Co Ltd 7974.OS and Sony Corp (6758.T) (SNE.N). The world largest software vendor, which has ambitions of making its Xbox 360 not just a gaming device but a hub of home video and Web entertainment, will also begin selling a smaller, same-priced version of the console this week. Microsoft would not say how much Kinect -- which plugs into Xboxes and lets players control games with body and hand gestures -- will sell for, though analysts estimates range from $50 to $200. Executives said 15 titles from developers including Electronic Arts Inc ERTS.O and Ubisoft Entertainment SA (UBIP.PA) will be available at the time of launch. Ahead of this week Electronic Entertainment Expo convention in Los Angeles, Microsoft offered sneak peaks of upcoming titles, including a LucasArts game in which Jedi Knights do battle with light sabers, and a fitness program that lets players compete in sports from bowling to sprinting. The world leading gaming hardware makers, hoping to reignite the slumping $60 billion industry, will unveil a plethora of futuristic gadgets at the E3 convention. The rush of technology comes just as the video game industry, which dwarfs the $10 billion domestic movie box office, needs it. U.S. industry sales -- hardware, software and accessories -- are down more than 10 percent at $4.7 billion this year through April, according to research firm NPD Group. < E3 FACTBOX [IDnN14206793] Graphics showing share performance of games industry link.reuters.comtab99k > Microsoft also said on Monday it had struck a deal with Walt Disney Co (DIS.N) ESPN network to broadcast live sporting events into U.S. living rooms through the Xbox 360 games console, bypassing traditional cable providers. Live games will be broadcast through Microsoft Xbox Live service, and will be offered at no additional cost. It already offers Netflix (NFLX.O) movies and Zune music and videos through its Xbox Live online subscription service. There has been talk that it will announce a deal to add Hulu TV shows to the service at E3. [IDnN0899538] The arrival of Kinect may pressure Nintendo, which pioneered motion-sensing gaming through an all-purpose controller with its Wii system. Nintendo is expected to unveil more details on its 3D games system that requires no glasses at E3 [IDnN09169766]. ""This year E3 gives the gaming industry the first real opportunity to prove that it not just about making shoot-em-up games for testosterone-fueled boys,"" Forrester Research analyst James McQuivey said. ""This is because the secret to the gaming industry future is the realization that game consoles are the most powerful device in the living room,"" he wrote in a note. A HIGH BAR? In a surprise announcement, Microsoft also showed off a more compact, higher-capacity Xbox console that will ship to retailers on Monday and be available to consumers this week. With a 250-gigabyte hard drive, the console will carry the same price tag of $299. At the same time, Microsoft will slash $50 off the price of lower-capacity Xbox models -- the Xbox 360 Arcade and Xbox 360 Elite -- to $149.99 and $249.99, respectively. That makes them more affordable than the roughly $300 PlayStation -- though it comes with more capacity -- and in good shape against the roughly $199 Wii. Electronic Entertainment Design and Research analyst Jesse Divnich said Microsoft set a high bar ahead of announcements from Nintendo and Sony this week. ""This presentation was a great sign of how Microsoft is transforming the Xbox into being a real entertainment platform,"" he said. ""In a sense, they are trying to reinvent the Xbox 360, have it appeal to a broader audience."" Sony is expected to unveil its ""Move"" platform, which will compete with Kinect and Wii. Shares of Microsoft fell 0.64 percent to close at $25.50 on Nasdaq. Disney fell 0.9 percent to $33.93 and Sony slipped 0.7 percent to $28.40 on the New York Stock Exchange. Microsoft Kinect is a three-camera system that plugs into Xbox and allows for hands-free games and controlling the console with voice commands. The platform, if it works well, takes gamers a step beyond Nintendo Wii. Some may have been disappointed by the lack of blockbuster franchises -- such as Activision Blizzard Inc (ATVI.O) ""Call of Duty"" -- in the initial wave of releases for Kinect, but executives said that was a conscious decision. Electronic Arts also announced on Monday it was developing a fitness game called Active 2 for Kinect, due for release in November. At a news conference, the company outlined updates to its Medal of Honor, Madden NFL and Need for Speed franchises, with an appearance by football great Joe Montana. ""The last thing I want to do is take a franchise that strong and shove something in it too quickly,"" said Phil Spencer, vice president of Microsoft Game Studios. ""We want to put Kinect in the hands of creators (of Call of Duty and so on) and see what magic they come up with."" Janco Partners analyst Mike Hickey said, ""The fitness and dance games are both potential killer applications, driving a reasonably strong Kinect attach rate to the existing installed base and early adopters. ""The ESPN deal is huge, and the social networking applications Kinect offers are potentially powerful for driving initial adoption and loyalty,"" he said. (Reporting by Franklin Paul and Gabriel Madway; Writing by Edwin Chan; Editing by Richard Chang, Leslie Gevirtz)"

df_news = pd.read_csv('nasdaq_labeled_news.csv',index_col=False)
news_list = df_news['News'][43175:43195]
print(WordNetLemmatizer().lemmatize("laboratory"))
print(WordNetLemmatizer().lemmatize("lab"))
print(WordNetLemmatizer().lemmatize("cos"))
print(WordNetLemmatizer().lemmatize("company"))
def clean_text(headline):
    le=WordNetLemmatizer()
    word_tokens=word_tokenize(headline)
    tokens=[le.lemmatize(w) for w in word_tokens if w not in stop_words and len(w)>3]
    cleaned_text=" ".join(tokens)
    return cleaned_text
df_news['cleaned_text'] = df_news['News'].apply(clean_text)
vect =TfidfVectorizer(stop_words=stop_words,max_features=1000)
vect_text=vect.fit_transform(df_news['cleaned_text'])



lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))



# from sklearn.decomposition import LatentDirichletAllocation
# lda_model=LatentDirichletAllocation(n_components=10,
# random_state=42,max_iter=1) 
# lda_top=lda_model.fit_transform(vect_text)
# print("Document 0: ")
# for i,topic in enumerate(lda_top[0]):
#   print("Topic ",i,": ",topic*100,"%")
# df_topics = pd.DataFrame(data = lda_top)
# df_topics.to_csv("topics.csv")

# vocab = vect.get_feature_names()
# for i, comp in enumerate(lda_model.components_):
#      vocab_comp = zip(vocab, comp)
#      sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:10]
#      print("Topic "+str(i)+": ")
#      for t in sorted_words:
#             print(t[0],end=" ")