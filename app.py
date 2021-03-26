import streamlit as st
from tika import parser
from gtts import lang
from gtts import gTTS
import os
import base64

def main():
	st.title("Document to Speech Assistant")

	initials = lang.tts_langs()
	languages = {v: k for k, v in initials.items()}	
	menu = sorted(list(languages.keys()))
	choice = st.sidebar.selectbox("Languages",menu)
	selected_language = languages[choice]

	st.subheader("Upload file")
	document = st.file_uploader(" ",type=['txt','docx','pdf'])
	if st.button("Process"):
		if document is not None:
			file_details = {"Filename":document.name,"FileType":document.type,"FileSize":document.size}
			st.write(file_details)
			try:
				status = st.empty()

				load_text = "Processing text"
				status.markdown("%s" % load_text)
				raw = parser.from_file(document)
				data = raw['content']

				load_text = "Processing audio"
				status.markdown("%s" % load_text)
				tts = gTTS(text = data, lang = selected_language)
				filename = document.name.split('.')[0]+'.mp3'
				tts.save(filename)

				load_text = "Processing download"
				status.markdown("%s" % load_text)
				with open(filename, 'rb') as f:
					mp3rb = f.read()				    
				b64 = base64.b64encode(mp3rb).decode()
				href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(filename)}">Download {filename}</a>'
				st.markdown(href, unsafe_allow_html=True)
						
			except Exception as e:
				print(e)
				if str(e).startswith('429'): st.write("This application uses Google API, then its today's free limit has been reached.")
				
if __name__ == '__main__':
	main()
