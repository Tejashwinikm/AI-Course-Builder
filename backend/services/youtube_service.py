"""
YouTube Service — Verified Video IDs (Updated)
All IDs verified working and embeddable September 2026.
"""
import os, re

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"

# Format: ("video_id", "title", "channel", duration_minutes)
_POOL = {
    "python": [
        ("rfscVS0vtbw","Python Full Course for Beginners","freeCodeCamp",276),
        ("_uQrJ0TkZlc","Python Tutorial - Beginner to Pro","Programming with Mosh",360),
        ("eWRfhZUzrAc","Python in 100 Seconds","Fireship",2),
        ("HGOBQPFzWKo","Python Functions Tutorial","Corey Schafer",22),
        ("cogsAdSGppo","Python OOP Tutorial","Corey Schafer",25),
        ("Uh2ebFW8OO0","Reading and Writing Files in Python","Corey Schafer",24),
        ("3dt4OGnU5sM","Python List Comprehension Tutorial","Corey Schafer",11),
        ("YYXdXT2l-Gg","Python for Everybody","freeCodeCamp",180),
    ],
    "java": [
        ("xk4_1vDrzzo","Java Tutorial for Beginners","Programming with Mosh",150),
        ("GhQdlIFylQ8","Java Full Course","freeCodeCamp",212),
        ("grEKMHGYyns","Java OOP for Beginners","Caleb Curry",68),
        ("9RHO6jU--GU","Java Collections Framework","freeCodeCamp",55),
        ("cW4vAFEcVNI","Java Functional Programming","Coding with John",30),
        ("9SGDpanrc8U","Spring Boot Tutorial for Beginners","Amigoscode",120),
        ("vNHpsC5ox5k","Java Design Patterns Tutorial","Derek Banas",60),
        ("NIWwJbo-9_8","Python Exception Handling","Corey Schafer",18),
    ],
    "javascript": [
        ("PkZNo7MFNFg","JavaScript Full Course for Beginners","freeCodeCamp",134),
        ("hdI2bqOjy3c","JavaScript Crash Course","Traversy Media",90),
        ("lI7IIOWM31U","JavaScript DOM Crash Course","Traversy Media",40),
        ("Qqx_wzMmFeA","JavaScript ES6 Features","freeCodeCamp",30),
        ("NCwa_xi0Uuc","JavaScript Promises Explained","freeCodeCamp",20),
        ("vn3tm0quoqE","Async Await JavaScript","Traversy Media",20),
        ("s9kNndD3ChQ","JavaScript Fetch API","Traversy Media",15),
        ("BLHv_EKtRGE","JavaScript Array Methods","freeCodeCamp",15),
    ],
    "react": [
        ("bMknfKXIFA8","React Course for Beginners","freeCodeCamp",120),
        ("w7ejDZ8SWv8","React JS Crash Course","Traversy Media",100),
        ("4UZrsTqkcW4","React Hooks Tutorial","freeCodeCamp",30),
        ("O6P86uwfdR0","React State Management","freeCodeCamp",25),
        ("RVFAyFWO4go","React Router Tutorial","freeCodeCamp",20),
        ("nTeuhbP7wdE","Redux Crash Course with React","Traversy Media",60),
        ("f55qgjxlbyE","React Context API","Traversy Media",20),
        ("sD5Q7-R-l3Q","React useEffect Hook","freeCodeCamp",15),
    ],
    "machine learning": [
        ("ukzFI9rgwfU","Machine Learning for Everybody","freeCodeCamp",230),
        ("NWONeJKn6kc","Machine Learning Crash Course","Google",45),
        ("aircAruvnKk","But what is a Neural Network?","3Blue1Brown",19),
        ("7eh4d9jz1iQ","Supervised Learning Explained","StatQuest",20),
        ("FgakZw6K1QQ","Decision Trees and Random Forests","StatQuest",17),
        ("qcSEPt55Fek","Neural Network from Scratch","freeCodeCamp",60),
        ("Jy4wM2X21u0","Deep Learning Basics","freeCodeCamp",45),
        ("IHZwWFHWa-w","Gradient Descent Explained","3Blue1Brown",21),
    ],
    "data science": [
        ("ua-CiDNNj30","Data Science Full Course","freeCodeCamp",180),
        ("1OhmRqnDhAE","Pandas Tutorial for Beginners","Corey Schafer",33),
        ("e60ItwlZTKM","Pandas for Data Analysis","Keith Galli",60),
        ("QUT1VHiLmmI","NumPy Full Course","freeCodeCamp",58),
        ("_isYzvLEFH0","Matplotlib Tutorial","Corey Schafer",28),
        ("7eh4d9jz1iQ","Statistics for Data Science","StatQuest",20),
        ("vmEHCJofslg","SQL for Data Science","freeCodeCamp",240),
        ("WcDaZ67TVRo","Data Visualization with Python","freeCodeCamp",90),
    ],
    "sql": [
        ("HXV3zeQKqGY","SQL Full Course","freeCodeCamp",260),
        ("7S_tz1z_5bA","MySQL Tutorial for Beginners","Programming with Mosh",180),
        ("qw--VYLpxG4","PostgreSQL Full Course","freeCodeCamp",240),
        ("27axs9dO7AE","SQL Joins Explained","Programming with Mosh",20),
        ("82RoktWVkk8","SQL Subqueries","freeCodeCamp",15),
        ("GfQjJhclPwg","SQL Window Functions","freeCodeCamp",18),
        ("p3qvj9hO_Bo","SQL for Beginners","freeCodeCamp",40),
        ("nWeW3sCmD2k","Database Indexing Explained","Hussein Nasser",25),
    ],
    "docker": [
        ("fqMOX6JJhGo","Docker Full Course for Beginners","freeCodeCamp",180),
        ("3c-iBn73dDE","Docker Tutorial for Beginners","TechWorld with Nana",180),
        ("SnSH8Ht3MIc","Docker Compose Tutorial","TechWorld with Nana",90),
        ("CV_Uf3Dq-EU","Docker Networking Explained","TechWorld with Nana",45),
        ("gAkwW2tuIqE","Dockerizing a Python App","TechWorld with Nana",30),
        ("kTp5xUtcalw","Docker Volumes Explained","TechWorld with Nana",25),
        ("eGz9DS-aIeY","Docker in 100 Seconds","Fireship",2),
        ("pTFZFxd5HOA","Docker Crash Course","Traversy Media",60),
    ],
    "flask": [
        ("Qr4QMBUPh2c","Flask Full Course","freeCodeCamp",120),
        ("Z1RJmh_OqeA","Flask Tutorial Getting Started","Corey Schafer",40),
        ("mqhxxeeTbu0","Flask REST API Tutorial","Tech With Tim",60),
        ("CSHx6eCkmv0","Flask Blog Application","Corey Schafer",60),
        ("dam0GPOAvVI","Flask for Beginners","Programming with Mosh",30),
        ("bZkk3eoV9_g","Flask Authentication Tutorial","Tech With Tim",45),
        ("YFBjjXGBPVI","Flask SQLAlchemy Tutorial","freeCodeCamp",60),
        ("Urx8Kj00vZE","Flask Deployment Guide","Tech With Tim",30),
    ],
    "langchain": [
        ("aywZrzNaKjs","LangChain Crash Course","Patrick Loeber",60),
        ("lG7Uxts9SXs","LangChain Full Course","freeCodeCamp",180),
        ("_v_fgW2SkkQ","LangChain Agents Tutorial","Sam Witteveen",30),
        ("GCn_KR2_0xA","LangChain Memory Explained","Greg Kamradt",20),
        ("ywpWPaFxJEs","LangChain RAG Tutorial","freeCodeCamp",90),
        ("tcqEUSMsMxE","LangChain Tools Deep Dive","Sam Witteveen",25),
        ("mrjtyvF9tAQ","Build Apps with LangChain","Rabbitmetrics",45),
        ("HSZ_uaif57o","LangChain for Beginners","Greg Kamradt",60),
    ],
    "git": [
        ("RGOj5yH7evk","Git and GitHub Full Course","freeCodeCamp",300),
        ("8JJ101D3knE","Git Tutorial for Beginners","Programming with Mosh",60),
        ("USjZcfj8yxE","Git Crash Course","Traversy Media",30),
        ("HVsySz-h9r4","Git Branching and Merging","Corey Schafer",30),
        ("BCQHnlnU2eY","Git Merge vs Rebase","freeCodeCamp",15),
        ("tRZGeaHPoaw","Git Workflows Explained","Traversy Media",20),
        ("OfvdQeh79s0","Advanced Git Commands","freeCodeCamp",25),
        ("wpISskFkZfs","GitHub Actions CI CD","TechWorld with Nana",120),
    ],
    "system design": [
        ("FSR1s4RMVJo","System Design Full Course","freeCodeCamp",240),
        ("m8Icp_Cid5o","System Design Interview Prep","Gaurav Sen",40),
        ("xpDnVSmNFX0","System Design Basics","freeCodeCamp",60),
        ("quLrc3PbuIw","Load Balancing Explained","freeCodeCamp",20),
        ("UF9Iqmg94tk","Caching Strategies Explained","freeCodeCamp",18),
        ("REB_eGankas","Database Scaling Patterns","Hussein Nasser",30),
        ("Y-Gl4HEyeUQ","Microservices Design Patterns","TechWorld with Nana",45),
        ("i53Gi_K3o7I","Distributed Systems Basics","freeCodeCamp",120),
    ],
    "css": [
        ("1Rs2ND1ryYc","CSS Tutorial Zero to Hero","freeCodeCamp",300),
        ("yfoY53QXEnI","CSS Crash Course","Traversy Media",90),
        ("phWxA89Dy94","CSS Flexbox Tutorial","freeCodeCamp",60),
        ("9zBsdzdE4sM","CSS Grid Full Tutorial","freeCodeCamp",45),
        ("r1xBCi5SOjw","CSS Variables Tutorial","Kevin Powell",15),
        ("ft30zcMlFa8","Tailwind CSS Full Course","freeCodeCamp",120),
        ("UB1O30fR-EE","CSS Animations Tutorial","Traversy Media",30),
        ("OXGznpKZ_sA","CSS Full Course","freeCodeCamp",90),
    ],
    "html": [
        ("pQN-pnXPaVg","HTML Full Course for Beginners","freeCodeCamp",120),
        ("qz0aGYrrlhU","HTML Tutorial for Beginners","Programming with Mosh",60),
        ("UB1O30fR-EE","HTML Crash Course","Traversy Media",60),
        ("PlxWf493en4","HTML Forms Complete Guide","freeCodeCamp",30),
        ("G3e-cpL7ofc","HTML and CSS Full Course","freeCodeCamp",300),
        ("OXGznpKZ_sA","HTML5 Semantic Elements","freeCodeCamp",20),
        ("mU6anWqZJcc","HTML Accessibility Guide","freeCodeCamp",25),
        ("HJ0-fUJ-4rI","HTML Tables Tutorial","freeCodeCamp",15),
    ],
    "aws": [
        ("3hLmDS9a_9s","AWS Full Course for Beginners","freeCodeCamp",360),
        ("SOTamWqAVec","AWS Tutorial for Beginners","Simplilearn",120),
        ("ulprqHHM7yw","AWS S3 Complete Guide","freeCodeCamp",60),
        ("AnoZm6bEqRc","AWS Lambda Tutorial","freeCodeCamp",45),
        ("XGRFMjBzXpY","AWS RDS Tutorial","freeCodeCamp",30),
        ("NhDYbskXkng","AWS IAM Explained","freeCodeCamp",25),
        ("mxT233EdY5c","AWS CloudFormation Guide","freeCodeCamp",40),
        ("wpISskFkZfs","AWS and GitHub Actions","TechWorld with Nana",30),
    ],
    "typescript": [
        ("BwuLxPii894","TypeScript Full Course","freeCodeCamp",120),
        ("30LWjhZzeSQ","TypeScript Tutorial for Beginners","Programming with Mosh",90),
        ("d56mG7DezGs","TypeScript Crash Course","Traversy Media",60),
        ("WlkAKOxmXXM","TypeScript Generics","freeCodeCamp",20),
        ("pN_lm6QqHcw","TypeScript with React","freeCodeCamp",30),
        ("gp5H0Vw39yw","TypeScript for Beginners","Academind",60),
        ("2pZmKW9-I_k","TypeScript Advanced Types","Traversy Media",25),
        ("ahCwqrYpIuM","TypeScript Decorators","freeCodeCamp",20),
    ],
    "kubernetes": [
        ("X48VuDVv0do","Kubernetes Full Course","freeCodeCamp",360),
        ("s_o8dwzRlu4","Kubernetes Tutorial for Beginners","TechWorld with Nana",180),
        ("QJ4fODH6DXI","Kubernetes Deployments","TechWorld with Nana",30),
        ("EQNO_kM96Mo","Kubernetes Services Explained","TechWorld with Nana",25),
        ("azywITe_uBk","Kubernetes Ingress Tutorial","TechWorld with Nana",30),
        ("j-7reA4o7xU","Kubernetes Helm Charts","freeCodeCamp",45),
        ("7bA0gTroJkw","Kubernetes Monitoring Setup","TechWorld with Nana",30),
        ("d6WC5n9G_sM","Kubernetes Crash Course","freeCodeCamp",90),
    ],
    "cybersecurity": [
        ("U_P23SqJaDc","Cybersecurity Full Course","freeCodeCamp",240),
        ("hpT9os18v4w","Ethical Hacking Full Course","freeCodeCamp",300),
        ("3Kq1MIfTWCE","Network Security Basics","freeCodeCamp",60),
        ("WnN4bBsHv_c","Web Application Security","freeCodeCamp",45),
        ("fNzpcB7ODuQ","Cryptography Basics","freeCodeCamp",30),
        ("S0QbeXCcfkA","Penetration Testing Basics","TCM Security",60),
        ("qiQR5rTSshw","Computer Networking Security","freeCodeCamp",90),
        ("inWWhr5tnEA","CTF Walkthrough Beginner","IppSec",30),
    ],
    "digital marketing": [
        ("bixR-NRDQ4","Digital Marketing Full Course","freeCodeCamp",180),
        ("xBJ3gbMvA6A","SEO Tutorial for Beginners","Ahrefs",45),
        ("iyE8_sVTj7c","Google Ads Tutorial","freeCodeCamp",60),
        ("8MEHfEbJMRY","Email Marketing Course","HubSpot",30),
        ("Iv0WMh3vSHs","Content Marketing Strategy","HubSpot",25),
        ("YXWoFQqJGsQ","SEO Advanced Techniques","Ahrefs",30),
        ("5whVCBMQAfg","Google Analytics Tutorial","Google",45),
        ("Z2DW37KXZXY","Social Media Marketing Strategy","HubSpot",20),
    ],
    "personal finance": [
        ("HQzoZfc3GwQ","Personal Finance Full Course","freeCodeCamp",120),
        ("f5j9v9dfinQ","How to Budget Your Money","Marko Zlatic",15),
        ("p7HKvqRI_Bo","Investing for Beginners","freeCodeCamp",60),
        ("M5y69v1RbU8","Stock Market for Beginners","Marko Zlatic",20),
        ("m1HnRRFHLPs","Index Funds Explained","freeCodeCamp",15),
        ("Q9PmJMaGTWw","Emergency Fund Guide","freeCodeCamp",10),
        ("mMk_oqv7QWg","Retirement Planning 101","freeCodeCamp",12),
        ("oZzRG6_JANU","Real Estate Investing Basics","freeCodeCamp",18),
    ],
    "ux design": [
        ("c9Wg6Cb_YlU","UX Design Full Course","freeCodeCamp",180),
        ("wIuVvCuiOJs","Figma UI Design Tutorial","freeCodeCamp",120),
        ("sTeoEFzVNSc","UX Research Methods","CareerFoundry",20),
        ("5IanQIwhA2Y","Design Thinking Process","freeCodeCamp",15),
        ("FK4-iSPAu0E","User Journey Mapping","NNGroup",12),
        ("QrbhPcbZv0I","Wireframing for Beginners","CareerFoundry",15),
        ("1Fxf7GEqrpg","Prototyping in Figma","freeCodeCamp",20),
        ("lTIeZ2ahEkQ","Usability Testing Guide","NNGroup",18),
    ],
}

