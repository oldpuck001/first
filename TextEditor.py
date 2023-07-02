import os
import re
import tkinter as tk
import tkinter.font as tk_font
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename,asksaveasfilename
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import azure.cognitiveservices.speech as speechsdk

# New File
def mainNewFile(event=None):
    global mainFilePath
    if mainTextEditor.get('1.0',tk.END) != '\n':
        answer=tk.messagebox.askyesnocancel("Save changes?", "Do you want to save changes?")
        if answer is True:
            mainSaveFile()
            if mainFilePath != '':
                mainTextEditor.delete('1.0', tk.END)
        elif answer is False:
            mainTextEditor.delete('1.0', tk.END)
        else:
            return
    mainWindow.title("Text Editor")
    mainFilePath=''
    

# Open
def mainOpenFile(event=None):
    global mainFilePath
    if mainTextEditor.get('1.0',tk.END) != '\n':
        answer=tk.messagebox.askyesnocancel("Save changes?", "Do you want to save changes?")
        if answer is True:
            mainSaveFile()
        elif answer is False:
            pass            
        else:
            return
    mainFilePath=askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if mainFilePath:
        mainTextEditor.delete('1.0', tk.END)
        with open(mainFilePath, 'r') as mainInputFile:
            mainTextEditor.insert(tk.INSERT,mainInputFile.read())
    mainWindow.title("Text Editor - "+mainFilePath)

# Save
def mainSaveFile(event=None):
    if not mainFilePath:
        mainSaveAsFile()
    else:
        with open(mainFilePath, 'w') as mainOutputFile:
            mainOutputFile.write(mainTextEditor.get('1.0',tk.END+'-1c'))
    mainWindow.title("Text Editor - "+mainFilePath)

# Save As…
def mainSaveAsFile(event=None):
    global mainFilePath
    mainFilePath=asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if mainFilePath:
        with open(mainFilePath, 'w') as mainOutputFile:
            mainOutputFile.write(mainTextEditor.get('1.0',tk.END+'-1c'))
    mainWindow.title("Text Editor - "+mainFilePath)

# Export As PDF
def mainExportAsPDF():
    mainPDFpath=asksaveasfilename(defaultextension=".pdf")
    mainPDFtext=mainTextEditor.get('1.0','end')
    # Get default style and clone it for customization
    styles=getSampleStyleSheet()
    chinese_style=ParagraphStyle(
        "Chinese",
        parent=styles["BodyText"],
        fontName="Arial Unicode",
        fontSize=14,
        leading=16)
    lines=mainPDFtext.split('\n')
    story=[Paragraph(line,chinese_style) for line in lines]
    mainPDFfile=SimpleDocTemplate(mainPDFpath)
    mainPDFfile.build(story)

# Undo
def mainUndoText(event=None):
    mainTextEditor.edit_undo()

# Redo
def mainRedoText(event=None):
    mainTextEditor.edit_redo()

# Cut
def mainCutText(event=None):
    try:
        mainCopyText()
        mainTextEditor.delete("sel.first", "sel.last")
    except TclError:
        pass

# Copy
def mainCopyText(event=None):
    try:
        mainTextEditor.clipboard_clear()
        mainTextEditor.clipboard_append(mainTextEditor.selection_get()) 
    except TclError:
        pass

# Paste
def mainPasteText(event=None):
    try:
        mainTextEditor.insert(tk.INSERT,mainTextEditor.clipboard_get())
    except TclError:
        pass

# Read
def mainRead(event=None):
    try:
        text=mainTextEditor.selection_get()
    except tk.TclError:
        text=mainTextEditor.get('1.0',tk.END)

    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    speech_config.speech_synthesis_voice_name='zh-TW-YunJheNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

