from flask import Flask, render_template, request, redirect
import webbrowser
import threading
import os
import cohere
from dotenv import load_dotenv
from pathlib import Path
import shutil
import time


last_post_time = time.time()




load_dotenv()
api_key = os.getenv("API_KEY")
co = cohere.Client(api_key)

app=Flask(__name__)
Messages=[]
File_List=[]
File_List = [item.replace('\n', '') for item in File_List] 

command_dict={"open google": "https://www.google.com",
               "open youtube": "https://www.youtube.com",
               "open github": "https://github.com",
               "open linkedin": "https://www.linkedin.com",
               "open twitter": "https://twitter.com",
               "open facebook": "https://www.facebook.com",
               "open instagram": "https://www.instagram.com",
               "open whatsapp": "https://web.whatsapp.com",
               "open telegram": "https://web.telegram.org",
               "open spotify": "https://open.spotify.com",
               "open netflix": "https://www.netflix.com",
               "open gmail": "https://mail.google.com",
               "open amazon": "https://www.amazon.com",
               "open flipkart": "https://www.flipkart.com",
               "open hotstar": "https://www.hotstar.com",}

SmallTokenKeys=["who","when","where","whose","which","whatis","whom"]
MediumTokenKeys=["what","how","why"]
LargeTokenKeys=["explain","describe","summarize","discuss","elaborate","analyze","review","compare"]

voice_loop = False



with open('assets/file_List.txt', 'r') as f:  
    f.seek(0) 
    File_List = f.readlines()  
    File_List = [item.replace('\n', '') for item in File_List] 


        
        
        
        
    
        

@app.route('/', methods=['GET', 'POST'])
def index():
    global voice_loop
    global Messages
    global File_List
    

    if (request.method =='POST'):
        global last_post_time
        last_post_time = time.time()
        # Get the message from the user
        text = request.form.get('inputmessage')
        if text and text.strip():  # avoids crash on None
            msg = ("You", text)
            Messages.append(msg)
            if len(Messages) == 1 :
                with open('assets/file_List.txt', 'a') as f:
                    f.write(text+"\n")  # Append the file name to the file list in a newline
                Newfilename = text+".txt"
                with open("assets/History/"+Newfilename,"w") as f:  # write a new file in history
                    f.write(text+"\n")
            else:
                filename = Messages[0][1]+".txt"   # Find the file to write the message
                filename = filename.replace("\n","")  # replace newline with empyy string
                with open("assets/History/"+filename , "a") as f:    # writes the message in a new line
                    f.write(text+"\n")
                    
            if any(command in text.lower() for command in command_dict.keys()):
                for command in command_dict:
                    if command in text.lower():
                        matched_command = command
                        link= command_dict[matched_command]
                webbrowser.open_new(link)
                FinalOutput = f"Successfully Opened {matched_command.replace("open", "")}..."
                
            elif ( text.lower().strip() == "clear" or text.lower().strip() =="reset" or text.lower().strip() =="delete"):


                with open('assets/file_List.txt', 'w') as f:
                    f.truncate(0)
                history_folder = Path(__file__).parent / 'assets' / 'History'

                # Delete all files and subfolders in the folder
                for item in history_folder.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except Exception as e:
                        print(f"Could not delete {item}: {e}")
                    
                Messages.clear()
                
                
            else:
                try:
                    # AI response Logic according to token limit
                    if any(keyword1 in text.lower() for keyword1 in SmallTokenKeys):
                        response = co.generate(
                            prompt=text,
                            max_tokens=int(os.getenv("SMALL_TOKEN_UNIT"))
                            )
                        

                    elif any(keyword2 in text.lower() for keyword2 in MediumTokenKeys):
                        response = co.generate(
                            prompt=text,
                            max_tokens=int(os.getenv("MEDIUM_TOKEN_UNIT"))
                            )
                        

                    elif any(keyword3 in text.lower() for keyword3 in LargeTokenKeys):
                        response = co.generate(
                            prompt=text,
                            max_tokens=int(os.getenv("LARGE_TOKEN_UNIT"))
                            )
                        

                    else:
                        response = co.generate(
                            prompt=text,
                            max_tokens=150
                        )
                        
                    
                    AIresponse = response.generations[0].text
                    AIresponse = AIresponse.replace("\n", "")
                    pos = AIresponse.rfind('.')  # Find last full stop index
                    if pos != -1:
                        result = AIresponse[:pos+1]  # Keep up to and including the last full stop
                    else:
                        result = AIresponse # No full stop found, keep entire string
                    FinalOutput = result
                    
                    
                except cohere.CohereError:
                    FinalOutput = "Something went wrong, please try again after some time."
                
            
                
            try:
                Messages.append(("Jarvis", FinalOutput))
                filename = Messages[0][1]+".txt"
                filename = filename.replace("\n","")  # replace newline with empyy string
                with open("assets/History/"+filename , "a") as f:    # writes the AI response in a new line
                    f.write(FinalOutput+"\n")
            except:
                print("History Cleared")

        
        with open('assets/file_List.txt', 'r') as f:
            f.seek(0)
            File_List = f.readlines()
            File_List = [item.replace('\n', '') for item in File_List]

        if request.form.get('Newchat'):  # Clears the chat if the button is pressed
            Messages.clear()

        if request.form.get('Chatname'):  # If the user selects a chat name from the dropdown
            name=request.form.get('Chatname')
            Messages.clear()
            with open("assets/History/"+name+(".txt"),'r') as f:
                lines= f.readlines()
            ctr=2
            for line in lines:
                if ctr%2==0:
                    msgs = ("You", line)
                    Messages.append(msgs)
                else:
                    msgs = ("Jarvis", line)
                    Messages.append(msgs)
                ctr+=1
                
        
        return redirect('/')

        
    # Render the HTML template with the messages
    return render_template('index.html',Messages=Messages, File_List=File_List)

def shutdown_if_idle():
    while True:
        if time.time() - last_post_time > 300:  # 5 minutes = 300 seconds
            print("Server idle for 5 minutes. Shutting down.")
            os._exit(0)
        time.sleep(10)

def open_browser():
    ip=os.getenv("HOST")
    #Open the web browser after a delay and allow the server to start
    webbrowser.open_new(f"http://{ip}:5000")
    
    

if __name__=="__main__":
    threading.Thread(target=shutdown_if_idle, daemon=True).start()
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False, host=os.getenv("HOST"), port=5000)
    