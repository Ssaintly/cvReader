from PyPDF2 import PdfReader
import spacy
from spacy import displacy
from spacy.util import filter_spans
from spacy.tokens import DocBin
from tqdm import tqdm
import re
import os
from minibatch_data import minibatch_data 
from sklearn.model_selection import train_test_split




nlp = spacy.load("en_core_web_sm")
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe("ner")



directory_path = os.path.abspath('cvs_pdf')

# Names = []
names = []
Information = []
number = 0

# # LOL = minibatch_data[0][1]["entities"][0]
# # print(LOL)

# # TRAINING NEW ENTITIES-----------------------------------------------------------------------------------------

ner.add_label("JOB_TITLE")
ner.add_label('PERSON')
# doc_bin = DocBin()
# texts, annotations = zip(*minibatch_data)


# train_texts, remaining_texts, train_annotations, remaining_annotations = train_test_split(
#     texts, annotations, train_size=0.7, random_state=123)

# valid_texts, test_texts, valid_annotations, test_annotations = train_test_split(
#     remaining_texts, remaining_annotations, test_size=0.5, random_state=123)



# train_data = []
# for text, annotations in zip(train_texts, train_annotations):
#     train_data.append((text, annotations))

# valid_data = []
# for text, annotations in zip(valid_texts, valid_annotations):
#     valid_data.append((text, annotations))

# test_data = []
# for text, annotations in zip(test_texts, test_annotations):
#     test_data.append((text, annotations))




# Training_data = []
# for example in minibatch_data:
#     temp_dict = {}
#     temp_dict['text'] = example[0]
#     temp_dict['entities'] = []
#     for annotation in example[1]['entities']:
#         start = annotation[0]
#         end = annotation[1]
#         label = annotation[2].upper()
#         temp_dict['entities'].append((start, end, label))
#     Training_data.append(temp_dict)
# # print(Training_data)


# optimizer = nlp.begin_training()
# for training_example in tqdm (Training_data):
#     text = training_example['text']
#     doc = nlp.make_doc(text)
#     ents = []
#     for start,end,label in training_example["entities"]:
#         span = doc.char_span(start, end, label= label, alignment_mode= "contract")
#         if span :
#             ents.append(span)

#     filtered_ents = filter_spans(ents)
#     doc.ents = filtered_ents
#     doc_bin.add(doc)

# doc_bin.to_disk("train.spacy")

# nlp_ner = spacy.load("output/model-best")

        






# PDF EXTRACTION IN A LOOP--------------------------------------------------------------------------------------------------

for filename in os.listdir(directory_path):      #looping inside directory through PDF Files
    # print(filename, '\n')
    if filename.endswith('.pdf'):           
        with open(os.path.join(directory_path, filename), 'rb') as pdf_file:
            reader = PdfReader(pdf_file)             #extracting text

            page_text = ''

            for page in reader.pages:
                page_text += page.extract_text()

                

            doc = nlp(page_text)
            number = number+1
            
            





            # EXTRACTING SKILLS--------------------------------------------------------------------------------

            skills = []
            patterns = ["\n","\\n", "➢","-", ":", "✓", "❖","/","•"]

            
            for chunk in doc.noun_chunks:
                if 'skill' in chunk.text.lower() or 'expertise' in chunk.text.lower():
                    skills.append(chunk.text)
                for i in range(len(skills)):
                    for pattern in patterns:
                        skills[i] = skills[i].replace(pattern, "")
                
                clean_skills = [s.replace('\n', '') for s in skills]
                clean_skills = [s.replace('\s+', ' ')for s in clean_skills]
                skills = clean_skills
            

            if(number == 4):
                print(page_text)
            






            #  EXTRACTING POSITIONS-------------------------------------------------------------------------------

#             # positions = []
#             # for entity in doc.ents:
#             #     if entity.label_ == 'JOB_TITLE':
#             #         positions.append(entity.text)

#             # print('Positions:', positions)








            # EXTRACTING NAMES-------------------------------------------------------------------------------------------
            
            # for ent in doc.ents:
            #     if ent.label_ == 'PERSON':
            #         names.append(ent.text)
            
            # print(names)
            # names =[]








            #EXTRACTING EMAIL-----------------------------------------------------------------------------------------
            email=[]
            email_regex = r'\b[A-Za-z0-9._%+-.]+(\s{0,2})[A-Za-z0-9._%+-]+\b(\s{0,2})@(\s{0,2})[A-Za-z0-9-.\s]+\.[A-Z|a-z\s]{2,4}\b'

            for email_match in re.finditer(email_regex, page_text):
                if email_match is not None:
                    email_str = email_match.group(0)
                    rem = ["E-mail-", " ","  ","Email -","I D-","Email-","ID-","EmailId-","Id-"]
                    for a in rem:
                        if a in email_str:
                            email_str = email_str.replace(a, "")
                    email_str = email_str.split('\n', 1)[0]
    
                    if email_str not in email:
                        email.append(email_str)
                    
                    
                





            
# #             # EXTRACTING PHONE NUMBERS----------------------------------------------------------------------------------
            phoneNums = []
            k = ""
            phone_match = "(?:(?:\+|0{0,2})91(\s*)?(\s*[\\-]\s*)?|[0]\s?)?[789](\s*)\d{1,}\s*\d{1,}\s*\d{1,}\s*\d{1,}\s*\d{1,}"
            matches = re.finditer(phone_match, page_text)#Capture all the matches in the lines or the file f.
            rem = ["\t","  ","-"," "]
            for match in matches:              	#Traverse through matches tuple and printing all the matched mobile numbers 
                phone_no = "{match}".format(match = match.group(0))
                for a in rem:
                    if a in phone_no:
                        phone_no = phone_no.replace(a, "")
                if "\n" in phone_no:
                    phone_no = phone_no.split("\n")
                    k = phone_no[1]
                    phone_no = phone_no[0]
                # if(number == 10):
                n = 2
                while(n>0):
                    n-= 1
                    length = len(phone_no)
                    
                    if length >=10 and length < 24 and phone_no not in phoneNums:
                        
                        phoneNums.append(phone_no)
                        if k :
                            phone_no = k

                



            

            # SEQUENCING AND STORING INFORMATION-----------------------------------------------------------------------
            current = []
            current.append(number)
            if email:
              current.append(email)
            current.append(phoneNums)
            if skills:
              current.append(skills)
            
            # print(number," ",skills)
            Information.append(current)


# print(Information)