# Caption
def mainCaption(event=None):
    
    def captionExportZH():
        text=captionExportText.get('1.0',tk.END+'-1c')
        voice_name='zh-TW-YunJheNeural'
        TextToTextMP3(text,voice_name)

    def captionExportEN():
        text=captionExportText.get('1.0',tk.END+'-1c')
        voice_name='en-US-GuyNeural'
        TextToTextMP3(text,voice_name)

    def captionExportTH():
        text=captionExportText.get('1.0',tk.END+'-1c')
        voice_name='th-TH-NiwatNeural'
        TextToTextMP3(text,voice_name)

    def captionExportJA():
        text=captionExportText.get('1.0',tk.END+'-1c')
        voice_name='ja-JP-DaichiNeural'
        TextToTextMP3(text,voice_name)

    def captionExportKO():
        text=captionExportText.get('1.0',tk.END+'-1c')
        voice_name='ko-KR-GookMinNeural'
        TextToTextMP3(text,voice_name)

    textIn=mainTextEditor.get('1.0',tk.END)
    count=0
    first=True
    pattern=r"[\u3000-\u303F\uFF00-\uFFEF\u2000-\u206F\uFE10-\uFE1F\uFE30-\uFE4F]"
    resultString=re.sub(pattern,' ',textIn)
    resultList=resultString.split()
    
    captionWindow=tk.Toplevel(mainWindow)

    captionExportButtonFrame=tk.Frame(captionWindow)
    captionExportButtonFrame.pack(side='top')
    
    captionExportButtonZH=tk.Button(captionExportButtonFrame,text="Export as ZH",command=captionExportZH)
    captionExportButtonZH.pack(side='left')
    captionExportButtonEN=tk.Button(captionExportButtonFrame,text="Export as EN",command=captionExportEN)
    captionExportButtonEN.pack(side='left')
    captionExportButtonTH=tk.Button(captionExportButtonFrame,text="Export as TH",command=captionExportTH)
    captionExportButtonTH.pack(side='left')
    captionExportButtonJA=tk.Button(captionExportButtonFrame,text="Export as JA",command=captionExportJA)
    captionExportButtonJA.pack(side='left')
    captionExportButtonKO=tk.Button(captionExportButtonFrame,text="Export as KO",command=captionExportKO)
    captionExportButtonKO.pack(side='left')
    
    captionExportText=ScrolledText(captionWindow,undo=True)
    captionExportText.config(font=tk_font.Font(size=15))
    captionExportText.pack()

    for result in resultList:
        if len(result)>30:
            if first==False:captionExportText.insert(tk.INSERT,'\n')
            resultOut=list(result)
            count1=0
            for n in resultOut:
                captionExportText.insert(tk.INSERT,n)
                count1+=1
                if count1==30:
                    captionExportText.insert(tk.INSERT,'\n')
                    count1=0
            count=0
            first=False
        elif len(result)==30:
            if first==False:captionExportText.insert(tk.INSERT,'\n')
            captionExportText.insert(tk.INSERT,result)
            count=0
            first=False
        else:
            if count+1+len(result)>14:
                if first==False:captionExportText.insert(tk.INSERT,'\n')
                captionExportText.insert(tk.INSERT,result)
                count=len(result)
                first=False
            else:
                if count==0:
                    if first==False:captionExportText.insert(tk.INSERT,'\n')
                    captionExportText.insert(tk.INSERT,result)
                    count=len(result)
                    first=False
                elif count!=0:
                    captionExportText.insert(tk.INSERT,' ')
                    captionExportText.insert(tk.INSERT,result)
                    count=count+len(result)+1
                    first=False

def TextToTextMP3(text,voice_name):
    
    captionFilePathText=asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if captionFilePathText:
        with open(captionFilePathText, 'w') as captionOutputFileText:
            captionOutputFileText.write(text)

    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3)
    speech_config.speech_synthesis_voice_name=voice_name
        
    captionFilePathMP3=asksaveasfilename(defaultextension=".mp3",filetypes=[("MP3 Files","*.mp3"),("All Files","*.*")])
    audio_config=speechsdk.audio.AudioOutputConfig(filename=captionFilePathMP3)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    captionResult = speech_synthesizer.speak_text_async(text).get()

# Word count
def mainUpdateWordCount():
    mainWordCount=mainTextEditor.get('1.0','end')
    mainWordCount=mainWordCount.replace("\n", "")
    word_count=len(mainWordCount)
    mainWordCountLabel.config(text=' Words: '+str(word_count))
    mainWindow.after(1000,mainUpdateWordCount)

# Close window
def mainCloseWindow(event=None):
    if mainTextEditor.get('1.0',tk.END) != '\n':
        answer=tk.messagebox.askyesnocancel("Save changes?", "Do you want to save changes?")
        if answer is True:
            mainSaveFile()
            mainWindow.destroy()
        elif answer is False:
            mainWindow.destroy()
        else:
            return
    else:
        mainWindow.destroy()

# Initialize file path
global mainFilePath
mainFilePath=''

