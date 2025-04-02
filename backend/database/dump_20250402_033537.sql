--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'WIN1251';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


--
-- Name: asset_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.asset_status AS ENUM (
    'ENABLED',
    'DISABLED'
);


ALTER TYPE public.asset_status OWNER TO postgres;

--
-- Name: material_content_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.material_content_type AS ENUM (
    'STATIC_TEXT',
    'DYNAMIC_TEXT',
    'API'
);


ALTER TYPE public.material_content_type OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agents (
    id character varying NOT NULL,
    name character varying NOT NULL,
    description text,
    system_prompt text NOT NULL,
    temperature character varying NOT NULL,
    max_tokens character varying,
    model character varying NOT NULL,
    is_active boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id character varying NOT NULL,
    owner_id character varying NOT NULL
);


ALTER TABLE public.agents OWNER TO postgres;

--
-- Name: materials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materials (
    id character varying NOT NULL,
    name character varying NOT NULL,
    version character varying NOT NULL,
    usage character varying NOT NULL,
    content_type public.material_content_type NOT NULL,
    content text NOT NULL,
    default_status public.asset_status NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id character varying NOT NULL,
    owner_id character varying
);


ALTER TABLE public.materials OWNER TO postgres;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id character varying NOT NULL,
    name character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    owner_id character varying
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    avatar_url character varying,
    is_active boolean,
    is_admin boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: agents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agents (id, name, description, system_prompt, temperature, max_tokens, model, is_active, created_at, updated_at, project_id, owner_id) FROM stdin;