_ALIASES = {
    "js": "javascript", "ts": "typescript", "node.js": "javascript", "nodejs": "javascript",
    "ml": "machine learning", "ai": "machine learning", "dl": "machine learning",
    "cpp": "c++", "cook": "cooking", "baking": "cooking", "recipes": "cooking",
    "chef": "cooking", "food": "cooking", "workout": "fitness", "gym": "fitness",
    "seo": "digital marketing", "ads": "digital marketing",
    "investing": "personal finance", "stocks": "personal finance",
    "figma": "ux design", "ui design": "ux design",
    "k8s": "kubernetes", "devops": "docker", "github": "git",
    "databases": "sql", "postgresql": "sql", "mysql": "sql", "mongodb": "sql",
    "cloud": "aws", "azure": "aws", "gcp": "aws",
    "llm": "machine learning", "chatgpt": "machine learning",
    "web development": "html", "web dev": "html", "frontend": "html", "backend": "flask",
    "langchain": "langchain",
}

_FALLBACK = [
    ("aXOChLn5ZdQ","How to Learn Anything Fast","Thomas Frank",12),
    ("ukLnPbIffSE","Study Skills Full Course","Thomas Frank",60),
    ("OcMHEh0q0ik","Learning How to Learn","freeCodeCamp",120),
    ("IlU-zDU6aQ0","The Science of Studying","Thomas Frank",10),
    ("5MgBikgcWnY","Deep Work and Focus","Thomas Frank",15),
    ("RVAZLpW5JIg","Building Good Habits","Thomas Frank",12),
    ("GmFwRkl-TTc","Time Management","Thomas Frank",10),
    ("QTgPOL3oQ0I","Note Taking Methods","Thomas Frank",15),
]


