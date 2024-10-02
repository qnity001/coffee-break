# Coffee Break

Meet Milo! The ULTIMATE mental health chat bot designed for students, offering personalized support, CBT tools and immense amount of resources to help all the students lead a better life.

**WHAT OUR SOLUTION DOES**

**Coffee Break** is a dedicated mental health companion designed specifically for students, addressing their unique challenges in managing mental well-being.

**1.** In a usual chat with Generative AI, conversations about mental health end quickly and do not allow a user to engage in the psychological processes of change. This leads to the conversation derailing often and the user cannot reach a satisfactory output. Milo, the mental health chatbot at Coffee Break, solves this problem by keeping the user focused on the emotion they are experiencing at hand. 
**2.** Instead of showing empathy and personalisation, Generative AI uses bullet points and information instead of sympathising and empathising with the user. The state-of-art system instructions provided to Gen AI makes the bot more human-like, while adding witty jokes to make it more relatable.

**PROJECT DESCRIPTION**

**In-scope of the solution**
-Empathetic and Personalised- Uses human expressions and expresses itself using emojis.
-Does not use bullet points- Acts like a emotional support bot and not an information giving machine
-Addresses one thing at a time instead of asking multiple questions, or giving multiple solutions at once
-Encourages the user to come to the solutions and take action upon themselves to increase engagement and activity (not passive)

**Out of scope**
-Professional Therapy- Milo is not a replacement for an actual therapist. Users are encouraged to talk to helpline numbers or seek a therapist in case of crisis situations.
-Mood-tracking-Coffee Break currently does not have memory over multiple chats. However, it does have memory for a single session. Therefore, mood-tracking is not possible currently.
**Future Opportunities**
-Mood-tracking- Create a *database* to store the chats of users to apply better sentiment analysis
-User-database- Create a user database so that chats are stored personally for each user
-Expansion on Resources- Add more data such as book suggestions etc. Add *details* for each of the resources so that user can get reviews from our application itself.
-Addition of Modules and Tools- *CBT* and *ACT* Techniques used commonly can be added as tools for topics such as Stress, Depression, Anxiety, etc.
-Create options in chat- Too much open-ended conversations are bound to be derailed. User is not satisfied usually. To change this, possible through *Dialogflow* and other APIs, include the option of creating choices for the user at certain intervals. This enables the user to work on the emotion they are currently feeling.
-Wider Range of Emotions- Include *examples* and *data* so that the model can learn from a wider range of emotions.

**PROBLEMS FACED WHILE MAKING THE PROJECT**
-It was our first time working with generative AI and technologies like Flask. Making a working handshake protocol between front-end and back-end was a tough task. With studies, it was possible. Understanding the concepts behind handshaking through Computer Networks was a challenging but a fulfilling task.
-Kept running into an error during chatting with Milo in the interface that said, "Error 429 resource might be exhausted (check quota)". This might be due to the limit on the number of requests that an API can handle in a single minute. Our quota kept getting full. This is not a pleasant experience for the user. We added a delay to the python, so that it would be able to take requests again.
-API Key reached day limit
-Flask requires its HTML file to be stored in a folder called "templates". Github Pages requires a file known as index.html to be present in the main repository for the website to work. Flask requires that the landing page and the HTML file for the chat interface be in the same directory. Transferring the landing page html file to templates created problems and led to 404 error on Github Pages.
-As students, training the model Milo without availability of much data was very difficult. We would test the chatbot, and it would not give the appropriate responses that we wanted. To overcome this, we went into further detail to create multiple and numerous cases so that Milo would respond as required.
-Implementation of Flask and BackEnd: As beginners, we had to learn about Flask from scratch and lack of mentors and any kind of experience led to a delay in the creation of our project.
-Interface doesn't run: The chat does not work if the server is closed. This server keeps the chat running and sends queries to the API to generate responses. If the server is closed on the dev's laptops and PCs, the chat interface does not work. The solution would be to keep the server running or getting free cloud service.
