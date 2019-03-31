import os
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
MAX_SENT_LEN_CHARS = 200
MAX_FROM_ONE_DOC = 2000

if __name__ == "__main__":
    with open("docs_berty.txt", "w") as outf:
        is_first_file = True
        for filename in tqdm(os.listdir("./data")):
            if not is_first_file:
                outf.write("\n\n")
            is_first_file = False
            with open(f"./data/{filename}") as f:
                lines = f.readlines()
            filedata = "".join(lines)
            sents = sent_tokenize(filedata)
            # Split by new lines
            new_sents = []
            for sent in sents:
                new_sents.extend(sent.split("\n"))
            sents = new_sents
            # try and split really long lines
            new_sents = []
            for sent in sents:
                if len(sent) > MAX_SENT_LEN_CHARS:
                    if "," in sent:
                        comas = sent.split(",")
                        new_sents.append(comas[0])
                        new_sents.extend(["," + s for s in comas[1:]])
                    else:
                        new_sents.extend(sent.split(" "))
                else:
                    new_sents.append(sent)
            sents = new_sents
            # reset remove only blank lines
            sents = [x.strip() for x in sents if x != "\n" and len(x) > 0]
            # merge short sents
            new_sents = []
            new_sent = ""
            for sent in sents:
                if len(new_sent) > 0 and (len(new_sent) > 60 or len(new_sent + sent) > 150):
                    if len(new_sent) > MAX_SENT_LEN_CHARS:
                        break
                    new_sents.append(new_sent)
                    new_sent = ""
                new_sent += " " + sent
            if 0 < len(new_sent) < MAX_SENT_LEN_CHARS:
                new_sents.append(new_sent)
            sents = new_sents
            sents = [x.replace("\n", " ").strip()
                     for x in sents
                     if x.strip() != "\n" and len(x.strip()) > 0]
            # Don't have too short docs
            if len(sents) < 3:
                continue
            sents = sents[:min(len(sents, MAX_FROM_ONE_DOC))]
            outf.writelines("\n".join(sents))
