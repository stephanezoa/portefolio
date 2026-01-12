// TRUEFOCUS ANIMATION (JS version of React component)
class TrueFocus {
    constructor({
        sentence = 'True Focus',
        separator = ' ',
        manualMode = false,
        blurAmount = 5,
        borderColor = 'red',
        glowColor = 'rgba(255, 0, 0, 0.6)',
        animationDuration = 2,
        pauseBetweenAnimations = 1
    }) {
        this.sentence = sentence;
        this.separator = separator;
        this.manualMode = manualMode;
        this.blurAmount = blurAmount;
        this.borderColor = borderColor;
        this.glowColor = glowColor;
        this.animationDuration = animationDuration;
        this.pauseBetweenAnimations = pauseBetweenAnimations;

        this.words = sentence.split(separator);
        this.currentIndex = 0;
        this.lastActiveIndex = null;
        this.containerRef = document.getElementById('true-focus-container');
        this.wordRefs = [];
        this.focusRect = { x: 0, y: 0, width: 0, height: 0 };

        this.init();
    }

    init() {
        this.render();
        if (!this.manualMode) {
            this.startAutoCycle();
        }
    }

    render() {
        this.containerRef.innerHTML = '';
        this.words.forEach((word, index) => {
            const span = document.createElement('span');
            span.textContent = word;
            span.className = 'relative text-[2rem] md:text-[3rem] font-black cursor-pointer';
            span.style.filter = index === this.currentIndex ? 'blur(0px)' : `blur(${this.blurAmount}px)`;
            span.style.transition = `filter ${this.animationDuration}s ease`;
            span.style.outline = 'none';
            span.style.userSelect = 'none';
            span.style['--border-color'] = this.borderColor;
            span.style['--glow-color'] = this.glowColor;

            span.addEventListener('mouseenter', () => this.handleMouseEnter(index));
            span.addEventListener('mouseleave', () => this.handleMouseLeave());

            this.wordRefs[index] = span;
            this.containerRef.appendChild(span);
        });

        this.addFocusOverlay();
    }

    addFocusOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'absolute top-0 left-0 pointer-events-none box-border border-0';
        overlay.id = 'focus-overlay';

        const corners = [
            { className: 'top-[-10px] left-[-10px] border-r-0 border-b-0' },
            { className: 'top-[-10px] right-[-10px] border-l-0 border-b-0' },
            { className: 'bottom-[-10px] left-[-10px] border-r-0 border-t-0' },
            { className: 'bottom-[-10px] right-[-10px] border-l-0 border-t-0' }
        ];

        corners.forEach(corner => {
            const cornerEl = document.createElement('span');
            cornerEl.className = `absolute w-4 h-4 border-[3px] rounded-[3px] ${corner.className}`;
            cornerEl.style.borderColor = 'var(--border-color)';
            cornerEl.style.filter = 'drop-shadow(0 0 4px var(--border-color))';
            overlay.appendChild(cornerEl);
        });

        this.containerRef.appendChild(overlay);
        this.overlay = overlay;
    }

    startAutoCycle() {
        this.intervalId = setInterval(() => {
            this.currentIndex = (this.currentIndex + 1) % this.words.length;
            this.updateFocus();
        }, (this.animationDuration + this.pauseBetweenAnimations) * 1000);
    }

    updateFocus() {
        if (this.currentIndex === null || this.currentIndex === -1) return;
        if (!this.wordRefs[this.currentIndex] || !this.containerRef) return;

        const parentRect = this.containerRef.getBoundingClientRect();
        const activeRect = this.wordRefs[this.currentIndex].getBoundingClientRect();

        this.focusRect = {
            x: activeRect.left - parentRect.left,
            y: activeRect.top - parentRect.top,
            width: activeRect.width,
            height: activeRect.height
        };

        this.animateOverlay();
    }

    animateOverlay() {
        const overlay = this.overlay;
        if (!overlay) return;

        overlay.style.transform = `translate(${this.focusRect.x}px, ${this.focusRect.y}px)`;
        overlay.style.width = `${this.focusRect.width}px`;
        overlay.style.height = `${this.focusRect.height}px`;
        overlay.style.opacity = this.currentIndex >= 0 ? 1 : 0;

        // Animate using CSS transitions
        overlay.style.transition = `transform ${this.animationDuration}s ease, width ${this.animationDuration}s ease, height ${this.animationDuration}s ease, opacity ${this.animationDuration}s ease`;
    }

    handleMouseEnter(index) {
        if (this.manualMode) {
            this.lastActiveIndex = index;
            this.currentIndex = index;
            this.updateFocus();
        }
    }

    handleMouseLeave() {
        if (this.manualMode && this.lastActiveIndex !== null) {
            this.currentIndex = this.lastActiveIndex;
            this.updateFocus();
        }
    }

    destroy() {
        if (this.intervalId) clearInterval(this.intervalId);
    }
}

