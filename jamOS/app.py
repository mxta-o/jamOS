from flask import Flask, render_template_string

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
    <title>jamOS - The Future of Operating Systems</title>
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

        .features {
            margin-top: 4rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            max-width: 1000px;
        }

        .feature {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .feature:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.15);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .feature h3 {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: white;
        }

        .feature p {
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        .feature-link {
            color: #4ecdc4;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            display: inline-block;
        }

        .feature-link:hover {
            color: #ff6b6b;
            transform: translateX(5px);
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
            
            .features {
                grid-template-columns: 1fr;
                margin-top: 2rem;
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

@app.route('/')
def home():
    return render_template_string(LANDING_PAGE)

@app.route('/apps')
def apps():
    return render_template_string(APPS_PAGE)

@app.route('/about-me')
def about_me():
    return "<h1>About Me</h1><p>hi there ! I'm jarlan, or jam as my friends call me, an aspiring software enthusiast exploring the world of Python and Flask.</p>"

@app.route('/brain-dump')
def brain_dump():
    return "<h1>Brain Dump</h1><p>Your safe space for thoughts - Coming soon!</p>"

@app.route('/rhythm-logger')
def rhythm_logger():
    return "<h1>Rhythm Game Logger</h1><p>Track your scores - Coming soon!</p>"

@app.route('/pomodoro')
def pomodoro():
    return "<h1>Pomodoro Timer</h1><p>Focus sessions - Coming soon!</p>"

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
    app.run(debug=True, host='0.0.0.0', port=5000)