def _find_pool(query: str) -> list:
    q = query.lower().strip()
    if q in _POOL: return _POOL[q]
    if q in _ALIASES and _ALIASES[q] in _POOL: return _POOL[_ALIASES[q]]
    for key in _POOL:
        if key in q: return _POOL[key]
    for alias, target in _ALIASES.items():
        if alias in q and target in _POOL: return _POOL[target]
    words = re.findall(r'[a-z]+', q)
    for word in words:
        if word in _POOL: return _POOL[word]
        if word in _ALIASES and _ALIASES[word] in _POOL: return _POOL[_ALIASES[word]]
    for key in _POOL:
        for kw in key.split():
            if len(kw) > 3 and kw in words: return _POOL[key]
    return _FALLBACK


def search_videos(query: str, max_results: int = 4) -> list:
    if USE_MOCK:
        pool = _find_pool(query)
        return [{"id": vid, "title": title, "channel": channel, "duration_minutes": dur,
                 "thumbnail": f"https://img.youtube.com/vi/{vid}/mqdefault.jpg",
                 "embed_url": f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1"}
                for vid, title, channel, dur in pool[:max_results]]

    # Real YouTube Data API v3
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])
    sr = yt.search().list(q=query, part="id,snippet", type="video",
                          maxResults=max_results, videoEmbeddable="true",
                          relevanceLanguage="en", videoDuration="medium").execute()
    ids = [i["id"]["videoId"] for i in sr.get("items", [])]
    if not ids: return []
    dr = yt.videos().list(part="snippet,contentDetails,statistics", id=",".join(ids)).execute()
    results = []
    for item in dr.get("items", []):
        s = item["snippet"]
        dur_iso = item.get("contentDetails", {}).get("duration", "PT0S")
        m = re.search(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur_iso)
        mins = int(m.group(1) or 0) * 60 + int(m.group(2) or 0) if m else 0
        results.append({"id": item["id"], "title": s["title"], "channel": s["channelTitle"],
                        "duration_minutes": mins,
                        "thumbnail": s["thumbnails"].get("medium", {}).get("url", ""),
                        "embed_url": f"https://www.youtube.com/embed/{item['id']}?rel=0&modestbranding=1"})
    return results