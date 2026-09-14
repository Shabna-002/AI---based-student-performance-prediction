/**
 * EduPredict AI - High-Performance AI Neural-Network Particles & Interactive Ambience
 * 
 * Features:
 * - 🤖 AI Neural-Network Particles with Synaptic Connections
 * - ⚡ Traveling Electrical Action Potential Pulses along synapses
 * - 🖱️ Interactive Mouse Attraction & Magnetic Constellation
 * - 🔋 Auto-throttling & zero battery drain when tab is inactive
 * - 📱 Retina/HiDPI display support with devicePixelRatio
 */

(function (window) {
    'use strict';

    class AINeuralNetworkCanvas {
        constructor(options = {}) {
            this.canvasId = options.canvasId || 'ai-neural-canvas';
            this.canvas = document.getElementById(this.canvasId);
            
            if (!this.canvas) {
                this.canvas = document.createElement('canvas');
                this.canvas.id = this.canvasId;
                document.body.prepend(this.canvas);
            }

            this.ctx = this.canvas.getContext('2d');
            this.width = 0;
            this.height = 0;
            this.dpr = Math.min(window.devicePixelRatio || 1, 2);

            // Configuration
            this.isMobile = window.innerWidth < 768;
            this.particleCount = options.particleCount || (this.isMobile ? 35 : 75);
            this.maxDistance = options.maxDistance || (this.isMobile ? 100 : 145);
            this.mouseRadius = 180;
            this.pulseFrequency = 0.035;

            // State
            this.particles = [];
            this.pulses = [];
            this.mouse = { x: -1000, y: -1000, isOver: false };
            this.animationFrameId = null;
            this.lastTime = performance.now();
            this.isActive = true;

            this.init();
        }

        init() {
            this.resize();
            this.createParticles();
            this.bindEvents();
            this.loop(performance.now());
        }

        resize() {
            this.width = window.innerWidth;
            this.height = window.innerHeight;
            this.canvas.width = this.width * this.dpr;
            this.canvas.height = this.height * this.dpr;
            this.ctx.scale(this.dpr, this.dpr);
        }

        createParticles() {
            this.particles = [];
            const colors = [
                { r: 56, g: 189, b: 248 },   // Electric Cyan
                { r: 99, g: 102, b: 241 },   // Indigo
                { r: 168, g: 85, b: 247 },   // Violet/Purple
                { r: 192, g: 132, b: 252 }   // Soft Orchid
            ];

            for (let i = 0; i < this.particleCount; i++) {
                const colorObj = colors[Math.floor(Math.random() * colors.length)];
                this.particles.push({
                    x: Math.random() * this.width,
                    y: Math.random() * this.height,
                    vx: (Math.random() - 0.5) * 0.75,
                    vy: (Math.random() - 0.5) * 0.75,
                    radius: Math.random() * 2.2 + 1.2,
                    baseAlpha: Math.random() * 0.45 + 0.35,
                    color: colorObj,
                    pulseOffset: Math.random() * Math.PI * 2
                });
            }
        }

        bindEvents() {
            window.addEventListener('resize', () => {
                this.resize();
            }, { passive: true });

            window.addEventListener('mousemove', (e) => {
                this.mouse.x = e.clientX;
                this.mouse.y = e.clientY;
                this.mouse.isOver = true;
            }, { passive: true });

            window.addEventListener('mouseleave', () => {
                this.mouse.isOver = false;
                this.mouse.x = -1000;
                this.mouse.y = -1000;
            });

            // Pause when tab hidden to save CPU/GPU
            document.addEventListener('visibilitychange', () => {
                this.isActive = !document.hidden;
                if (this.isActive) {
                    this.lastTime = performance.now();
                    this.loop(performance.now());
                } else if (this.animationFrameId) {
                    cancelAnimationFrame(this.animationFrameId);
                }
            });
        }

        spawnPulse(p1, p2) {
            this.pulses.push({
                x1: p1.x,
                y1: p1.y,
                x2: p2.x,
                y2: p2.y,
                progress: 0,
                speed: 0.02 + Math.random() * 0.02,
                color: Math.random() > 0.5 ? '#38bdf8' : '#c084fc'
            });
        }

        update(dt) {
            const time = performance.now() * 0.002;

            for (let i = 0; i < this.particles.length; i++) {
                const p = this.particles[i];

                // Position drift
                p.x += p.vx * (dt / 16);
                p.y += p.vy * (dt / 16);

                // Screen bounce
                if (p.x < 0) { p.x = 0; p.vx *= -1; }
                if (p.x > this.width) { p.x = this.width; p.vx *= -1; }
                if (p.y < 0) { p.y = 0; p.vy *= -1; }
                if (p.y > this.height) { p.y = this.height; p.vy *= -1; }

                // Mouse interaction / subtle attraction
                if (this.mouse.isOver) {
                    const dx = this.mouse.x - p.x;
                    const dy = this.mouse.y - p.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < this.mouseRadius && dist > 1) {
                        const force = (1 - dist / this.mouseRadius) * 0.35;
                        p.x += (dx / dist) * force;
                        p.y += (dy / dist) * force;
                    }
                }
            }

            // Update synaptic pulses
            for (let i = this.pulses.length - 1; i >= 0; i--) {
                const pulse = this.pulses[i];
                pulse.progress += pulse.speed;
                if (pulse.progress >= 1) {
                    this.pulses.splice(i, 1);
                }
            }
        }

        draw() {
            this.ctx.clearRect(0, 0, this.width, this.height);

            // 1. Draw Synaptic Connections (Neural network edges)
            for (let i = 0; i < this.particles.length; i++) {
                const p1 = this.particles[i];

                for (let j = i + 1; j < this.particles.length; j++) {
                    const p2 = this.particles[j];
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const distSq = dx * dx + dy * dy;
                    const maxDistSq = this.maxDistance * this.maxDistance;

                    if (distSq < maxDistSq) {
                        const dist = Math.sqrt(distSq);
                        const alpha = (1 - dist / this.maxDistance) * 0.38;

                        // Spawn occasional electrical action potential pulse
                        if (Math.random() < 0.0006 && this.pulses.length < 12) {
                            this.spawnPulse(p1, p2);
                        }

                        // Gradient line
                        const gradient = this.ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
                        gradient.addColorStop(0, `rgba(${p1.color.r}, ${p1.color.g}, ${p1.color.b}, ${alpha})`);
                        gradient.addColorStop(1, `rgba(${p2.color.r}, ${p2.color.g}, ${p2.color.b}, ${alpha * 0.7})`);

                        this.ctx.beginPath();
                        this.ctx.strokeStyle = gradient;
                        this.ctx.lineWidth = 1;
                        this.ctx.moveTo(p1.x, p1.y);
                        this.ctx.lineTo(p2.x, p2.y);
                        this.ctx.stroke();
                    }
                }

                // Connect to mouse cursor
                if (this.mouse.isOver) {
                    const mdx = p1.x - this.mouse.x;
                    const mdy = p1.y - this.mouse.y;
                    const mDist = Math.sqrt(mdx * mdx + mdy * mdy);

                    if (mDist < this.mouseRadius) {
                        const mAlpha = (1 - mDist / this.mouseRadius) * 0.55;
                        this.ctx.beginPath();
                        this.ctx.strokeStyle = `rgba(56, 189, 248, ${mAlpha})`;
                        this.ctx.lineWidth = 1.2;
                        this.ctx.moveTo(p1.x, p1.y);
                        this.ctx.lineTo(this.mouse.x, this.mouse.y);
                        this.ctx.stroke();
                    }
                }
            }

            // 2. Draw Traveling Synapse Pulses
            for (let i = 0; i < this.pulses.length; i++) {
                const p = this.pulses[i];
                const curX = p.x1 + (p.x2 - p.x1) * p.progress;
                const curY = p.y1 + (p.y2 - p.y1) * p.progress;

                this.ctx.beginPath();
                this.ctx.arc(curX, curY, 2.5, 0, Math.PI * 2);
                this.ctx.fillStyle = p.color;
                this.ctx.shadowColor = p.color;
                this.ctx.shadowBlur = 8;
                this.ctx.fill();
                this.ctx.shadowBlur = 0; // Reset
            }

            // 3. Draw Neural Nodes (Particles)
            const time = performance.now() * 0.003;
            for (let i = 0; i < this.particles.length; i++) {
                const p = this.particles[i];
                const pulsingAlpha = p.baseAlpha + Math.sin(time + p.pulseOffset) * 0.15;

                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${pulsingAlpha})`;
                this.ctx.shadowColor = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, 0.8)`;
                this.ctx.shadowBlur = 10;
                this.ctx.fill();
                this.ctx.shadowBlur = 0; // Reset
            }
        }

        loop(currentTime) {
            if (!this.isActive) return;

            const dt = Math.min(currentTime - this.lastTime, 64);
            this.lastTime = currentTime;

            this.update(dt);
            this.draw();

            this.animationFrameId = requestAnimationFrame((t) => this.loop(t));
        }

        destroy() {
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
            }
            if (this.canvas && this.canvas.parentNode) {
                this.canvas.parentNode.removeChild(this.canvas);
            }
        }
    }

    // Global initializer
    window.initAiAmbientEffects = function (options) {
        if (!window.aiNeuralCanvasInstance) {
            window.aiNeuralCanvasInstance = new AINeuralNetworkCanvas(options);
        }
        return window.aiNeuralCanvasInstance;
    };

})(window);