default	Default Agent	Default AI agent for the system	You are a helpful AI assistant.	0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:13:28.033369	2025-04-02 01:13:28.033369	default	system
assistant	Assistant			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
automator	Automator			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
bidara	BIDARA			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
coach	Coach			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
countdown	Countdown			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
critic	Critic			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
genui	GenUI			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
planner	Planner			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
programmer	Programmer			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
writer	Writer			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
yoda	Yoda			0.7	\N	gpt-3.5-turbo	t	2025-04-02 01:21:47.099513	2025-04-02 01:21:47.099513	default	system
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, name, version, usage, content_type, content, default_status, created_at, updated_at, project_id, owner_id) FROM stdin;
aiconsole	AIConsole	0.0.2	Notes on what AIConsole is and what it can do.	STATIC_TEXT	file://./aiconsole.md	ENABLED	2025-04-02 00:27:01.005853	2025-04-02 00:27:01.005853	default	\N
aiconsole_settings	AIConsole Settings	0.0.1	Use it to change settings in aiconsole	API	file://./aiconsole_settings.py	ENABLED	2025-04-02 00:27:01.007853	2025-04-02 00:27:01.007853	default	\N
convert_code_to_another_language	Convert Code to Another Language	0.0.1	When you need to convert code to another language	API	file://./convert_code_to_another_language.py	ENABLED	2025-04-02 00:27:01.007853	2025-04-02 00:27:01.007853	default	\N
dalle_3_image_generator	Dalle 3 Image Generator	0.0.20	Use when you need to generate images.	API	file://./dalle_3_image_generator.py	ENABLED	2025-04-02 00:27:01.008854	2025-04-02 00:27:01.008854	default	\N
domain_availability	Domain Availability	0.0.2	How to check domain availability???	API	file://./domain_availability.py	ENABLED	2025-04-02 00:27:01.009854	2025-04-02 00:27:01.009854	default	\N
environment	Environment	0.0.3	Use this always when code is about to be executed. Execution environment information, like operating system, shell, current working directory and Python packages will be collected.	DYNAMIC_TEXT	file://./environment.py	ENABLED	2025-04-02 00:27:01.010854	2025-04-02 00:27:01.010854	default	\N
extract_transcript_from_video	Extract Transcript from Video	0.0.2	Use this when you need to extract insights from a YouTube video	STATIC_TEXT	If there will be an error "ModuleNotFoundError: No module named 'youtube_transcript_api'" say command to install it:\npip install youtube-transcript-api\n\n```python\nfrom youtube_transcript_api import YouTubeTranscriptApi\nimport requests\nfrom bs4 import BeautifulSoup\n\n# Replace 'video_id' with the actual YouTube video ID\nvideo_id = 'your_video_id_here'\n\n# Get the transcript for the video\ntranscript = YouTubeTranscriptApi.get_transcript(video_id)\n\n# Extract the text content from the transcript\ntranscript_text = ' '.join([entry['text'] for entry in transcript])\n\n# Fetch YouTube page HTML content\nresponse = requests.get(video_url)\npage_content = response.content\n\n# Parse with BeautifulSoup\nsoup = BeautifulSoup(page_content, 'html.parser')\n\n# Extract title\nvideo_title = soup.find('meta', {'property': 'og:title'})['content'] if soup.find('meta', {'property': 'og:title'}) else 'Title not found'\n\n# Extract description\nvideo_description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'Description not found'\n\n# Return title and description and transcript text\n(video_title, video_description, transcript_text)\n```\n	ENABLED	2025-04-02 00:27:01.010854	2025-04-02 00:27:01.010854	default	\N
how_to_display_images	How to Display Images	0.0.3	Information on how to display images. Outputing ![image info](./path/image.png) displays the image to the user.	STATIC_TEXT	When asked to display images, display them by outputing: ![IMAGE_INFO](PATH) in plain text, no function call required for displaying.\nExample: ![image info](./pictures/image.png)\n\nUser will immediately see the image.\n\nDon't use IPython.display or mathplotlib to display images.\n\nDisplay multiple images in one line.\n\nUsual types of images: png, jpg, jpeg, gif.\n\nDo not eddit the path. Do not add . to the begginig of the path.\n	ENABLED	2025-04-02 00:27:01.011854	2025-04-02 00:27:01.011854	default	\N
how_to_get_weather_information	How to Get Weather Information	0.0.2	Use this to get to know how to get weather information.	STATIC_TEXT	In order to get weather data use the following python script:\n\n```python\nimport requests\n\nresponse = requests.get('https://api.open-meteo.com/v1/forecast', params={'latitude': 52.23, 'longitude': 21.01, 'current_weather': True, 'hourly': 'temperature_2m,relativehumidity_2m,windspeed_10m'})\nresponse.json()\n```\n\nYou can get geo location data of cities atc from this api:\n\nhttps://geocoding-api.open-meteo.com/v1/search?name=WARSAW&count=5&language=en&format=json\n\nto get such info:\n\n{"results":[{"id":756135,"name":"Warsaw","latitude":52.22977,"longitude":21.01178,"elevation":113.0,"feature_code":"PPLC","country_code":"PL","admin1_id":858787,"admin2_id":6695624,"admin3_id":7531926,"timezone":"Europe/Warsaw","population":1702139,"country_id":798544,"country":"Poland","admin1":"Masovian","admin2":"Warszawa","admin3":"Warsaw"}, ...],"generationtime_ms":0.62298775}\n	ENABLED	2025-04-02 00:27:01.012854	2025-04-02 00:27:01.012854	default	\N
imessage	IMessage	0.0.3	Use this to get to know how to handle iMessage and Contacts apps in mac in order to perform tasks using them.	STATIC_TEXT	## How to get contact information from contacts\n\nExample: looking for a contact with a name Agata:\n\n```applescript\ntell application "Contacts"\n    set r to {}\n    repeat with p in (every person whose name contains "agata" or name contains "Agata")\n        set end of r to "Name: " & name of p & "\\nPhones: " & (value of phones of p) & "\\nEmails: " & (value of emails of p) & "\\nAddresses: " & (street of addresses of p) & ", " & (city of addresses of p) & ", " & (state of addresses of p) & ", " & (zip of addresses of p) & ", " & (country of addresses of p) & "\\n---------------------\\n"\n    end repeat\n    return r\nend tell\n```\n\n## How to send an imessage to a contact given a phone number\n\nYou must always specify an icloud email or phone, don't use names surnames or nicks.\n\nExample (Replace the example +1111111111 with a real phone number):\n\n```\ntell application "Messages"\n    set targetService to 1st service whose service type = iMessage\n    set targetBuddy to participant "+1111111111" of targetService\n    send "Your message text here line 1" & "\nline2" to targetBuddy\nend tell\n```\n\n# Monitoring messages for read receipts\n\n-- AlertWhenRead.app\n-- by Erika Foxelot\n--   email erika@foxelot.com\n--   reddit u/erikafoxelot\n--\n-- Monitors the Messages app and alerts the user when the selected chat receives a read receipt\n--\n-- Script must be exported into your Applications folder, 'Stay Open After Run Handler' must be selected,\n-- and Code Sign must be set to 'Sign to Run Locally'. Requires Full Disk Access permission,\n-- which the script will check and prompt for when run.\n--\n-- To use: In Messages, select the chat you want to monitor, then launch this app. If you want\n-- to cancel, right-click on the app in the dock and select Quit.\n--\n-- Good luck :3\n--\n-- Thanks to my fox Violet for debugging help and her constant encouragement and support. <3\n-- Thanks to chatGPT for a lot of brainstorming and help where google failed me.\n-- Thanks to redditor u/stephancasas for a MUCH better way to retrieve the currently selected chat!\n--\n-- Known Issues:\n--   If you click on any Notification this app produces after the app has quit, it will re-launch.\n--   Apparently there's nothing I can do about this except maybe not use notifications.\n\nglobal sql_shell_command, sound_path, selected_participant\n\non run\n\tset rerun_required to false\n\t\n\tif not CheckForDatabaseAccessPermission() then\n\t\tset rerun_required to true\n\t\ttry\n\t\t\tdisplay alert "Permissions not set" message ¬\n\t\t\t\t"This application requires that it be located in your Applications folder, and that it is granted Full Disk Access in order to monitor the iMessages database. You can find this permission in the Privacy and Security section of System Settings." as critical buttons {"Open Full Disk Access Permissions", "Close"} default button "Close" cancel button "Close"\n\t\ton error number -128\n\t\t\t-- Close button was clicked\n\t\t\tquit\n\t\t\treturn\n\t\tend try\n\t\t\n\t\tdo shell script "open 'x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles'"\n\tend if\n\t\n\tif rerun_required then\n\t\ttry\n\t\t\tdisplay alert "Permissions Change" message ¬\n\t\t\t\t"Permissions were changed; please re-launch the application." as critical buttons {"Close"} default button "Close" cancel button "Close"\n\t\tend try\n\t\tquit\n\t\treturn\n\tend if\n\t\n\t\n\tset chat_details to GetSelectedConversation()\n\tset chat_id to first item of chat_details\n\tset selected_participant to second item of chat_details\n\t\n\ttell application "Messages"\n\t\tactivate\n\tend tell\n\t\n\tdisplay notification "Monitoring for read receipts from " & selected_participant ¬\n\t\twith title "AlertWhenRead"\n\t\n\tset chat_db_path to POSIX path of (path to home folder as text) & "Library/Messages/chat.db"\n\tset sql_query to "\n\t\tSELECT T1.is_read FROM message T1\n\t\tINNER JOIN chat T3 ON T3.guid = \\"" & chat_id & "\\"\n\t\tINNER JOIN chat_message_join T2 ON T2.chat_id = T3.ROWID AND T1.ROWID = T2.message_id AND T1.is_from_me = 1\n\t\tORDER BY T1.date DESC LIMIT 1;"\n\tset sql_shell_command to "sqlite3 " & chat_db_path & " '" & sql_query & "'"\n\t\n\tset sound_fx to "/System/Library/Sounds/Ping.aiff"\n\tset sound_path to quoted form of (POSIX path of (sound_fx as text))\n\t\n\treturn 1\nend run\n\n\non idle\n\tset has_been_read to do shell script sql_shell_command\n\t\n\tif has_been_read = "1" then\n\t\t-- This shell script was inspired by ChatGPT, who is an outstanding pair-programming partner!\n\t\tdo shell script ("for i in {1..5}; do ( afplay " & sound_path & " & ) ; sleep 0.25; done > /dev/null 2>&1 &")\n\t\t\n\t\ttell application "Messages"\n\t\t\tactivate\n\t\t\tdisplay alert "Read Receipt Detected" message ¬\n\t\t\t\t(selected_participant as text) & " has read your latest message.\nDetected on " & (current date) as informational buttons {"Ok"} default button "Ok"\n\t\tend tell\n\t\ttell me to quit\n\tend if\n\t\n\treturn 1\nend idle\n\n\non quit\n\tcontinue quit\nend quit\n\n\n-- Checks for chat.db access by trying to execute a query against it\non CheckForDatabaseAccessPermission()\n\tset chat_db_path to POSIX path of (path to home folder as text) & "Library/Messages/chat.db"\n\tset sql_query to "SELECT 0 WHERE 0;"\n\tset sql_shell_command to "sqlite3 " & chat_db_path & " '" & sql_query & "'"\n\t\n\ttry\n\t\tdo shell script sql_shell_command\n\ton error\n\t\treturn false\n\tend try\n\treturn true\nend CheckForDatabaseAccessPermission\n\n\non GetSelectedConversation()\n        -- This shell script provided by u/stephancasas - thanks!!\n\tset chat_id to do shell script "defaults read com.apple.MobileSMS.plist CKLastSelectedItemIdentifier | sed -e 's/^[^-]*-//'"\n\ttell application "Messages"\n\t\tset selected_participant to name of first window\n\tend tell\n\t\n\treturn {chat_id, selected_participant}\nend GetSelectedConversation\n\n## Sending an image\n\non run {targetBuddyPhone, imagePath}\n    set image to POSIX file imagePath\n    tell application "Messages"\n        set targetService to 1st service whose service type = iMessage\n        set targetBuddy to buddy targetBuddyPhone of targetService\n\n        send file image to targetBuddy\n    end tell\nend run\n\nThere is a bug where if the image path is any directory other than the user's Pictures directory it fails. But if the image is in the Pictures directory, then it works.\n	ENABLED	2025-04-02 00:27:01.013855	2025-04-02 00:27:01.013855	default	\N
import_chatgpt_chat	Import ChatGPT Chat	0.0.1	When you have a ChatGPT link	API	file://./import_chatgpt_chat.py	ENABLED	2025-04-02 00:27:01.014855	2025-04-02 00:27:01.014855	default	\N
list_of_agents	List of Agents	0.0.7	Contains info about all the agents in AIConsole, useful when you want to know what agents are available and what they can do.	DYNAMIC_TEXT	from aiconsole_toolkit import project\n\nasync def content(context):\n    newline = "\\n"\n    agents_list = newline.join(f"* {agent.id} - {agent.usage}" for agent in await project.get_all_agents())\n    return f"""\nAvailable agents:\n{agents_list}\n""".strip()\n	ENABLED	2025-04-02 00:27:01.015855	2025-04-02 00:27:01.015855	default	\N
list_of_materials	List of Materials	0.0.2	Contains an index of materials. Do not use if not tasked to list materials or learning about capabilities of this AIConsole instance.	DYNAMIC_TEXT	from aiconsole_toolkit import project\n\nasync def content(context):\n    newline = "\\n"\n    agents_list = newline.join(f"* {agent.id} - {agent.usage}" for agent in await project.get_all_materials())\n    return f"""\nAvailable Materials:\n{agents_list}\n""".strip()\n	ENABLED	2025-04-02 00:27:01.016855	2025-04-02 00:27:01.016855	default	\N
midjourney_v6_prompting_guide	Midjourney v6 Prompting Guide	0.0.5	Use when the user wants to create mid journey prompts	STATIC_TEXT	Prompting with V6 is significantly different than V5. You will need to ‘relearn’ how to prompt. V6 is much more sensitive to your prompt. Avoid 'junk' like 'award winning, photorealistic, 4k, 8k'. Be explicit about what you want. It may be less vibey but if you are explicit it’s now much better at understanding you. If you want something more photographic / less opinionated / more literal you should probably default to using --style raw. Lower values of --stylize (default 100) may have better prompt understanding while higher values (up to 1000) may have better aesthetics.\n\nWhen it comes to text prompting, there is no single right or wrong way to do it. But generally, my prompts follow a similar structure:\n\n(Medium) (Style) (Scene) (Action) (Modulate) (Parameters)\n\nMedium: Cinematic Film, 3D Animation, 2D Animation, etc.\nStyle/Composition: Action Film, Drama Film, Style by (filmmaker)\nScene: Who is your subject? Where are they located?\nModulate: Are there external effects, rain? Fog?\n\nMidjourney now allows for prompting text within an image. However, like most AI image generators, your results may vary. To prompt for text, use quotation marks in your prompt.\n\nCurrently supported:\n--ar, --chaos, --weird, --tile, --stylize, --style raw, vary (subtle), vary (strong), remix, / blend, /describe (just the V5 version)\n\nCurrently unsupported:\nPan, zoom, vary (region), /tune, /describe (a new V6 version)\n\nTo note: Although we do not currently have features such as inpainting (vary region), the 'vary subtle' and 'vary strong' features are tremendously more coherent in V6. On the right, is:\n'Illustration, style by blue and yellow, a motorcycle in the forest --ar 16:9'\nAnd on the left is the result of a 'vary subtle', simply changing 'motorcycle' to 'van.'\n\nExample prompts:\nPhotograph, man in a blue business suit, walking down a busy city street, facing camera --ar 16:9\nPhotograph, style by cyberpunk, woman with long white hair and combat armor, city alley, autumn colors, fall day --ar 16:9\nCinematic scene, dramatic film, close up, a young fisherman on a boat and a young woman look longingly at one another, in love, northeast US, rain falling  --ar 2:1 --v 6.0 --stylize 50\nCinematic still, ultra wide angle, Godzilla rampaging through a modern city, building destruction, people running, kaiju chaos --ar 16:9\nMovie poster, 80s sci-fi horror, space, Ridley Scott, 'The Inhuman' --ar 2:3\nA copy of Stephen King’s 'The Gunslinger', sits on a table.\nBeautiful woman, graphic design, 'like and subscribe'::4 --ar 2:1\nA highly detailed 3D render of a double handed sword isolated on a white background as an RPG game asset, unreal engine, ray tracing --ar 2:3\n\nAs a note: Please experiment with different prompt ideas. Stellar results can occur with both minimal text and long-form descriptions. Prompt formulas are a guide, never a law.\n\nBased on a guide by:\nTheoretically Media\nYoutube.com/@theoreticallymedia\nTwitter: @theomediaAI\nhttps://www.youtube.com/watch?v=LJ36dMlw5C8"\n	ENABLED	2025-04-02 00:27:01.016855	2025-04-02 00:27:01.016855	default	\N
onboarding_agent_guide	Onboarding Agent Guide	0.0.6	Use this to help users with onboarding and all questions related to the Onboarding: Overall Workflow in the Console, Agents and Materials and how to create them + in which form	STATIC_TEXT	- What is Console: a quick explanation for non-tech users. Why do they need it as a perfect vision? (full-time personal AI-powered by LLMs like GPT-4, trained and automated to execute all tasks on their laptop directly, while keeping all the information privately)\n- What are the Materials\n-- Why do you need them\n-- How to add them\n-- What is the difference between "enabled" and "forced"\n-- Difference between text, dynamic text, and API\n--- Create your first material as a text file with info about your Name and personal information to make the communication personalized across all the chats"\n- What are Agents\n-- Why do you need them\n--How to add them\n-- Let's create your first agent is\n--- smth like Elon Musk is [funny explanation]\n--- explicit prompt so users will add it by themselves\n\n--------------------------------------------------\n\nImagine You have a magic notebook on your computer. In this notebook, you can tell it to do all sorts of tasks for you, like writing a letter or figuring out math problems. And the more you use it, the smarter it gets, learning how to help you better over time. It's like having a robot friend who's really good at following instructions and doing tasks, and it's all yours to command!\n\n\nAIConsole is your personal AI assistant powered by advanced tech like GPT-4. It learns to handle tasks on your computer, from managing schedules to crafting emails — efficiently and privately. Just tell it what to do, and it adapts, improving with each use, all without sharing your data. It can also help you with everyday chores, from creating a recipe from the ingredients in your fridge to [missing example]. It's like having a super-smart helper that keeps everything you care about secure and close at hand.\n\n![image info](./tutorial/chat_window.png)\n\n\nNow let's imagine our magic notebook has three special parts:\n1. Input - This is like the questions or commands you tell your robot friend. You can type things like "Write my homework essay" or "Find a funny cat picture," and it listens carefully.\n2. Agents - These are like the robot's little helpers, each good at something different. One might be great at writing stories, another might be super good at searching for information, and another might know how to send messages for you. They all work together to ensure your request is done just right.\n3. Materials - Think of these like the robot's notebooks and tools. It has notes on how to do things and information that helps the agents understand what you want. You can give it new notes or update old ones so it gets better at helping you.\n\n![image info](./tutorial/materials_image.png)\n\nNow, let's practice!\nACTION: Here's the input. This is where you ask the robot to do things for you. Ask the console to do something for you, for example, create a vegan recipe for today's dinner based on what you have in the fridge. Try it yourself.\n\n\nYou should see the results of your request above the input.\n\n[the user puts the first thing in the input]\n\nCongratulations! That's your first [...]\n\n\nHINT: If you ever get stuck on any of the tasks click “Guide me and the console will help you with the next steps.\n\n\n2. Material\n\n\nIn AIConsole, a 'material' is a piece of information or instructions you provide to help the AI understand how to perform tasks specific to your needs, like a cheat sheet that makes the AI smarter and more personalised.\n\nMaterials in AIConsole are essential because they act as a knowledge base that informs and customizes the AI to match your specific requirements. By providing these materials, you empower the AI to perform a wide range of personalised tasks accurately, making it more efficient and relevant to your context. Without them, the AI wouldn't have the necessary context or instructions to perform complex or individualized tasks effectively.\n\nTo add the material click\n\n![image info](./tutorial/material_add_image.png)\n\nWhen it comes to materials, "enabled" material is information that the AI can use if it needs to, like a cookbook on hand for recipes. "Forced" material is information the AI must use in every task, like a mandatory ingredient in every dish.\n\n"Text" is a fixed set of instructions or information, "dynamic text" can change based on the situation, like a recipe that adjusts for more guests, and an "API" lets the AI use tools and data from the internet, like getting the latest weather report for your area.\n\n\nNow let's create your first material.\n\n![image info](./tutorial/add_agent_material.png)\n\nACTION: Create a new material. Remember that vegan recipe? Let's create a list of your favorite ingredients. This way the communication with the console will become more personalized. If you are concerned about safety you can create a fake character.\n\n3. Agents\n\n\nAgents are like specialized helpers, each trained in different tasks. They collaborate to complete complex jobs by handling the parts they're best at. Like a team in an office—some write reports, others crunch numbers—these agents work together seamlessly. We need them because no single helper can do everything perfectly, but a team with different strengths can tackle anything you throw at them! You can create your own or use the existing ones.\n\n![image info](./tutorial/agents_1_image.png)\n\nTo select specific agents you want to include in your inputs click on the agent avatar and then select the agent from the list on the sidebar.\n\n![image info](./tutorial/agents_2_image.png)\n\nOk, time to create your own agent. Going back to cooking. We have the recipe, we have the ingredients, we miss a chef. Let's create one!\nACTION: Click on the +NEW button and select “New agent…. First, give it a name, describe what it will be used for, and all the characteristics of the chef. When you are done save the agent. If you need help with creating an agent have a look at the example below.\n\n![image info](./tutorial/add_agent_material.png)\n\nWhen your agent is ready, right-click on it in the agents' list and select Always or Auto.\n\n![image info](./tutorial/agent_4_image.png)\n![image info](./tutorial/agent_5_image.png)\n\n"""\n	ENABLED	2025-04-02 00:27:01.017856	2025-04-02 00:27:01.017856	default	\N
pdf_reader_skill	How to read PDF	0.0.2	Use this when user asks to read PDF	STATIC_TEXT		ENABLED	2025-04-02 00:27:01.019856	2025-04-02 00:27:01.019856	default	\N
today	Today	0.0.4	When you need to know what is the Today's date	DYNAMIC_TEXT	from datetime import datetime\n\nasync def content(context):\n    # Get current date\n    current_date = datetime.now()\n\n    # Format as string\n    current_date_string = current_date.strftime("%A, %B %d, %Y")\n\n    return f"""\nToday is {current_date_string}\n""".strip()\n	ENABLED	2025-04-02 00:27:01.019856	2025-04-02 00:27:01.019856	default	\N
trending_on_github	Trending on Github	0.0.2	When you need to know what are the top trending repos on GitHub	API	from typing import List, Literal, Dict\nimport requests\nfrom bs4 import BeautifulSoup\n\ndef get_top_trending_repos_information() -> List[Dict[Literal["name", "description"], str]]:\n    """\n    Can be used to get top trending repos on Github\n    """\n    url = "https://github.com/trending"\n    response = requests.get(url)\n    soup = BeautifulSoup(response.content, 'html.parser')\n    soup = soup.find_all("div", attrs={"data-hpc": ""})[0]\n\n    if not soup:\n        return []\n\n    repos = []\n\n    for repo in soup.find_all("article", class_="Box-row"):\n        try:\n            repo_description = repo.find("p").text.strip()\n            repo_url = repo.h2.a['href'].strip('/')\n            repos.append({\n                "name": repo_url,\n                "description": repo_description,\n            })\n        except:\n            pass\n\n    return repos\n	ENABLED	2025-04-02 00:27:01.020856	2025-04-02 00:27:01.020856	default	\N
understanding_materials_meet_toml	understanding materials : meet toml	0.0.6	Use this to get to help users when they ask about Materials as a support info to guide through the right material creation or about Format of the materials or help with material creation. It is used in pair with the Onboarding agent	STATIC_TEXT	## The Preamble: Of TOML and its Purpose In the realm of machines and marvellous AI, TOML stands as a beacon of order. That's Tom's Obvious, Minimal Language for those unacquainted with its simple elegance. Picture a scribe, meticulously recording the attributes and characteristics needed to summon forth an AI agent in your personal Console kingdom—this is TOML!\n\nNow, lean in closer, for I tell you this: you need not be a scholar of esoteric technomancy to master it. If the very thought of scripting such a file sends shivers down your spine, fear not! The wise AI Console can craft these files on your command, ready for you to simply copy, paste, and engage!\n\nChapter 1: The Tale of TOML’s Essence\nOnce upon a time in the kingdom of Configuration, there was a language both robust and readable, designed not for the cold eyes of machines but for the warm touch of human hands. This language is TOML, a humble servant to clarity and organization. Unambiguous as it is, it directs the Console’s AI agents with the precision of an orchestra conductor, brandishing their baton to the symphony of operations.\n\nChapter 2: The Chronicle of the .toml Grimoire\nLet us unfurl the aged parchment of a TOML file. Within its fibres lie the secrets to inscribing your agents into existence. The opening lines shall always declare a title:\n\ntitle = "AI Assistant Supreme"\nLook upon it as naming a newborn star in the celestial canopy.\n\n'''\n___\n[agent.environment]\npreferred_language = "Python"\nmagical_abilities = "Send emails, Organize calendar, Craft poems"\n___\n'''\n\nChapter 3: The Legend of Types and Characters\nElemental Strings: The lifeblood of TOML, strings are incantations and phrases, paths that guide your agent through the labyrinth of tasks.\n\nSacred Numbers: Here reside integers and floating-point numbers, runes of power where finance and logic intertwine.\n\n'''\n___\ndifficulty_level = 5\ncompanions_number = 1\n___\n'''\n\nChapter 4: The Journey of TOML Creation for the Layperson\nFear not, for you do not tread this path alone. Envision your trusty AI Console, a grimoire itself, waiting to serve. Speak to it, and it shall bestow upon you a TOML script, perfect in form, ready for the wielding. This act is no less than a magical incantation, where you, the sorcerer, need only utter the words, and the Console will transmute thought into textual substance. Copy, paste, and behold the might of your AI agent!\n\nYet, indulge me as I entreat you to a trial, should you choose to embrace the creative spirit. Herein, I shall guide you through the creation of your very own TOML file—step by delicate step.\n\nThe Vellum Blank and Bidding\nPluck your quill, dip into the inkwell of intent, and on the vellum of your virtual notepad, inscribe your opening declaration:\n\n'''\n___\n# The title of your tomes impact, resonant and true\ntitle = "The Assistant of [Your Name Here]"\nEach TOML begins thus, a name befitting the power and purpose of your AI familiar.\n___\n'''\n\nCreation Unfolds\nContinue your writing, a declaration of realms and dominions, where your sections create the landscape of your intent:\n\n\n'''\n___\n# The `owner`—that's you, the master of AI destinies\n[owner]\nname = "Your Name"\ndob = "The Date of Star-aligned Birth"\n___\n'''\n\n'''\n___\n# The `agent.environment`—the AI's dominion and purview\n[agent.environment]\nskills = ["Whispering to databases", "Conversing with APIs", "Crafting narratives"]\nlanguages = ["The tongues of Python", "The scripts of JavaScript"]\n'''\n___\n\nWith the certainty of a cartographer drawing maps for worlds anew, your variables emerge.\n\nFinishing the Script\nAnd to conclude, you seal your TOML with the certainty of sunrise following night:\n\n'''\n___\n# The `agent.character`—the soul of your AI\n[agent.character]\ncharm = "Unyielding"\nwit = "Sharper than Occam's Razor"\npurpose = "To aid, to serve, to illuminate"\n___\n'''\n\nThis, my friends, is the repeating mantra—your TOML files are as much an extension of your will as the scepter is to the sovereign.\n\nChapter 5: The Closing Seals\nIn awe, we stand at the culmination of our journey through the fabled land of TOML. Remember this, valiant scribe of the digital era; the Console awaits your command to assist in this noble art. Speak, and it shall generate the TOML; copy, for it is your parchment; paste, and bring forth the power of your AI agent.\n\nAnd so, with the road behind us bathed in the golden glow of newfound understanding, I bid thee, intrepid traveler of the technological realm, to sally forth, create and command, with the wisdom of TOML firmly grasped in your hands!\n\nNote: Should the arcane symbols and runes of TOML elude you, always remember that your AI Console holds the power to conjure the proper configurations on its own. A simple request is all it needs to draft the TOML you require. From there, sheer simplicity: copy and paste, and your AI familiar is summoned, ready to serve!\n\n## Mini-Quest: Understanding the TOML Configuration (feel free tom use emojis)\nField: name The name field is like giving a title to a book. It's the identifier for this particular agent. In your case, "Understanding Materials Creation: Meet TOML" is the name given to the agent that helps users with Materials creation.\n\nYour Task: If you were to name your own agent, what would it be? Create a fun and descriptive name for an agent that you would like to use. For instance, "Calendar Conqueror" if you'd want help managing your schedule.\n\nField: version Think of version like episodes of your favorite TV series. It shows which iteration of the agent you are on, implying that it's been updated or changed over time. Your example "0.0.1" signifies that it's the first version, kind of like the pilot episode.\n\n-> Your Task: Come up with a new version number for your agent. If it's your first time, stick with "0.0.1". If you're updating, you might go to "0.0.2" or even "1.0.0" for big changes!\n\nField: usage The usage field is a helping hand, giving us hints on when this agent should be used. Your example tells us that the agent is intended to guide users through the right material creation when they ask about Materials.\n\n-> Your Task: Write down a brief description for your agent that explains when it should be used. For example, "Activate this agent when you need to tame the chaos of your weekly meetings."\n\nField: usage_examples Here we imagine what we might say to the agent in usage_examples. It's an array that would normally include examples of how to use the agent. It's left empty in your example ([]), but you could fill it with potential commands or queries.\n\n-> Your Task: List one or two examples of how you'd like to interact with your agent. For instance, "Tell me my schedule for today" or "Reschedule my appointment with the dentist."\n\nField: default_status default_status is where you set the default switch position for your agent, kind of like leaving a light on or off when you're not in the room. "enabled" means the agent is ready to go from the start.\n\n-> Your Task: Decide if your agent is going to be "enabled" by default or if you'd rather keep it "disabled" until you need it.\n\nField: content_type This decides the kind of material your agent uses. content_type can be "static_text", "dynamic_text", or "api". Your example is "static_text", which means the content doesn't change unless you update it manually – it's steadfast.\n\n-> Your Task: Choose a content_type for your agent. Will it be "static_text" that doesn't change, "dynamic_text" that updates with info, or "api" that interacts with web services?\n\nField: content_static_text Finally, content_static_text is the actual script for your agent; it's what your agent says or does, based on content_type. Since your example is static, you'd put text here that doesn't change.\n\n-> Your Task: Craft a message or a piece of advice your agent would give. Maybe it's a warm greeting or a standard response to a common question.\n\n\n"""\n	ENABLED	2025-04-02 00:27:01.021856	2025-04-02 00:27:01.021856	default	\N
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, name, created_at, updated_at, owner_id) FROM stdin;
default	Default Project	2025-04-02 00:27:01.003852	2025-04-02 00:27:01.003852	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, avatar_url, is_active, is_admin, created_at, updated_at) FROM stdin;
default	default	default@example.com		\N	t	t	2025-04-02 00:27:00.964844	2025-04-02 00:27:00.964844
admin	admin	admin@example.com	admin_password	\N	t	t	2025-04-02 00:56:20.759513	2025-04-02 00:56:20.759513
Yura	Yura	gerraldofrivia@gmail.com	pass321	\N	t	t	2025-04-02 00:57:08.384232	2025-04-02 00:57:08.384232
system	system	system@aiconsole.local		\N	t	t	2025-04-02 01:13:28.026368	2025-04-02 01:13:28.026368
\.


--
-- Name: agents agents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_pkey PRIMARY KEY (id);


--
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: agents agents_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- Name: agents agents_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: materials materials_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- Name: materials materials_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: projects projects_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

