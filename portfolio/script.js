document.addEventListener('DOMContentLoaded', () => {

    // --- Mobile Menu ---
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            const isFlex = navLinks.style.display === 'flex';

            if (!isFlex) {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.background = '#FFFFFF';
                navLinks.style.borderBottom = '3px solid #121212';
                navLinks.style.padding = '20px';
                menuBtn.textContent = 'CLOSE';
                menuBtn.style.background = '#FFDE59';
            } else {
                navLinks.style.display = ''; // Revert to CSS
                menuBtn.textContent = 'MENU';
                menuBtn.style.background = '';
            }
        });
    }

    // --- Hover Glitch Effect on Hero Title ---
    const glitchText = document.querySelector('.glitch-text');
    if (glitchText) {
        glitchText.addEventListener('mouseover', () => {
            glitchText.style.color = '#ff00ea'; // Neon Magenta
            glitchText.style.textShadow = '0 0 20px #ff00ea';
            glitchText.textContent = 'SYS.OVERRIDE()';

            setTimeout(() => {
                glitchText.textContent = glitchText.getAttribute('data-text');
                glitchText.style.color = '';
                glitchText.style.textShadow = '';
            }, 300);
        });
    }
    // --- Custom Cursor Logic (Target Tracker) ---
    const cursorDot = document.querySelector('.cursor-dot');
    const cursorOutline = document.querySelector('.cursor-outline');

    if (cursorDot && cursorOutline) {
        window.addEventListener('mousemove', (e) => {
            const posX = e.clientX;
            const posY = e.clientY;

            // Dot follows instantly
            cursorDot.style.left = `${posX}px`;
            cursorDot.style.top = `${posY}px`;

            // Tracking outline follows with a spring effect
            cursorOutline.animate({
                left: `${posX}px`,
                top: `${posY}px`
            }, { duration: 150, fill: "forwards", easing: "ease-out" });
        });

        // Hover Effect on Links
        document.querySelectorAll('a, button, .btn, .hover-link').forEach(el => {
            el.addEventListener('mouseenter', () => {
                document.body.classList.add('hovering');
            });
            el.addEventListener('mouseleave', () => {
                document.body.classList.remove('hovering');
            });
        });
    }

    // --- ADDING 3D TILT & GLOW TRACKING ---
    const cards = document.querySelectorAll('.brutal-box, .project-row, .veille-section-block');

    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Set CSS variables for the spotlight gradient
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);

            // Subtle 3D Tilt calculation
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            // Limit tilt to 4 degrees max to keep it smooth
            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            // Move glow out of sight when mouse leaves
            setTimeout(() => {
                card.style.setProperty('--mouse-x', `-1000px`);
                card.style.setProperty('--mouse-y', `-1000px`);
            }, 300);
        });
    });

    // --- GOOGLE ALERTS / NEWS API FOR VEILLE TECHNO ---
    async function fetchVeilleAlerts() {
        const resultsContainer = document.getElementById('veille-api-results');
        if (!resultsContainer) return;

        // RSS feed URL for Google News search string "cybersécurité cloud"
        const rssUrl = encodeURIComponent('https://news.google.com/rss/search?q=cybers%C3%A9curit%C3%A9+cloud&hl=fr&gl=FR&ceid=FR:fr');
        // Using rss2json API to convert XML RSS to JSON
        const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${rssUrl}`;

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error('API Request Failed');
            
            const data = await response.json();
            
            if (data && data.items && data.items.length > 0) {
                resultsContainer.innerHTML = ''; // Clear loading message
                
                // Get top 3 latest articles
                const topArticles = data.items.slice(0, 3);
                
                topArticles.forEach(article => {
                    const date = new Date(article.pubDate).toLocaleDateString('fr-FR', {
                        day: '2-digit', month: '2-digit', year: 'numeric'
                    });
                    
                    const card = document.createElement('div');
                    card.className = 'veille-article-card hover-link';
                    
                    // We also remove the " - source" from the title if present in google news
                    const cleanTitle = article.title.split(' - ')[0];

                    card.innerHTML = `
                        <div>
                            <span class="veille-article-date">>[LOG_DATE]: ${date}</span>
                            <h4 class="veille-article-title">${cleanTitle}</h4>
                        </div>
                        <a href="${article.link}" target="_blank" class="veille-article-link">
                            [DECRYPT] <i class="fas fa-external-link-alt"></i>
                        </a>
                    `;
                    resultsContainer.appendChild(card);
                });
            } else {
                resultsContainer.innerHTML = `<div class="veille-loading-msg" style="color: var(--accent-red)"><i class="fas fa-exclamation-triangle"></i> ERROR: NO DATA FOUND IN STREAM</div>`;
            }
        } catch (error) {
            console.error('Error fetching veille data:', error);
            resultsContainer.innerHTML = `<div class="veille-loading-msg" style="color: var(--accent-red)"><i class="fas fa-exclamation-triangle"></i> ERROR: CONNECTION TO DATA STREAM FAILED</div>`;
        }
    }

    // Initialize fetching data
    fetchVeilleAlerts();
});
