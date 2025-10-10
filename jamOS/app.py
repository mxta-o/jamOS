from flask import Flask, render_template_string
import time

app = Flask(__name__)

# Apps page template
APPS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apps - jamOS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(to bottom right, #1A1F36, #3C4E76);
            min-height: 100vh;
            color: white;
        }

        .navbar {
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-link {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
            background: rgba(176, 196, 222);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
        }

        .nav-links a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: white;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }

        .page-header {
            text-align: center;
            margin-bottom: 4rem;
        }

        .page-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: rgba(176, 196, 222);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .page-subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto;
        }

        .apps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }

        .app-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .app-card:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .app-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }

        .app-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
        }

        .app-description {
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .app-status {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        .status-ready {
            background: rgba(76, 175, 80, 0.2);
            color: #4CAF50;
            border: 1px solid rgba(76, 175, 80, 0.3);
        }

        .status-coming-soon {
            background: rgba(255, 193, 7, 0.2);
            color: #FFC107;
            border: 1px solid rgba(255, 193, 7, 0.3);
        }

        .app-link {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: rgba(176, 196, 222, 0.8);
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .app-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(176, 196, 222, 0.4);
        }

        .app-link.disabled {
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.5);
            cursor: not-allowed;
        }

        .app-link.disabled:hover {
            transform: none;
            box-shadow: none;
        }

        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            
            .apps-grid {
                grid-template-columns: 1fr;
            }
            
            .nav-links {
                display: none;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-content">
            <a href="/" class="logo-link">jamOS</a>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/apps">Apps</a>
                <a href="/roadmap">Roadmap</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">jar's apps</h1>
            <p class="page-subtitle">
                a collection of silly little apps that i just wanted to for shits and giggles
                as well as some that are useful to me personally.
            </p>
        </div>

        <div class="apps-grid">
            <div class="app-card">
                <h3 class="app-title">Rhythm Game Logger</h3>
                <div class="app-status status-coming-soon">Coming Soon</div>
                <p class="app-description">
                    for me to track my scores in rhythm games like osu! and robeats mwehehehe
                </p>
                <a href="/rhythm-logger" class="app-link disabled">Launch App</a>
            </div>

            <div class="app-card">
                <h3 class="app-title">Brain Dump</h3>
                <div class="app-status status-coming-soon">Coming Soon</div>
                <p class="app-description">
                    safe space for me to jot down spontaneous thoughts, and talk about them with my best friend later (chatgpt)
                </p>
                <a href="/brain-dump" class="app-link disabled">Start Writing</a>
            </div>

            <div class="app-card">
                <h3 class="app-title">Pomodoro Timer</h3>
                <div class="app-status status-coming-soon">Coming Soon</div>
                <p class="app-description">
                    timer for me to use when i NEEEEED to lock in and focus my attention span is so cooked guys
                </p>
                <a href="/pomodoro" class="app-link disabled">Start Session</a>
            </div>

            <div class="app-card">
                <h3 class="app-title">Anti Brainfog Generator</h3>
                <div class="app-status status-coming-soon">Coming Soon</div>
                <p class="app-description">
                    im gonna see if i can turn this into a random popup feature instead of an app so that when im doing random things
                    i can get a random task to snap me back into place
                </p>
                <a href="/brainfog-buster" class="app-link disabled">Get Task</a>
            </div>

            <div class="app-card">
                <h3 class="app-title">Letter to Future Me</h3>
                <div class="app-status status-coming-soon">Coming Soon</div>
                <p class="app-description">
                    creating time capsulses for my future self to read either for when i need them or just to see
                    how far ive come, or to reminisce :p
                </p>
                <a href="/time-capsule" class="app-link disabled">Write Letter</a>
            </div>

            <div class="app-card">
                <h3 class="app-title">More Apps Coming</h3>
                <div class="app-status status-coming-soon">In Development</div>
                <p class="app-description">
                    errr if im not lazy i might add more apps in the future, but here you can see the roadmap for what
                    other silly little apps i might add in the future
                </p>
                <a href="/roadmap" class="app-link">View Roadmap</a>
            </div>
        </div>
    </div>
</body>
</html>
"""
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>jamOS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(to bottom right, #1A1F36, #3C4E76);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .hero {
            text-align: center;
            color: white;
            max-width: 800px;
            padding: 2rem;
        }

        .logo {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: rgba(176, 196, 222, 0.9);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .tagline {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            font-weight: 300;
        }

        .description {
            font-size: 1.2rem;
            line-height: 1.6;
            margin-bottom: 3rem;
            opacity: 0.8;
        }

        .cta-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background: rgba(176, 196, 222, 0.8);
            color: white;
            box-shadow: 0 10px 30px rgba(187, 205, 230, 0.2);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }

        .btn-primary:hover {
            box-shadow: 0 15px 40px rgba(176, 196, 222, 0.4);
        }

        .floating-shapes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
        }

        .shape {
            position: absolute;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }

        .shape:nth-child(1) {
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: white;
            border-radius: 50%;
            opacity: 0.6;
            animation: particle 8s linear infinite;
        }

        @keyframes particle {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 0.6;
            }
            90% {
                opacity: 0.6;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }

        @media (max-width: 768px) {
            .logo {
                font-size: 3rem;
            }
            
            .tagline {
                font-size: 1.2rem;
            }
            
            .description {
                font-size: 1rem;
            }
            
            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape">🧊</div>
        <div class="shape">🐋</div>
        <div class="shape">💎</div>
    </div>

    <div class="container">
        <div class="hero">
            <h1 class="logo">jamOS</h1>
            <p class="tagline">welcome :D</p>
            <p class="description">
                helloo ! this is jamOS, a very small project of mine to experiment with Python and Flask.
                not only is it just an introduction of myself, but it includes a collection of apps that I find useful to me personally. have fun exploring :)
            </p>
            
            <div class="cta-buttons">
                <a href="/apps" class="btn btn-primary">Explore Apps</a>
                <a href="/about-me" class="btn btn-secondary">About Me</a>
            </div>
        </div>
        </div>
    </div>

    <script>
        // Create floating particles
        function createParticle() {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 3 + 5) + 's';
            particle.style.animationDelay = Math.random() * 2 + 's';
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 8000);
        }

        // Create particles periodically
        setInterval(createParticle, 300);

        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add entrance animations
        window.addEventListener('load', () => {
            const hero = document.querySelector('.hero');
            const features = document.querySelectorAll('.feature');
            
            hero.style.opacity = '0';
            hero.style.transform = 'translateY(30px)';
            hero.style.transition = 'all 1s ease';
            
            setTimeout(() => {
                hero.style.opacity = '1';
                hero.style.transform = 'translateY(0)';
            }, 100);
            
            features.forEach((feature, index) => {
                feature.style.opacity = '0';
                feature.style.transform = 'translateY(30px)';
                feature.style.transition = 'all 0.8s ease';
                
                setTimeout(() => {
                    feature.style.opacity = '1';
                    feature.style.transform = 'translateY(0)';
                }, 500 + index * 200);
            });
        });
    </script>
</body>
</html>
"""
ABOUTME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - jamOS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(to bottom right, #1A1F36, #3C4E76);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }

        .navbar {
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-link {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
            background: rgba(176, 196, 222);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
        }

        .nav-links a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: white;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }

        .page-header {
            text-align: center;
            margin-bottom: 4rem;
        }

        .page-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: rgba(176, 196, 222);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .page-subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
        }

        .about-content {
            display: flex;
            flex-direction: column;
            gap: 3rem;
        }

        .about-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .about-section:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: rgba(176, 196, 222);
        }

        .section-content {
            line-height: 1.8;
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .highlight {
            background: rgba(193, 227, 247);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .skill-tag {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.8rem 1rem;
            border-radius: 25px;
            text-align: center;
            font-weight: 500;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .skill-tag:hover {
            background: rgba(142, 181, 232, 0.2);
            transform: translateY(-2px);
        }

        .contact-links {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .contact-link {
            padding: 0.8rem 1.5rem;
            background: rgba(117, 161, 217);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .contact-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(117, 161, 217, 0.3);
        }

        .floating-shapes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
            pointer-events: none;
        }

        .shape {
            position: absolute;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
            font-size: 2rem;
        }

        .shape:nth-child(1) {
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }
        .profile-container {
            display: flex;
            gap: 2rem;
            align-items: flex-start;
            flex-wrap: wrap;
        }

        .profile-image {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid rgba(176, 196, 222, 0.5);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            flex-shrink: 0;
        }

        .profile-image:hover {
            transform: scale(1.05);
            border-color: rgba(176, 196, 222, 0.8);
            box-shadow: 0 15px 40px rgba(176, 196, 222, 0.2);
        }

        .profile-text {
            flex: 1;
            min-width: 300px;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }

        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            .profile-container {
                flex-direction: column;
                text-align: center;
            }
            .profile-image {
                width: 150px;
                height: 150px;
                margin: 0 auto 1.5rem auto;
            }
            .nav-links {
                display: none;
            }
            
            .skills-grid {
                grid-template-columns: 1fr;
            }
            
            .contact-links {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape">💭</div>
        <div class="shape">🎯</div>
        <div class="shape">✨</div>
    </div>

    <nav class="navbar">
        <div class="nav-content">
            <a href="/" class="logo-link">jamOS</a>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/apps">Apps</a>
                <a href="/about">About</a>
                <a href="/roadmap">Roadmap</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="page-header">
            <h1 class="page-title">About Me</h1>
            <p class="page-subtitle">The human behind jamOS</p>
        </div>

        <div class="about-content">
            <div class="about-section">
                <h2 class="section-title">Who I Am</h2>
                <div class="section-content">
                    <img src="/static/images/jam.jpg" 
                    alt="Jarlan (Jam)" 
                    class="profile-image">
                <div class="profile-text">
                    hello :O my name is <span class="highlight">jarlan</span>, or <span class="highlight">jam</span>,
                    and i'm the creator of jamOS. i'm an aspiring software developer who loves building tools that help
                    me build better habits and take care of my mental health, and i hope these apps can somewhat
                    help you too :) i am currently a 2nd year university student studying computer science, equipped
                    with a passion for coding and dozens of unfinished projects :yum: 
                    </div>
                </div>
            </div>

            <div class="about-section">
                <h2 class="section-title">My Journey</h2>
                <div class="section-content">
                    like many others, i've struggled with <span class="highlight">brain fog, procrastination, and 
                    mental health mishaps</span>. i found myself overwhelmed by daily tasks and often felt lost 
                    <span class="highlight">staying organized</span>. instead of just dealing with it, i decided to build a <span class="highlight">solution.</span>
                    jamOS started as a personal project - a tiny simple website just to write about me and play around
                    with UI development. as i kept building, it evolved into a collection of apps that i needed for myself.
                    each app is designed to address a specific challenge i faced, whether it was staying focused,
                    organizing my thoughts, or simply finding motivation. i wanted to create a space where i could
                    <span class="highlight">experiment, learn, and share </span>my journey with others who might be going through similar struggles.
                    i hope that by sharing my experiences and the tools i've created, i can help others find their own
                    path to better mental health and productivity. with that being said, i hope you find these apps
                    useful in your own journey, and that you <span class="highlight">have fun ! </span>thanks for reading :)
                </div>
            </div>

            <div class="about-section">
                <h2 class="section-title">What I'm Learning</h2>
                <div class="section-content">
                    this is actually my <span class="highlight">first actual coding project! </span> i'm learning 
                    web development through building things i actually want to use. it's been an invigorating 
                    journey of discovery - from figuring out Flask to designing user experiences that feel 
                    helpful to me and hopefully to you too.
                </div>
                <div class="skills-grid">
                    <div class="skill-tag">Python & Flask</div>
                    <div class="skill-tag">HTML & CSS</div>
                    <div class="skill-tag">JavaScript</div>
                    <div class="skill-tag">UI/UX Design</div>
                    <div class="skill-tag">Git & Version Control</div>
                    <div class="skill-tag">Problem Solving</div>
                </div>
            </div>

            <div class="about-section">
                <h2 class="section-title">Why jamOS?</h2>
                <div class="section-content">
                    some of my friends call me jam as a nickname lols, and as this is a personal project for myself, i
                    wanted to make it a personal space obviously.
                </div>
            </div>

            <div class="about-section">
                <h2 class="section-title">Let's Connect</h2>
                <div class="section-content">
                    i'd love to hear from you! :D whether you have feedback on the apps, want to share your own 
                    productivity struggles, or just want to say hi - i'm always down to meet and connect with
                    like-minded people. feel free to reach out through any of the links below :)
                </div>
                <div class="contact-links">
                    <a href="mailto:jaelancruz@yahoo.com" class="contact-link">
                        send me an email :]
                    </a>
                    <a href="https://www.linkedin.com/in/jaelan-cruz/" class="contact-link" target="_blank">
                        LinkedIn
                    </a>
                    <a href="https://github.com/mxta-o" class="contact-link" target="_blank">
                        GitHub
                    </a>
                    <a href="https://guns.lol/jarlan" class="contact-link" target="_blank">
                        Misc Socials
                    </a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
POMODORO_TIMER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apps - jamOS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(to bottom right, #1A1F36, #3C4E76);
            min-height: 100vh;
            color: white;
        }

        .navbar {
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-link {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
            background: rgba(176, 196, 222);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
        }

        .nav-links a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: white;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }

        .page-header {
            text-align: center;
            margin-bottom: 4rem;
        }

        .page-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: rgba(176, 196, 222);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
        }

        .pomodoro-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            position: center;
            text-align: center;
            margin: 0 auto;
            width: 70%;
        }

        .pomodoro-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }

        .pomodoro-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .page-subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto;
        }

        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            
            .apps-grid {
                grid-template-columns: 1fr;
            }
            
            .nav-links {
                display: none;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-content">
            <a href="/" class="logo-link">jamOS</a>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/apps">Apps</a>
                <a href="/roadmap">Roadmap</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="page-header">
            <h1 class="page-title">jar's pomorodo timer :D</h1>
            <p class="page-subtitle">
                simple pomodoro timer to use in case you need to lock in :p
            </p>
        </div>
    </div>
    <div class="pomodoro-card">
        <h3 class="pomodoro-title">Pomodoro Timer</h3>
        <img src="/images/oshawottyay.gif" alt="Pomodoro Timer Icon" class="pomodoro-icon">
        <a href="/pomodoro" class="app-link disabled">Start Session</a>
    </div>
</body>
</html>
"""
@app.route('/')
def home():
    return render_template_string(LANDING_PAGE)

@app.route('/apps')
def apps():
    return render_template_string(APPS_PAGE)

@app.route('/about-me')
def about_me():
    return render_template_string(ABOUTME_PAGE)

@app.route('/brain-dump')
def brain_dump():
    return "<h1>Brain Dump</h1><p>Your safe space for thoughts - Coming soon!</p>"

@app.route('/rhythm-logger')
def rhythm_logger():
    return "<h1>Rhythm Game Logger</h1><p>Track your scores - Coming soon!</p>"

@app.route('/pomodoro')
def pomodoro():
    return render_template_string(POMODORO_TIMER)

@app.route('/brainfog-buster')
def brainfog_buster():
    return "<h1>Anti Brainfog Generator</h1><p>Instant motivation - Coming soon!</p>"

@app.route('/time-capsule')
def time_capsule():
    return "<h1>Letter to Future Me</h1><p>Time capsules - Coming soon!</p>"

@app.route('/roadmap')
def roadmap():
    return "<h1>jamOS Roadmap</h1><p>What's coming next - Coming soon!</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
