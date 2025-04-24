from flask import Flask, render_template, request
import requests
from gensim.summarization import summarize
import re
from PyPDF2 import PdfFileReader
from videoSummarizer.preprocess import get_text_from_video

from textSummarizer.preprocess import webprocess, query
app = Flask(__name__)


@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == "POST":
        input_string = request.form['input']
        print(input_string)

        #check if user input is website or plain text:
        website = re.match("^http*", input_string)

        #if it's a website:
        if website: 
            if 'youtube.com' in str(input_string):
                webpage= get_text_from_video(input_string)
                print(webpage)
                articel_processed = str(webpage).replace(',',' ').replace('"','').replace("'",'')

                gensim_summary = summarize(articel_processed, ratio = 0.1)
                abstract = query([articel_processed])

                print(f"abstract.............. is {abstract}")
                print(f"type.............. is {type(abstract)}")

                iter = 0
                while isinstance(abstract, list) == False and iter < 15:  
                    abstract = query([articel_processed])
                    print("................getting cache!!! ")
                    iter =+1

                try: 
                    output_summary = abstract[0]
                except:
                    output_summary = {"summary_text": "Sorry, the server is busy, please go to back to homepage, refresh and try again. "}
                
                return render_template("result.html", text = articel_processed, summary = output_summary['summary_text'], gensim_summary = gensim_summary )
            else:
                webpage= requests.get(input_string).text
                articel_processed = webprocess(webpage)

                gensim_summary = summarize(articel_processed, ratio = 0.1)
                abstract = query([articel_processed])

                print(f"abstract.............. is {abstract}")
                print(f"type.............. is {type(abstract)}")

                iter = 0
                while isinstance(abstract, list) == False and iter < 15:  
                    abstract = query([articel_processed])
                    print("................getting cache!!! ")
                    iter =+1

                try: 
                    output_summary = abstract[0]
                except:
                    output_summary = {"summary_text": "Sorry, the server is busy, please go to back to homepage, refresh and try again. "}
                
                return render_template("result.html", text = articel_processed, summary = output_summary['summary_text'], gensim_summary = gensim_summary )
       
        #if input is plain text
        else:     
            #if not empty
            if len(input_string) >0:
                abstract = query([input_string])

                iter = 0
                while isinstance(abstract, list) == False and iter < 15:
                    abstract = query([input_string])
                    print("................Retry and getting cache from API server!!! ")
                    iter +=1
                
                try: 
                     output_summary = abstract[0]
                except:
                     output_summary = {"summary_text": "Sorry, the server is busy, please go to back to homepage, refresh and try again. "}

                gensim_summary = summarize(input_string, ratio =0.1)

                if len(gensim_summary) !=0: 
                    return render_template("result.html", text = input_string, summary = output_summary['summary_text'], gensim_summary = gensim_summary)
                
                else:              
                    return render_template("result.html", text = input_string, summary = output_summary['summary_text'], gensim_summary = "Sorry, no extractive summary generated because input texts doesn't meet the mininum length requirement.")


            else:
                return render_template("result.html", text=  "", summary = "", gensim_summary = "")
 
    else: 

        return render_template("result.html", text = "", summary = "", gensim_summary = "")

@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        mylist = []
        gensim_summary1 = []
        output_summary = "Sorry, the server is busy, please go to back to homepage, refresh and try again. "
        if 'pdf' in request.files:
            text = PdfFileReader(request.files['pdf'])
            numOfPages = text.getNumPages()
            mylist1 = [((text.getPage(i)).extractText())for i in range(numOfPages)]
            mylist1 = str(mylist1)
            mylist1 = mylist1.replace('\n', ' ').replace('\\n', ' ')
            mylist.append(mylist1)
            gensim_summary = summarize(str(mylist), ratio = 0.1)
            gensim_summary = gensim_summary.replace('\n', ' ')
            gensim_summary1.append(gensim_summary)
            abstract = query([mylist])


            iter = 0
            while isinstance(abstract, list) == False and iter < 15:  
                abstract = query([mylist])
                print("................getting cache!!! ")
                iter =+1

            try: 
                output_summary = abstract[0]
            except Exception as e:
                print(e)
                output_summary = {"summary_text": "Sorry, the server is busy, please go to back to homepage, refresh and try again. "}
            
        return render_template("result.html", text = mylist, summary = output_summary[0]['summary_text'], gensim_summary = gensim_summary1[0])


        
@app.route('/model')
def model():
    return render_template( "index.html")

@app.route('/', methods=['POST','GET'])
def intro():
    return render_template("intro.html")

@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
    return render_template('pdfupload.html')

@app.route('/contact', methods=['POST','GET'])
def contact():
    return render_template("contact.html")

@app.route('/error', methods=['POST','GET'])
def error():
    return render_template( "500.html")

if __name__ == '__main__':
	app.run(debug = True, port=8000)