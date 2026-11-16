document.addEventListener('DOMContentLoaded', () => {

    /* --- TYPEWRITER EFFECT --- */
    const heroStatus = document.querySelector('.status');
    const textToType = "SYSTEM: ONLINE_";
    if (heroStatus) {
        heroStatus.textContent = "";
        let charIndex = 0;
        function typeWriter() {
            if (charIndex < textToType.length) {
                heroStatus.textContent += textToType.charAt(charIndex);
                charIndex++;
                setTimeout(typeWriter, 100);
            } else {
                setInterval(() => {
                    if (heroStatus.textContent.endsWith('_')) {
                        heroStatus.textContent = heroStatus.textContent.slice(0, -1);
                    } else {
                        heroStatus.textContent += '_';
                    }
                }, 800);
            }
        }
        setTimeout(typeWriter, 1000);
    }

    /* --- MOBILE MENU --- */
    const menuBtn = document.querySelector('.menu-btn');
    const menu = document.querySelector('.hud-nav .menu');

    if (menuBtn && menu) {
        menuBtn.addEventListener('click', () => {
            menu.classList.toggle('open');
            const icon = menuBtn.querySelector('i');
            if (menu.classList.contains('open')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });

        // Fermer le menu au clic sur un lien
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('open');
                const icon = menuBtn.querySelector('i');
                icon.className = 'fas fa-bars';
            });
        });
    }

    /* --- SCROLL OBSERVER (Animations) --- */
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.classList.remove('hidden');

                // Animate skill bars
                if (entry.target.classList.contains('skill-bar-container')) {
                    const bar = entry.target.querySelector('.fill');
                    if (bar) {
                        const targetWidth = bar.style.width;
                        bar.style.width = '0';
                        setTimeout(() => { bar.style.width = targetWidth; }, 150);
                    }
                }
            }
        });
    }, observerOptions);

    document.querySelectorAll('.hidden').forEach(el => {
        observer.observe(el);
    });

    /* --- CONTACT FORM --- */
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('.btn-send');
            const originalText = btn.textContent;
            const username = document.getElementById('username').value;
            const msg = document.getElementById('message').value;
            const myEmail = "amokranerosa123@gmail.com";
            const subject = encodeURIComponent(`Contact Portfolio — ${username}`);
            const body = encodeURIComponent(`Nom: ${username}\n\nMessage:\n${msg}`);

            btn.textContent = "SENDING...";
            btn.disabled = true;
            window.location.href = `mailto:${myEmail}?subject=${subject}&body=${body}`;

            setTimeout(() => {
                btn.textContent = "MESSAGE ENVOYÉ!";
                btn.style.background = "var(--sentinel-green)";
                btn.style.color = "var(--bg-dark)";

                const chatLog = document.querySelector('.chat-log');
                if (chatLog) {
                    const newLog = document.createElement('p');
                    newLog.className = 'system-msg';
                    newLog.innerHTML = `> <strong>${username}</strong>: ${msg}`;
                    chatLog.appendChild(newLog);
                    chatLog.scrollTop = chatLog.scrollHeight;
                }

                form.reset();
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = "";
                    btn.style.color = "";
                    btn.disabled = false;
                }, 3000);
            }, 1200);
        });
    }

    /* --- PHARMASI IMAGE GALLERY (auto-slideshow) --- */
    const galleries = document.querySelectorAll('.quest-img-gallery');
    galleries.forEach(gallery => {
        const slides = gallery.querySelectorAll('.quest-img');
        const dots = gallery.querySelectorAll('.dot');
        let current = 0;

        function showSlide(index) {
            slides.forEach(s => { s.classList.remove('active-slide'); s.style.position = 'absolute'; s.style.opacity = '0'; });
            dots.forEach(d => d.classList.remove('active'));
            slides[index].style.position = 'relative';
            slides[index].style.opacity = '1';
            slides[index].classList.add('active-slide');
            if (dots[index]) dots[index].classList.add('active');
        }

        // Dots click
        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => { current = i; showSlide(current); });
        });

        // Auto-advance every 2.5s
        setInterval(() => {
            current = (current + 1) % slides.length;
            showSlide(current);
        }, 2500);
    });

    /* --- VEILLE DYNAMIQUE --- */
    const veilleGrid = document.getElementById('veille-grid');
    const veilleTags = document.querySelectorAll('.veille-tag');
    let currentTag = 'ai';

    function formatDate(dateStr) {
        const d = new Date(dateStr);
        return `${String(d.getDate()).padStart(2, '0')}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`;
    }

    function truncateText(text, maxLen = 120) {
        if (!text) return 'Cliquez pour lire l\'article complet...';
        const stripped = text.replace(/<[^>]*>/g, '');
        return stripped.length > maxLen ? stripped.substring(0, maxLen) + '...' : stripped;
    }

    async function fetchArticles(tag) {
        if (!veilleGrid) return;
        veilleGrid.innerHTML = `<div class="news-card loading-card"><div class="news-date">SCANNING [${tag.toUpperCase()}]...</div><h4>Récupération des données...</h4></div>`;

        let url;
        let isRSS = false;

        try {
            if (tag === 'cybersecurity') {
                // Google Alerts RSS via rss2json
                const googleRssUrl = "https://news.google.com/rss/search?q=cybersecurite+securite+informatique&hl=fr&gl=FR&ceid=FR:fr";
                url = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(googleRssUrl)}`;
                isRSS = true;
            } else {
                url = `https://dev.to/api/articles?tag=${tag}&per_page=6&top=7`;
                isRSS = false;
            }

            const response = await fetch(url);
            if (!response.ok) throw new Error(`Erreur réseau : ${response.status}`);
            const data = await response.json();

            const articles = isRSS ? data.items : data;

            if (!articles || articles.length === 0) {
                veilleGrid.innerHTML = `<div class="news-card"><div class="news-date">SCAN COMPLETE</div><h4>Aucun article trouvé pour: ${tag}</h4></div>`;
                return;
            }

            veilleGrid.innerHTML = '';

            articles.forEach((article, index) => {
                const title = article.title || 'Sans titre';
                const link = isRSS ? article.link : article.url;
                const date = isRSS ? article.pubDate : article.published_at;
                const desc = isRSS ? article.description : article.description;
                const authorName = (article.user && article.user.name) ? article.user.name : (isRSS ? 'RSS' : 'Anonyme');
                const reactions = article.positive_reactions_count || 0;
                const meta = isRSS ? '📡 GOOGLE_NEWS' : `✍ ${authorName} | ❤ ${reactions}`;

                const card = document.createElement('a');
                card.href = link;
                card.target = '_blank';
                card.rel = 'noopener noreferrer';
                card.className = 'news-card hidden';
                card.style.animationDelay = `${index * 0.1}s`;
                card.innerHTML = `
                    <div class="news-date">${formatDate(date)}</div>
                    <h4>${title}</h4>
                    <p>${truncateText(desc)}</p>
                    <div class="news-meta"><span class="news-author">${meta}</span><span class="news-reactions">${isRSS ? '' : `❤ ${reactions}`}</span></div>
                `;
                veilleGrid.appendChild(card);
                observer.observe(card);
            });

        } catch (error) {
            console.error("Erreur veille :", error);
            veilleGrid.innerHTML = `<div class="news-card"><div class="news-date">ERROR</div><h4>Connexion échouée ou flux vide.</h4><p>Vérifiez votre connexion internet.</p></div>`;
        }
    }

    veilleTags.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const clickedBtn = e.target.closest('.veille-tag');
            if (!clickedBtn) return;
            const tag = clickedBtn.dataset.tag;
            veilleTags.forEach(b => b.classList.remove('active'));
            clickedBtn.classList.add('active');
            fetchArticles(tag);
        });
    });

    fetchArticles(currentTag);
});