// GRADIENT TEXT ANIMATION
class GradientText {
    constructor({
        element,
        colors = ['#5227FF', '#FF9FFC', '#B19EEF'],
        animationSpeed = 8,
        showBorder = false,
        direction = 'horizontal',
        pauseOnHover = false,
        yoyo = true
    }) {
        this.element = element;
        this.colors = colors;
        this.animationSpeed = animationSpeed;
        this.showBorder = showBorder;
        this.direction = direction;
        this.pauseOnHover = pauseOnHover;
        this.yoyo = yoyo;

        this.isPaused = false;
        this.elapsed = 0;
        this.lastTime = null;
        this.progress = 0;

        this.init();
    }

    init() {
        this.element.classList.add('relative', 'inline-block', 'text-transparent', 'bg-clip-text');

        const gradientAngle =
            this.direction === 'horizontal' ? 'to right' :
            this.direction === 'vertical' ? 'to bottom' : 'to bottom right';

        const gradientColors = [...this.colors, this.colors[0]].join(', ');

        this.element.style.backgroundImage = `linear-gradient(${gradientAngle}, ${gradientColors})`;
        this.element.style.backgroundSize = this.direction === 'horizontal' ? '300% 100%' : '100% 300%';
        this.element.style.backgroundRepeat = 'repeat';
        this.element.style.webkitBackgroundClip = 'text';

        if (this.showBorder) {
            const borderDiv = document.createElement('div');
            borderDiv.className = 'absolute inset-0 z-0 pointer-events-none rounded-[1.25rem]';
            borderDiv.style.backgroundImage = `linear-gradient(${gradientAngle}, ${gradientColors})`;
            borderDiv.style.backgroundSize = this.direction === 'horizontal' ? '300% 100%' : '100% 300%';
            borderDiv.style.backgroundRepeat = 'repeat';
            this.element.parentNode.insertBefore(borderDiv, this.element);

            const innerBg = document.createElement('div');
            innerBg.className = 'absolute bg-black rounded-[1.25rem] z-[-1]';
            innerBg.style.width = 'calc(100% - 2px)';
            innerBg.style.height = 'calc(100% - 2px)';
            innerBg.style.left = '50%';
            innerBg.style.top = '50%';
            innerBg.style.transform = 'translate(-50%, -50%)';
            borderDiv.appendChild(innerBg);
        }

        if (this.pauseOnHover) {
            this.element.addEventListener('mouseenter', () => this.isPaused = true);
            this.element.addEventListener('mouseleave', () => this.isPaused = false);
        }

        this.startAnimation();
    }

    startAnimation() {
        const animate = (time) => {
            if (this.isPaused) {
                this.lastTime = null;
                requestAnimationFrame(animate);
                return;
            }

            if (this.lastTime === null) {
                this.lastTime = time;
                requestAnimationFrame(animate);
                return;
            }

            const deltaTime = time - this.lastTime;
            this.lastTime = time;
            this.elapsed += deltaTime;

            const animationDuration = this.animationSpeed * 1000;

            if (this.yoyo) {
                const fullCycle = animationDuration * 2;
                const cycleTime = this.elapsed % fullCycle;

                if (cycleTime < animationDuration) {
                    this.progress = (cycleTime / animationDuration) * 100;
                } else {
                    this.progress = 100 - ((cycleTime - animationDuration) / animationDuration) * 100;
                }
            } else {
                this.progress = (this.elapsed / animationDuration) * 100;
            }

            const backgroundPosition =
                this.direction === 'horizontal' ? `${this.progress}% 50%` :
                this.direction === 'vertical' ? `50% ${this.progress}%` : `${this.progress}% 50%`;

            this.element.style.backgroundPosition = backgroundPosition;

            requestAnimationFrame(animate);
        };

        requestAnimationFrame(animate);
    }
}

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', () => {
    // TrueFocus on homepage
    if (document.getElementById('true-focus-container')) {
        new TrueFocus({
            sentence: "Back End Developer | Scalable Systems | Clean Code",
            manualMode: false,
            blurAmount: 3,
            borderColor: '#00ffaa',
            glowColor: 'rgba(0, 255, 170, 0.6)',
            animationDuration: 2,
            pauseBetweenAnimations: 1
        });
    }

    // Gradient Text on homepage title
    if (document.getElementById('gradient-title')) {
        new GradientText({
            element: document.getElementById('gradient-title'),
            colors: ["#40ffaa", "#4079ff", "#40ffaa", "#4079ff", "#40ffaa"],
            animationSpeed: 3,
            showBorder: false,
            direction: 'horizontal',
            pauseOnHover: false,
            yoyo: true
        });
    }
});