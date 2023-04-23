#Code from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer, util

#Example code to compare two sentences
"""
sentences = ["Stubbing your toe can be painful and uncomfortable, but fortunately, most stubbed toes will heal on their own within a few days. Here are a few things you can do to ease the discomfort and speed up the healing process: Elevate the affected foot: Keep the foot elevated to reduce swelling. Apply ice: Wrap ice in a towel and place it on the affected area for 15-20 minutes at a time to reduce pain and swelling. Take pain relievers: Over-the-counter pain relievers such as ibuprofen or acetaminophen can help to reduce pain and inflammation. Rest: Avoid activities that may put pressure on the injured toe. Wear comfortable shoes: Wear shoes that are comfortable and don't put pressure on the injured toe. If your toe is severely injured or you are experiencing severe pain or swelling, it's best to seek medical attention.", "Stubbing your toe can be painful, but there are some things you can do to help alleviate the pain and promote healing: Elevate your foot: Try to elevate your foot to reduce swelling and pain. Apply ice: Applying ice to the affected area can help reduce swelling and alleviate pain. Use a cloth or towel to wrap the ice before applying it to your skin. Take pain relievers: Over-the-counter pain relievers such as acetaminophen, ibuprofen, or aspirin can help reduce pain and inflammation. Rest: Try to stay off your feet as much as possible to allow the injury to heal. Use a topical ointment: Applying a topical ointment, such as aloe vera or arnica gel, can help reduce inflammation and pain. Seek medical attention: If the pain and swelling do not go away or if you suspect a more serious injury, it is best to seek medical attention. Remember, if the pain and swelling persist, or if you have trouble moving your toe or foot, it is important to consult a doctor to ensure that there are no serious injuries."]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

embedding_1 = model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

print(util.pytorch_cos_sim(embedding_1, embedding_2))
"""


#This is the answer I got

#Two texts to compare
textA = "Stubbing your toe can be painful and uncomfortable, but fortunately, most stubbed toes will heal on their own within a few days. Here are a few things you can do to ease the discomfort and speed up the healing process: Elevate the affected foot: Keep the foot elevated to reduce swelling. Apply ice: Wrap ice in a towel and place it on the affected area for 15-20 minutes at a time to reduce pain and swelling. Take pain relievers: Over-the-counter pain relievers such as ibuprofen or acetaminophen can help to reduce pain and inflammation. Rest: Avoid activities that may put pressure on the injured toe. Wear comfortable shoes: Wear shoes that are comfortable and don't put pressure on the injured toe. If your toe is severely injured or you are experiencing severe pain or swelling, it's best to seek medical attention."
textB = "Stubbing your toe can be painful, but there are some things you can do to help alleviate the pain and promote healing: Elevate your foot: Try to elevate your foot to reduce swelling and pain. Apply ice: Applying ice to the affected area can help reduce swelling and alleviate pain. Use a cloth or towel to wrap the ice before applying it to your skin. Take pain relievers: Over-the-counter pain relievers such as acetaminophen, ibuprofen, or aspirin can help reduce pain and inflammation. Rest: Try to stay off your feet as much as possible to allow the injury to heal. Use a topical ointment: Applying a topical ointment, such as aloe vera or arnica gel, can help reduce inflammation and pain. Seek medical attention: If the pain and swelling do not go away or if you suspect a more serious injury, it is best to seek medical attention. Remember, if the pain and swelling persist, or if you have trouble moving your toe or foot, it is important to consult a doctor to ensure that there are no serious injuries."

#Split these into multiple sentences
sentencesA = textA.split(".")
sentencesB = textB.split(".")

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

Scores = 0.0
sentenceCount = 0

#Compare each sentence with the other sentences given
for sentenceA in sentencesA:
    for sentenceB in sentencesB:
        embedding_1 = model.encode(sentenceA, convert_to_tensor=True)
        embedding_2 = model.encode(sentenceB, convert_to_tensor=True)
        newScore = util.pytorch_cos_sim(embedding_1, embedding_2)
        Scores += newScore
        sentenceCount += 1

        #Print average given
print(Scores / sentenceCount)

#I got this solution because comparing two lists of split texts gave me an array that showed it comparing every sentence to every other sentence