# Register font
pdfmetrics.registerFont(TTFont('Arial Unicode','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))

# Create the main window
mainWindow=tk.Tk()
mainWindow.title("Text Editor")
mainWindow.minsize(900,500)

# Create the main window menu
mainMenu=tk.Menu(mainWindow)
mainWindow.config(menu=mainMenu)

mainMenuFile=tk.Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='File',menu=mainMenuFile)
menu=mainMenuFile.add_command(label='New File',command=mainNewFile)
menu=mainMenuFile.add_command(label='Open…',command=mainOpenFile)
menu=mainMenuFile.add_command(label='Save',command=mainSaveFile)
menu=mainMenuFile.add_command(label='Save As…',command=mainSaveAsFile)
menu=mainMenuFile.add_command(label='Export as PDF',command=mainExportAsPDF)

mainMenuEdit=tk.Menu(mainMenu,tearoff=0)
mainMenu.add_cascade(label='Edit',menu=mainMenuEdit)
mainMenuEdit.add_command(label='Undo',command=mainUndoText)
mainMenuEdit.add_command(label='Redo',command=mainRedoText)
mainMenuEdit.add_command(label='Cut',command=mainCutText)
mainMenuEdit.add_command(label='Copy',command=mainCopyText)
mainMenuEdit.add_command(label='Paste',command=mainPasteText)
mainMenuEdit.add_command(label='Read',command=mainRead)
mainMenuEdit.add_command(label='Caption',command=mainCaption)

# Create the shortcut key framework and shortcut keys, word count label for the main window
mainShortcutKeyFrame=tk.Frame(mainWindow)
mainShortcutKeyFrame.pack(side='top', fill='x')

mainShortcutKeyNew=tk.Button(mainShortcutKeyFrame,text="New File", width=5)
mainShortcutKeyNew.pack(side='left')
mainShortcutKeyNew.bind('<Button-1>',mainNewFile)

mainShortcutKeyNew=tk.Button(mainShortcutKeyFrame,text="Open…", width=5)
mainShortcutKeyNew.pack(side='left')
mainShortcutKeyNew.bind('<Button-1>',mainOpenFile)

mainShortcutKeySave=tk.Button(mainShortcutKeyFrame,text="Save", width=5)
mainShortcutKeySave.pack(side='left')
mainShortcutKeySave.bind('<Button-1>',mainSaveFile)

mainShortcutKeyUndo=tk.Button(mainShortcutKeyFrame,text="Undo", width=5)
mainShortcutKeyUndo.pack(side='left')
mainShortcutKeyUndo.bind('<Button-1>',mainUndoText)

mainShortcutKeyRedo=tk.Button(mainShortcutKeyFrame,text="Redo", width=5)
mainShortcutKeyRedo.pack(side='left')
mainShortcutKeyRedo.bind('<Button-1>',mainRedoText)

mainShortcutKeyCut=tk.Button(mainShortcutKeyFrame,text="Cut", width=5)
mainShortcutKeyCut.pack(side='left')
mainShortcutKeyCut.bind('<Button-1>',mainCutText)

mainShortcutKeyCopy=tk.Button(mainShortcutKeyFrame,text="Copy", width=5)
mainShortcutKeyCopy.pack(side='left')
mainShortcutKeyCopy.bind('<Button-1>',mainCopyText)

mainShortcutKeyPaste=tk.Button(mainShortcutKeyFrame,text="Paste", width=5)
mainShortcutKeyPaste.pack(side='left')
mainShortcutKeyPaste.bind('<Button-1>',mainPasteText)

mainShortcutKeyRead=tk.Button(mainShortcutKeyFrame,text="Read", width=5)
mainShortcutKeyRead.pack(side='left')
mainShortcutKeyRead.bind('<Button-1>',mainRead)

mainShortcutKeyCaption=tk.Button(mainShortcutKeyFrame,text="Caption", width=5)
mainShortcutKeyCaption.pack(side='left')
mainShortcutKeyCaption.bind('<Button-1>',mainCaption)

mainWordCountLabel=tk.Label(mainShortcutKeyFrame,text=' Words: 0')
mainWordCountLabel.pack(side='left')

# Create the text editing area
mainTextEditor=ScrolledText(mainWindow,undo=True)
mainTextEditor.config(font=tk_font.Font(size=15))
mainTextEditor.pack(side='bottom',expand=True,fill='both')

# Activate word count statistics
mainWindow.after(1000,mainUpdateWordCount)

# Activate check for saved updates when closing the window
mainWindow.protocol("WM_DELETE_WINDOW",mainCloseWindow)

mainWindow.mainloop()
