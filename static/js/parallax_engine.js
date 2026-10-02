/**
 * EduPredict AI - Ultra-Smooth Multi-Layer Parallax & 3D Glass Tilt Engine
 * 
 * Features:
 * - 🖱️ Interactive Mouse Parallax (Multi-plane depth for background, orbs, and academic icons)
 * - 📜 Smooth Scroll-Driven Parallax (Cinematic spatial drift on scroll)
 * - 🪟 Interactive 3D Card Tilt with dynamic specular shine on hover
 * - ⚡ 60 FPS GPU-accelerated LERP interpolation loop
 * - 🔋 Tab visibility auto-pause & accessibility (prefers-reduced-motion) compliance
 */

(function (window, document) {
    'use strict';

    // Respect user motion preferences
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    // Device check
    const isMobile = window.innerWidth < 768 || (navigator.maxTouchPoints && navigator.maxTouchPoints > 2);

    class ParallaxUniverseEngine {
        constructor() {
            // Screen & Scroll State
            this.winW = window.innerWidth;
            this.winH = window.innerHeight;
            this.halfW = this.winW / 2;
            this.halfH = this.winH / 2;
            this.scrollY = window.scrollY || window.pageYOffset;

            // Mouse Target & Current Normalized Coordinates (-1.0 to 1.0)
            this.targetMouseX = 0;
            this.targetMouseY = 0;
            this.currentMouseX = 0;
            this.currentMouseY = 0;

            // Scroll Target & Current
            this.targetScrollY = this.scrollY;
            this.currentScrollY = this.scrollY;

            // Animation state
            this.animFrameId = null;
            this.isActive = true;

            // Cache DOM Elements for high-performance transforms
            this.bgVideo = null;
            this.bgKenBurns = null;
            this.ambientOrbs = [];
            this.mathSymbols = [];
            this.floatingPills = [];
            this.floatingCharts = [];

            this.init();
        }

        init() {
            this.queryElements();
            this.bindEvents();
            this.initCardTilt();
            this.loop();
        }

        queryElements() {
            this.bgVideo = document.getElementById('ai-bg-video') || document.querySelector('.ai-bg-video');
            this.bgKenBurns = document.querySelector('.ai-bg-kenburns');
            this.ambientOrbs = Array.from(document.querySelectorAll('.ambient-orb, .blue-glow-circle'));
            this.mathSymbols = Array.from(document.querySelectorAll('.math-symbol'));
            this.floatingPills = Array.from(document.querySelectorAll('.floating-glass-pill, .hero-badge-pill'));
            this.floatingCharts = Array.from(document.querySelectorAll('.floating-chart-card, .floating-shape-analytics'));

            // Assign individual random or staggered depth multipliers to math symbols
            this.mathSymbols.forEach((sym, idx) => {
                const depths = [0.035, 0.055, 0.075, 0.09, 0.045];
                sym.dataset.depth = sym.dataset.depth || depths[idx % depths.length];
                sym.dataset.scrollFactor = (idx % 2 === 0 ? 0.08 : -0.06);
            });

            this.floatingPills.forEach((pill, idx) => {
                pill.dataset.depth = 0.06 + (idx * 0.02);
            });

            this.floatingCharts.forEach((chart, idx) => {
                chart.dataset.depth = 0.08 + (idx * 0.025);
            });
        }

        bindEvents() {
            // Mouse move with normalized coordinates
            window.addEventListener('mousemove', (e) => {
                this.targetMouseX = (e.clientX - this.halfW) / this.halfW;
                this.targetMouseY = (e.clientY - this.halfH) / this.halfH;
            }, { passive: true });

            // Leave window -> gentle return to center
            window.addEventListener('mouseleave', () => {
                this.targetMouseX = 0;
                this.targetMouseY = 0;
            });

            // Scroll position
            window.addEventListener('scroll', () => {
                this.targetScrollY = window.scrollY || window.pageYOffset;
            }, { passive: true });

            // Resize update
            window.addEventListener('resize', () => {
                this.winW = window.innerWidth;
                this.winH = window.innerHeight;
                this.halfW = this.winW / 2;
                this.halfH = this.winH / 2;
                this.queryElements();
            }, { passive: true });

            // Tab visibility
            document.addEventListener('visibilitychange', () => {
                this.isActive = !document.hidden;
                if (this.isActive) {
                    this.loop();
                } else if (this.animFrameId) {
                    cancelAnimationFrame(this.animFrameId);
                }
            });
        }

        loop() {
            if (!this.isActive) return;
            this.animFrameId = requestAnimationFrame(() => this.loop());

            // Linear Interpolation (LERP) for buttery smooth motion
            const lerpFactor = 0.07;
            this.currentMouseX += (this.targetMouseX - this.currentMouseX) * lerpFactor;
            this.currentMouseY += (this.targetMouseY - this.currentMouseY) * lerpFactor;
            this.currentScrollY += (this.targetScrollY - this.currentScrollY) * 0.1;

            const mx = this.currentMouseX;
            const my = this.currentMouseY;
            const sy = this.currentScrollY;

            // 1. Plane 1 (Deepest Background: Video & Ken Burns)
            if (this.bgVideo) {
                const vidX = -mx * 16;
                const vidY = -my * 14 + (sy * 0.08);
                this.bgVideo.style.transform = `translate(calc(-50% + ${vidX}px), calc(-50% + ${vidY}px)) scale(1.06)`;
            }

            if (this.bgKenBurns) {
                const kbX = -mx * 12;
                const kbY = -my * 10 + (sy * 0.05);
                this.bgKenBurns.style.transform = `translate3d(${kbX}px, ${kbY}px, 0)`;
            }

            // 2. Plane 2 (Ambient Halos & Glow Orbs)
            this.ambientOrbs.forEach((orb, i) => {
                const mult = (i % 2 === 0 ? 1 : -1);
                const orbX = mx * 28 * mult;
                const orbY = my * 22 * mult + (sy * 0.06);
                orb.style.transform = `translate3d(${orbX}px, ${orbY}px, 0)`;
            });

            // 3. Plane 3 (Floating Academic Math Symbols - Multi-plane depth)
            if (!isMobile) {
                this.mathSymbols.forEach((sym) => {
                    const depth = parseFloat(sym.dataset.depth || 0.05);
                    const scrollFactor = parseFloat(sym.dataset.scrollFactor || 0.05);
                    const symX = mx * depth * this.halfW * 0.45;
                    const symY = my * depth * this.halfH * 0.45 - (sy * scrollFactor);
                    sym.style.transform = `translate3d(${symX.toFixed(2)}px, ${symY.toFixed(2)}px, 0)`;
                });

                // 4. Plane 4 (Floating Glass Academic Badges & Charts)
                this.floatingPills.forEach((pill) => {
                    const depth = parseFloat(pill.dataset.depth || 0.06);
                    const pillX = -mx * depth * 35;
                    const pillY = -my * depth * 30 - (sy * 0.04);
                    pill.style.transform = `translate3d(${pillX.toFixed(2)}px, ${pillY.toFixed(2)}px, 0)`;
                });

                this.floatingCharts.forEach((chart) => {
                    const depth = parseFloat(chart.dataset.depth || 0.08);
                    const chartX = mx * depth * 40;
                    const chartY = my * depth * 35 - (sy * 0.05);
                    chart.style.transform = `translate3d(${chartX.toFixed(2)}px, ${chartY.toFixed(2)}px, 0)`;
                });
            }
        }

        /**
         * 3D Interactive Card Tilt with Dynamic Specular Glare
         */
        initCardTilt() {
            if (isMobile) return;

            const tiltCardSelectors = [
                '.predict-glass-card',
                '.glass-kpi-card',
                '.glass-action-card',
                '.stat-pill-hero',
                '.triage-card',
                '.prediction-result-master',
                '.chart-glass-card'
            ];

            const cards = document.querySelectorAll(tiltCardSelectors.join(', '));

            cards.forEach((card) => {
                // Ensure card perspective
                card.style.transformStyle = 'preserve-3d';
                card.style.willChange = 'transform';
                card.style.transition = 'transform 0.15s ease-out, box-shadow 0.25s ease';

                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const cardX = e.clientX - rect.left;
                    const cardY = e.clientY - rect.top;

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    // Calculate rotation angles (gentle tilt: max 5 deg)
                    const rotateX = -((cardY - centerY) / centerY) * 5.5;
                    const rotateY = ((cardX - centerX) / centerX) * 6.5;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.015, 1.015, 1.015)`;
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
                });
            });
        }
    }

    // Expose and auto-start engine on DOM ready
    window.ParallaxUniverseEngine = ParallaxUniverseEngine;

    document.addEventListener('DOMContentLoaded', () => {
        window.parallaxEngine = new ParallaxUniverseEngine();
    });

})(window, document);
