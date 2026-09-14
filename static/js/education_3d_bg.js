/**
 * EduPredict AI - Interactive 3D Education Background Engine
 * Pure Three.js procedural 3D academic animation:
 * - 3D Graduation Mortarboard Caps (with gold tassels)
 * - 3D Hardcover & Open Books (with formulas & bookmark ribbons)
 * - 3D Rolled Diplomas / Scrolls
 * - 3D Atomic Knowledge Orbits
 * - 3D Floating Academic Glyphs (A+, ∑, π, 🎓, 📚, 100%, AI, f(x))
 * - 3D Neural Knowledge Network / Constellation
 * - Responsive 60fps WebGL with smooth mouse parallax
 */

(function (window) {
    'use strict';

    class Education3DBackground {
        constructor(options = {}) {
            this.container = typeof options.container === 'string' 
                ? document.getElementById(options.container) 
                : (options.container || document.body);
            
            this.theme = options.theme || 'cyberBlue';
            this.subtleMode = options.subtle || false;
            this.speed = options.speed || 1.0;
            this.enableMouse = options.enableMouse !== false;
            this.interactiveOrbit = options.interactiveOrbit || false;

            this.scene = null;
            this.camera = null;
            this.renderer = null;
            this.clock = null;
            this.animationFrameId = null;

            // Interactive state
            this.mouseX = 0;
            this.mouseY = 0;
            this.targetMouseX = 0;
            this.targetMouseY = 0;
            this.windowHalfX = window.innerWidth / 2;
            this.windowHalfY = window.innerHeight / 2;

            // 3D Object collections
            this.floatingObjects = [];
            this.constellationNodes = [];
            this.constellationLines = null;
            this.particleGroup = null;
            this.glyphSprites = [];
            this.atomicRings = [];

            // Color Palettes
            this.palettes = {
                cyberBlue: {
                    bgTop: 0x070d1d,
                    bgBottom: 0x030712,
                    primary: 0x3b82f6,
                    accent: 0x60a5fa,
                    secondary: 0x8b5cf6,
                    gold: 0xf59e0b,
                    bookCover1: 0x1e3a8a,
                    bookCover2: 0x4338ca,
                    capColor: 0x0f172a,
                    particleColor: 0x38bdf8
                },
                academicGold: {
                    bgTop: 0x0a101f,
                    bgBottom: 0x020617,
                    primary: 0x2563eb,
                    accent: 0xf59e0b,
                    secondary: 0xd97706,
                    gold: 0xfbbf24,
                    bookCover1: 0x1e293b,
                    bookCover2: 0x78350f,
                    capColor: 0x090d16,
                    particleColor: 0xfcd34d
                },
                emeraldScholar: {
                    bgTop: 0x041d14,
                    bgBottom: 0x02100b,
                    primary: 0x10b981,
                    accent: 0x34d399,
                    secondary: 0x06b6d4,
                    gold: 0xf59e0b,
                    bookCover1: 0x064e3b,
                    bookCover2: 0x134e4a,
                    capColor: 0x022c22,
                    particleColor: 0x6ee7b7
                },
                midnight: {
                    bgTop: 0x090a0f,
                    bgBottom: 0x020305,
                    primary: 0x6366f1,
                    accent: 0xec4899,
                    secondary: 0x8b5cf6,
                    gold: 0xfacc15,
                    bookCover1: 0x312e81,
                    bookCover2: 0x581c87,
                    capColor: 0x030712,
                    particleColor: 0xc084fc
                }
            };

            this.currentPalette = this.palettes[this.theme] || this.palettes.cyberBlue;

            this.init();
        }

        init() {
            if (!window.THREE) {
                console.error("Three.js must be loaded before Education3DBackground.");
                return;
            }

            const width = this.container.clientWidth || window.innerWidth;
            const height = this.container.clientHeight || window.innerHeight;

            // 1. Scene Setup
            this.scene = new THREE.Scene();
            this.scene.fog = new THREE.FogExp2(this.currentPalette.bgBottom, this.subtleMode ? 0.025 : 0.018);

            // 2. Camera Setup
            this.camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
            this.camera.position.set(0, 0, 32);

            // 3. Renderer Setup
            this.renderer = new THREE.WebGLRenderer({
                alpha: true,
                antialias: true,
                powerPreference: "high-performance"
            });
            this.renderer.setSize(width, height);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            this.renderer.outputEncoding = THREE.sRGBEncoding;

            // Make sure canvas fits background
            this.renderer.domElement.style.position = 'absolute';
            this.renderer.domElement.style.top = '0';
            this.renderer.domElement.style.left = '0';
            this.renderer.domElement.style.width = '100%';
            this.renderer.domElement.style.height = '100%';
            this.renderer.domElement.style.pointerEvents = this.interactiveOrbit ? 'auto' : 'none';
            this.renderer.domElement.style.zIndex = '0';
            this.container.appendChild(this.renderer.domElement);

            this.clock = new THREE.Clock();

            // 4. Lighting
            this.setupLights();

            // 5. Build Academic 3D Elements
            this.buildGraduationCaps();
            this.buildBooks();
            this.buildDiplomas();
            this.buildAtomicKnowledgeRings();
            this.buildFloatingGlyphs();
            this.buildKnowledgeConstellation();

            // 6. Event Listeners
            this.onWindowResize = this.onWindowResize.bind(this);
            this.onMouseMove = this.onMouseMove.bind(this);
            this.onTouchMove = this.onTouchMove.bind(this);

            window.addEventListener('resize', this.onWindowResize, false);
            if (this.enableMouse) {
                window.addEventListener('mousemove', this.onMouseMove, false);
                window.addEventListener('touchmove', this.onTouchMove, { passive: true });
            }

            // 7. Start Animation Loop
            this.animate = this.animate.bind(this);
            this.animate();
        }

        setupLights() {
            // Ambient light
            const ambient = new THREE.AmbientLight(0xffffff, this.subtleMode ? 0.7 : 0.9);
            this.scene.add(ambient);

            // Key light (Primary cyan/blue)
            const keyLight = new THREE.DirectionalLight(this.currentPalette.primary, 1.2);
            keyLight.position.set(20, 25, 20);
            this.scene.add(keyLight);

            // Fill light (Purple/accent)
            const fillLight = new THREE.DirectionalLight(this.currentPalette.secondary, 0.8);
            fillLight.position.set(-20, -15, 15);
            this.scene.add(fillLight);

            // Warm golden rim light (Academic excellence glow)
            const rimLight = new THREE.PointLight(this.currentPalette.gold, 1.4, 60);
            rimLight.position.set(0, 15, -10);
            this.scene.add(rimLight);
            this.rimLight = rimLight;
        }

        /**
         * Procedural 3D Graduation Mortarboard Cap
         */
        createGraduationCap(scale = 1.0) {
            const capGroup = new THREE.Group();

            const capMat = new THREE.MeshStandardMaterial({
                color: this.currentPalette.capColor,
                roughness: 0.35,
                metalness: 0.25,
                flatShading: false
            });

            // 1. Mortarboard Diamond Top
            const topGeo = new THREE.BoxGeometry(2.4, 0.08, 2.4);
            const topMesh = new THREE.Mesh(topGeo, capMat);
            topMesh.rotation.y = Math.PI / 4;
            capGroup.add(topMesh);

            // 2. Skull Cap Base (underneath)
            const baseGeo = new THREE.CylinderGeometry(0.75, 0.85, 0.65, 24);
            const baseMesh = new THREE.Mesh(baseGeo, capMat);
            baseMesh.position.y = -0.36;
            capGroup.add(baseMesh);

            // 3. Golden Center Button
            const goldMat = new THREE.MeshStandardMaterial({
                color: this.currentPalette.gold,
                roughness: 0.2,
                metalness: 0.9,
                emissive: 0x78350f,
                emissiveIntensity: 0.3
            });
            const btnGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.08, 16);
            const btnMesh = new THREE.Mesh(btnGeo, goldMat);
            btnMesh.position.y = 0.06;
            capGroup.add(btnMesh);

            // 4. Golden Tassel Cord & Hanging Fringe
            const cordCurve = new THREE.CatmullRomCurve3([
                new THREE.Vector3(0, 0.06, 0),
                new THREE.Vector3(0.6, 0.05, 0.6),
                new THREE.Vector3(1.35, -0.02, 1.35),
                new THREE.Vector3(1.45, -0.6, 1.45)
            ]);
            const cordGeo = new THREE.TubeGeometry(cordCurve, 16, 0.025, 8, false);
            const cordMesh = new THREE.Mesh(cordGeo, goldMat);
            capGroup.add(cordMesh);

            // Tassel fringe brush
            const tasselGeo = new THREE.ConeGeometry(0.12, 0.5, 16);
            const tasselMesh = new THREE.Mesh(tasselGeo, goldMat);
            tasselMesh.position.set(1.45, -0.85, 1.45);
            tasselMesh.rotation.x = Math.PI;
            capGroup.add(tasselMesh);

            // Scale & Shadow
            capGroup.scale.set(scale, scale, scale);
            return capGroup;
        }

        buildGraduationCaps() {
            const count = this.subtleMode ? 4 : 8;
            const positions = [
                { x: -14, y: 7, z: -5, rotSpeed: 0.004, bobSpeed: 1.2, scale: 1.5 },
                { x: 13, y: 8, z: -8, rotSpeed: -0.005, bobSpeed: 1.5, scale: 1.6 },
                { x: -12, y: -8, z: -4, rotSpeed: 0.006, bobSpeed: 1.1, scale: 1.3 },
                { x: 15, y: -7, z: -6, rotSpeed: -0.004, bobSpeed: 1.4, scale: 1.4 },
                { x: 6, y: 11, z: -14, rotSpeed: 0.005, bobSpeed: 0.9, scale: 1.1 },
                { x: -7, y: 12, z: -16, rotSpeed: -0.003, bobSpeed: 1.3, scale: 1.0 },
                { x: 0, y: -12, z: -10, rotSpeed: 0.005, bobSpeed: 1.6, scale: 1.2 },
                { x: 18, y: 1, z: -12, rotSpeed: -0.006, bobSpeed: 1.0, scale: 1.2 }
            ];

            for (let i = 0; i < count; i++) {
                const config = positions[i % positions.length];
                const cap = this.createGraduationCap(config.scale);
                cap.position.set(config.x, config.y, config.z);
                cap.rotation.set(
                    (Math.random() - 0.5) * 0.6,
                    Math.random() * Math.PI * 2,
                    (Math.random() - 0.5) * 0.4
                );

                this.scene.add(cap);
                this.floatingObjects.push({
                    mesh: cap,
                    baseY: config.y,
                    bobSpeed: config.bobSpeed,
                    bobOffset: i * 1.4,
                    rotSpeedX: config.rotSpeed * 0.5,
                    rotSpeedY: config.rotSpeed,
                    rotSpeedZ: config.rotSpeed * 0.3
                });
            }
        }

        /**
         * Procedural 3D Academic Hardcover Book with textured pages & formulas
         */
        createBook(isOpen = false, coverColor = null, scale = 1.0) {
            const bookGroup = new THREE.Group();
            const color = coverColor || this.currentPalette.bookCover1;

            const coverMat = new THREE.MeshStandardMaterial({
                color: color,
                roughness: 0.4,
                metalness: 0.2
            });

            const pageMat = new THREE.MeshStandardMaterial({
                color: 0xfbfbf8,
                roughness: 0.8,
                metalness: 0.05
            });

            const goldBookmarkMat = new THREE.MeshStandardMaterial({
                color: this.currentPalette.gold,
                roughness: 0.3,
                metalness: 0.85
            });

            if (!isOpen) {
                // Closed Hardcover Textbook
                const width = 1.8;
                const height = 2.4;
                const thickness = 0.45;

                // Cover top & bottom
                const coverT = 0.04;
                const topCover = new THREE.Mesh(new THREE.BoxGeometry(width, coverT, height), coverMat);
                topCover.position.y = thickness / 2;
                bookGroup.add(topCover);

                const btmCover = new THREE.Mesh(new THREE.BoxGeometry(width, coverT, height), coverMat);
                btmCover.position.y = -thickness / 2;
                bookGroup.add(btmCover);

                // Spine
                const spine = new THREE.Mesh(new THREE.BoxGeometry(coverT, thickness + coverT, height), coverMat);
                spine.position.x = -width / 2;
                bookGroup.add(spine);

                // Embossed gold band on spine
                const spineGold = new THREE.Mesh(new THREE.BoxGeometry(coverT * 1.1, 0.08, height * 0.8), goldBookmarkMat);
                spineGold.position.x = -width / 2 - 0.01;
                bookGroup.add(spineGold);

                // Pages Block
                const pages = new THREE.Mesh(new THREE.BoxGeometry(width - 0.1, thickness - coverT * 2, height - 0.1), pageMat);
                pages.position.x = 0.04;
                bookGroup.add(pages);

                // Ribbon bookmark peeking out
                const ribbon = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.02, 0.6), goldBookmarkMat);
                ribbon.position.set(0.3, 0, height / 2 + 0.2);
                ribbon.rotation.x = 0.2;
                bookGroup.add(ribbon);

            } else {
                // Open Textbook with angled wings & formulas
                const pageW = 1.3;
                const pageH = 1.9;
                const pageD = 0.06;
                const openAngle = 0.32; // Slight V-shape

                // Left wing
                const leftWing = new THREE.Group();
                const leftCover = new THREE.Mesh(new THREE.BoxGeometry(pageW, 0.03, pageH), coverMat);
                leftCover.position.x = -pageW / 2;
                leftWing.add(leftCover);

                const leftPages = new THREE.Mesh(new THREE.BoxGeometry(pageW * 0.95, pageD, pageH * 0.95), pageMat);
                leftPages.position.set(-pageW / 2, pageD / 2, 0);
                leftWing.add(leftPages);

                leftWing.rotation.z = openAngle;
                bookGroup.add(leftWing);

                // Right wing
                const rightWing = new THREE.Group();
                const rightCover = new THREE.Mesh(new THREE.BoxGeometry(pageW, 0.03, pageH), coverMat);
                rightCover.position.x = pageW / 2;
                rightWing.add(rightCover);

                const rightPages = new THREE.Mesh(new THREE.BoxGeometry(pageW * 0.95, pageD, pageH * 0.95), pageMat);
                rightPages.position.set(pageW / 2, pageD / 2, 0);
                rightWing.add(rightPages);

                rightWing.rotation.z = -openAngle;
                bookGroup.add(rightWing);

                // Spine Center
                const spine = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, pageH, 12), coverMat);
                spine.rotation.x = Math.PI / 2;
                spine.position.y = -0.05;
                bookGroup.add(spine);
            }

            bookGroup.scale.set(scale, scale, scale);
            return bookGroup;
        }

        buildBooks() {
            const count = this.subtleMode ? 3 : 6;
            const bookConfigs = [
                { x: -15, y: 1, z: -7, isOpen: true, color: this.currentPalette.bookCover1, scale: 1.4, rotSpeed: 0.005 },
                { x: 16, y: -2, z: -9, isOpen: false, color: this.currentPalette.bookCover2, scale: 1.5, rotSpeed: -0.006 },
                { x: -8, y: -11, z: -8, isOpen: false, color: this.currentPalette.primary, scale: 1.3, rotSpeed: 0.004 },
                { x: 10, y: 10, z: -12, isOpen: true, color: this.currentPalette.secondary, scale: 1.2, rotSpeed: -0.005 },
                { x: -17, y: -5, z: -15, isOpen: false, color: this.currentPalette.bookCover1, scale: 1.1, rotSpeed: 0.003 },
                { x: 7, y: -13, z: -11, isOpen: true, color: this.currentPalette.bookCover2, scale: 1.2, rotSpeed: -0.004 }
            ];

            for (let i = 0; i < count; i++) {
                const cfg = bookConfigs[i % bookConfigs.length];
                const book = this.createBook(cfg.isOpen, cfg.color, cfg.scale);
                book.position.set(cfg.x, cfg.y, cfg.z);
                book.rotation.set(
                    (Math.random() - 0.5) * 0.8,
                    Math.random() * Math.PI * 2,
                    (Math.random() - 0.5) * 0.6
                );

                this.scene.add(book);
                this.floatingObjects.push({
                    mesh: book,
                    baseY: cfg.y,
                    bobSpeed: 1.1 + (i % 3) * 0.3,
                    bobOffset: i * 2.1,
                    rotSpeedX: cfg.rotSpeed * 0.6,
                    rotSpeedY: cfg.rotSpeed,
                    rotSpeedZ: cfg.rotSpeed * 0.4
                });
            }
        }

        /**
         * Procedural 3D Rolled Diploma / Graduation Scroll
         */
        createDiploma(scale = 1.0) {
            const diplomaGroup = new THREE.Group();

            // Parchment scroll cylinder
            const parchmentMat = new THREE.MeshStandardMaterial({
                color: 0xfffcf0,
                roughness: 0.7,
                metalness: 0.05
            });
            const scrollGeo = new THREE.CylinderGeometry(0.24, 0.24, 2.2, 24);
            const scrollMesh = new THREE.Mesh(scrollGeo, parchmentMat);
            diplomaGroup.add(scrollMesh);

            // Silk ribbon band in the middle
            const ribbonMat = new THREE.MeshStandardMaterial({
                color: this.currentPalette.gold,
                roughness: 0.25,
                metalness: 0.8,
                emissive: 0xb45309,
                emissiveIntensity: 0.3
            });
            const ribbonGeo = new THREE.CylinderGeometry(0.26, 0.26, 0.28, 24);
            const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
            diplomaGroup.add(ribbonMesh);

            // Hanging ribbon tail tails
            const tailGeo = new THREE.BoxGeometry(0.08, 0.7, 0.02);
            const tail1 = new THREE.Mesh(tailGeo, ribbonMat);
            tail1.position.set(0.26, -0.3, 0);
            tail1.rotation.z = -0.2;
            diplomaGroup.add(tail1);

            const tail2 = new THREE.Mesh(tailGeo, ribbonMat);
            tail2.position.set(0.28, -0.28, 0.05);
            tail2.rotation.z = 0.2;
            diplomaGroup.add(tail2);

            diplomaGroup.scale.set(scale, scale, scale);
            return diplomaGroup;
        }

        buildDiplomas() {
            const count = this.subtleMode ? 2 : 4;
            const diplomaConfigs = [
                { x: 12, y: 3, z: -6, scale: 1.3, rotSpeed: 0.007 },
                { x: -10, y: 8, z: -10, scale: 1.2, rotSpeed: -0.005 },
                { x: -5, y: -10, z: -13, scale: 1.1, rotSpeed: 0.006 },
                { x: 17, y: -9, z: -12, scale: 1.0, rotSpeed: -0.006 }
            ];

            for (let i = 0; i < count; i++) {
                const cfg = diplomaConfigs[i];
                const diploma = this.createDiploma(cfg.scale);
                diploma.position.set(cfg.x, cfg.y, cfg.z);
                diploma.rotation.set(0.6, Math.random() * Math.PI, 0.8);

                this.scene.add(diploma);
                this.floatingObjects.push({
                    mesh: diploma,
                    baseY: cfg.y,
                    bobSpeed: 1.3 + i * 0.4,
                    bobOffset: i * 1.8 + 0.5,
                    rotSpeedX: cfg.rotSpeed * 0.5,
                    rotSpeedY: cfg.rotSpeed,
                    rotSpeedZ: cfg.rotSpeed * 0.7
                });
            }
        }

        /**
         * Procedural 3D Atomic Knowledge Orbits
         */
        buildAtomicKnowledgeRings() {
            const orbitGroup = new THREE.Group();
            orbitGroup.position.set(11, -6, -15);

            // Glowing nucleus (Core intelligence sphere)
            const nucleusGeo = new THREE.SphereGeometry(0.7, 24, 24);
            const nucleusMat = new THREE.MeshStandardMaterial({
                color: this.currentPalette.primary,
                roughness: 0.2,
                metalness: 0.8,
                emissive: this.currentPalette.primary,
                emissiveIntensity: 0.6
            });
            const nucleus = new THREE.Mesh(nucleusGeo, nucleusMat);
            orbitGroup.add(nucleus);

            // 3 Gyroscopic Orbit Rings
            const ringMat = new THREE.MeshBasicMaterial({
                color: this.currentPalette.accent,
                wireframe: false,
                transparent: true,
                opacity: 0.6
            });

            const ring1 = new THREE.Mesh(new THREE.TorusGeometry(2.4, 0.03, 16, 64), ringMat);
            const ring2 = new THREE.Mesh(new THREE.TorusGeometry(2.4, 0.03, 16, 64), ringMat);
            const ring3 = new THREE.Mesh(new THREE.TorusGeometry(2.4, 0.03, 16, 64), ringMat);

            ring1.rotation.x = Math.PI / 3;
            ring2.rotation.y = Math.PI / 3;
            ring3.rotation.z = Math.PI / 3;

            orbitGroup.add(ring1);
            orbitGroup.add(ring2);
            orbitGroup.add(ring3);

            this.scene.add(orbitGroup);
            this.atomicRings = [ring1, ring2, ring3];
            this.atomicCore = nucleus;
            this.atomicGroup = orbitGroup;
        }

        /**
         * Floating 3D Educational Glyphs (A+, 🎓, 📚, ∑, π, f(x), 100%, AI, 🧠)
         */
        createGlyphTexture(symbol, subtext = '', glowColor = '#38bdf8') {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');

            // Soft radial glow circle
            const grad = ctx.createRadialGradient(128, 128, 20, 128, 128, 120);
            grad.addColorStop(0, 'rgba(15, 23, 42, 0.9)');
            grad.addColorStop(0.7, 'rgba(15, 23, 42, 0.6)');
            grad.addColorStop(1, 'rgba(15, 23, 42, 0)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(128, 128, 110, 0, Math.PI * 2);
            ctx.fill();

            // Glowing border ring
            ctx.strokeStyle = glowColor;
            ctx.lineWidth = 4;
            ctx.shadowColor = glowColor;
            ctx.shadowBlur = 18;
            ctx.beginPath();
            ctx.arc(128, 128, 90, 0, Math.PI * 2);
            ctx.stroke();

            // Main Symbol Text
            ctx.shadowBlur = 12;
            ctx.shadowColor = '#ffffff';
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 74px "Inter", "Segoe UI", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(symbol, 128, subtext ? 116 : 128);

            // Subtext (e.g. "GRADE", "AI", "MATH")
            if (subtext) {
                ctx.shadowBlur = 6;
                ctx.fillStyle = glowColor;
                ctx.font = 'bold 22px "Inter", "Segoe UI", sans-serif';
                ctx.letterSpacing = '2px';
                ctx.fillText(subtext, 128, 168);
            }

            const texture = new THREE.CanvasTexture(canvas);
            texture.needsUpdate = true;
            return texture;
        }

        buildFloatingGlyphs() {
            const glyphData = [
                { symbol: 'A+', sub: 'GRADE', color: '#fbbf24', x: -11, y: 5, z: 2, scale: 2.6 },
                { symbol: '🎓', sub: 'HONORS', color: '#60a5fa', x: 10, y: 6, z: 1, scale: 2.8 },
                { symbol: '∑', sub: 'CALCULUS', color: '#c084fc', x: -12, y: -4, z: -1, scale: 2.4 },
                { symbol: 'AI', sub: 'PREDICT', color: '#38bdf8', x: 11, y: -5, z: 0, scale: 2.6 },
                { symbol: '100%', sub: 'ACCURACY', color: '#34d399', x: 0, y: 10, z: -4, scale: 2.5 },
                { symbol: 'π', sub: 'DATA', color: '#f472b6', x: -6, y: -9, z: -3, scale: 2.2 },
                { symbol: 'f(x)', sub: 'MODEL', color: '#a78bfa', x: 7, y: -10, z: -2, scale: 2.4 },
                { symbol: '📚', sub: 'STUDY', color: '#fb923c', x: -16, y: 10, z: -6, scale: 2.5 }
            ];

            const count = this.subtleMode ? 4 : glyphData.length;

            for (let i = 0; i < count; i++) {
                const item = glyphData[i];
                const texture = this.createGlyphTexture(item.symbol, item.sub, item.color);
                const spriteMat = new THREE.SpriteMaterial({
                    map: texture,
                    transparent: true,
                    opacity: this.subtleMode ? 0.6 : 0.88,
                    depthWrite: false,
                    blending: THREE.AdditiveBlending
                });

                const sprite = new THREE.Sprite(spriteMat);
                sprite.position.set(item.x, item.y, item.z);
                sprite.scale.set(item.scale, item.scale, 1);
                this.scene.add(sprite);

                this.glyphSprites.push({
                    sprite: sprite,
                    baseY: item.y,
                    bobSpeed: 1.2 + i * 0.25,
                    bobOffset: i * 1.5
                });
            }
        }

        /**
         * Procedural 3D Neural Knowledge Network / Constellation
         */
        buildKnowledgeConstellation() {
            const particleCount = this.subtleMode ? 45 : 85;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const velocities = [];

            const rangeX = 40;
            const rangeY = 28;
            const rangeZ = 24;

            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = (Math.random() - 0.5) * rangeX;
                positions[i * 3 + 1] = (Math.random() - 0.5) * rangeY;
                positions[i * 3 + 2] = (Math.random() - 0.5) * rangeZ;

                velocities.push({
                    vx: (Math.random() - 0.5) * 0.015,
                    vy: (Math.random() - 0.5) * 0.015,
                    vz: (Math.random() - 0.5) * 0.015
                });
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

            // Glowing round point texture
            const canvas = document.createElement('canvas');
            canvas.width = 64;
            canvas.height = 64;
            const ctx = canvas.getContext('2d');
            const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 30);
            g.addColorStop(0, 'rgba(255, 255, 255, 1)');
            g.addColorStop(0.3, 'rgba(96, 165, 250, 0.9)');
            g.addColorStop(0.8, 'rgba(59, 130, 246, 0.3)');
            g.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, 64, 64);
            const pTexture = new THREE.CanvasTexture(canvas);

            const pMaterial = new THREE.PointsMaterial({
                size: 0.9,
                map: pTexture,
                transparent: true,
                opacity: this.subtleMode ? 0.5 : 0.8,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });

            this.particlePoints = new THREE.Points(geometry, pMaterial);
            this.scene.add(this.particlePoints);
            this.particleVelocities = velocities;
            this.particleRange = { x: rangeX, y: rangeY, z: rangeZ };

            // Dynamic neural network connecting lines
            const lineMaxConnections = particleCount * 2;
            const linePositions = new Float32Array(lineMaxConnections * 6);
            const lineGeometry = new THREE.BufferGeometry();
            lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));

            const lineMaterial = new THREE.LineBasicMaterial({
                color: this.currentPalette.accent,
                transparent: true,
                opacity: this.subtleMode ? 0.15 : 0.28,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });

            this.constellationLines = new THREE.LineSegments(lineGeometry, lineMaterial);
            this.scene.add(this.constellationLines);
        }

        updateConstellation() {
            if (!this.particlePoints) return;

            const posAttr = this.particlePoints.geometry.attributes.position;
            const positions = posAttr.array;
            const vels = this.particleVelocities;
            const n = vels.length;

            const rx = this.particleRange.x / 2;
            const ry = this.particleRange.y / 2;
            const rz = this.particleRange.z / 2;

            for (let i = 0; i < n; i++) {
                positions[i * 3] += vels[i].vx * this.speed;
                positions[i * 3 + 1] += vels[i].vy * this.speed;
                positions[i * 3 + 2] += vels[i].vz * this.speed;

                // Bounce at boundaries
                if (Math.abs(positions[i * 3]) > rx) vels[i].vx *= -1;
                if (Math.abs(positions[i * 3 + 1]) > ry) vels[i].vy *= -1;
                if (Math.abs(positions[i * 3 + 2]) > rz) vels[i].vz *= -1;
            }
            posAttr.needsUpdate = true;

            // Connect nearby points with neural synapse lines
            if (this.constellationLines) {
                const linePos = this.constellationLines.geometry.attributes.position.array;
                let lineIndex = 0;
                const maxDist = 7.5;
                const maxDistSq = maxDist * maxDist;

                for (let i = 0; i < n; i++) {
                    for (let j = i + 1; j < n; j++) {
                        const dx = positions[i * 3] - positions[j * 3];
                        const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
                        const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
                        const distSq = dx * dx + dy * dy + dz * dz;

                        if (distSq < maxDistSq && lineIndex < linePos.length - 6) {
                            linePos[lineIndex++] = positions[i * 3];
                            linePos[lineIndex++] = positions[i * 3 + 1];
                            linePos[lineIndex++] = positions[i * 3 + 2];

                            linePos[lineIndex++] = positions[j * 3];
                            linePos[lineIndex++] = positions[j * 3 + 1];
                            linePos[lineIndex++] = positions[j * 3 + 2];
                        }
                    }
                }

                // Clear remaining segment slots
                for (let k = lineIndex; k < linePos.length; k++) {
                    linePos[k] = 0;
                }
                this.constellationLines.geometry.attributes.position.needsUpdate = true;
            }
        }

        onMouseMove(event) {
            this.targetMouseX = (event.clientX - this.windowHalfX) * 0.012;
            this.targetMouseY = (event.clientY - this.windowHalfY) * 0.012;
        }

        onTouchMove(event) {
            if (event.touches.length > 0) {
                this.targetMouseX = (event.touches[0].clientX - this.windowHalfX) * 0.01;
                this.targetMouseY = (event.touches[0].clientY - this.windowHalfY) * 0.01;
            }
        }

        onWindowResize() {
            const width = this.container.clientWidth || window.innerWidth;
            const height = this.container.clientHeight || window.innerHeight;

            this.windowHalfX = width / 2;
            this.windowHalfY = height / 2;

            if (this.camera) {
                this.camera.aspect = width / height;
                this.camera.updateProjectionMatrix();
            }

            if (this.renderer) {
                this.renderer.setSize(width, height);
            }
        }

        animate() {
            this.animationFrameId = requestAnimationFrame(this.animate);

            const elapsedTime = this.clock.getElapsedTime() * this.speed;

            // 1. Mouse Parallax with smooth lerp
            this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
            this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;

            if (!this.interactiveOrbit) {
                this.camera.position.x = this.mouseX * 3.5;
                this.camera.position.y = -this.mouseY * 3.5;
                this.camera.lookAt(0, 0, 0);
            }

            // 2. Animate 3D Academic Objects (bobbing + spinning)
            for (let i = 0; i < this.floatingObjects.length; i++) {
                const item = this.floatingObjects[i];
                const bob = Math.sin(elapsedTime * item.bobSpeed + item.bobOffset) * 0.45;
                item.mesh.position.y = item.baseY + bob;

                item.mesh.rotation.x += item.rotSpeedX;
                item.mesh.rotation.y += item.rotSpeedY;
                item.mesh.rotation.z += item.rotSpeedZ;
            }

            // 3. Animate 3D Floating Glyphs
            for (let i = 0; i < this.glyphSprites.length; i++) {
                const g = this.glyphSprites[i];
                const bob = Math.sin(elapsedTime * g.bobSpeed + g.bobOffset) * 0.35;
                g.sprite.position.y = g.baseY + bob;
            }

            // 4. Animate Atomic Knowledge Rings
            if (this.atomicRings.length === 3) {
                this.atomicRings[0].rotation.x += 0.015 * this.speed;
                this.atomicRings[0].rotation.y += 0.012 * this.speed;

                this.atomicRings[1].rotation.y += 0.018 * this.speed;
                this.atomicRings[1].rotation.z += 0.01 * this.speed;

                this.atomicRings[2].rotation.z += 0.014 * this.speed;
                this.atomicRings[2].rotation.x += 0.02 * this.speed;

                const corePulse = 1.0 + Math.sin(elapsedTime * 3) * 0.12;
                this.atomicCore.scale.set(corePulse, corePulse, corePulse);
            }

            // 5. Update Constellation & Neural Lines
            this.updateConstellation();

            // 6. Gentle light pulse
            if (this.rimLight) {
                this.rimLight.intensity = 1.3 + Math.sin(elapsedTime * 2) * 0.35;
            }

            this.renderer.render(this.scene, this.camera);
        }

        setTheme(themeName) {
            if (!this.palettes[themeName]) return;
            this.theme = themeName;
            this.currentPalette = this.palettes[themeName];

            if (this.scene && this.scene.fog) {
                this.scene.fog.color.setHex(this.currentPalette.bgBottom);
            }
        }

        setSpeed(newSpeed) {
            this.speed = Math.max(0.1, Math.min(3.0, newSpeed));
        }

        toggleSubtle(isSubtle) {
            this.subtleMode = isSubtle;
        }

        destroy() {
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
            }
            window.removeEventListener('resize', this.onWindowResize);
            window.removeEventListener('mousemove', this.onMouseMove);
            window.removeEventListener('touchmove', this.onTouchMove);

            if (this.renderer && this.renderer.domElement && this.renderer.domElement.parentNode) {
                this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
                this.renderer.dispose();
            }
        }
    }

    // Export globally
    window.Education3DBackground = Education3DBackground;

})(window);
