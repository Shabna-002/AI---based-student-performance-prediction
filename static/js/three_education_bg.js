/**
 * EduPredict AI - 3D Education & AI Animation Background
 * 
 * Features:
 * - 🎓 3D Procedural Graduation Cap (Mortarboard) with cyber glowing edges & tassel
 * - 📖 3D Open Academic Books with translucent pages
 * - 📜 3D Diploma Scroll with ribbon band
 * - 🧠 3D AI Neural Data Nodes & dynamic pulsating connecting synapse lines
 * - 💎 3D Wireframe Polyhedra & geometric data structures
 * - ✨ 3D Floating Particle Cloud
 * - 🌊 Slow-motion fluid movement (calm, non-distracting for reading)
 * - 📱 Mobile detection with lightweight fallback image to ensure 60 FPS
 * - 🔋 Tab visibility auto-pause for zero battery drain when inactive
 */

(function () {
    'use strict';

    // 1. Mobile & Capability Detection
    const isMobile = window.innerWidth < 768 || 
                     (navigator.maxTouchPoints && navigator.maxTouchPoints > 2) ||
                     /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    const canvas = document.getElementById('education-3d-canvas');
    const fallbackEl = document.getElementById('education-mobile-fallback');

    function checkWebGLSupport() {
        try {
            const testCanvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
                (testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    // If mobile or WebGL is not supported, activate lightweight fallback
    if (isMobile || !checkWebGLSupport() || typeof THREE === 'undefined') {
        if (canvas) {
            canvas.style.display = 'none';
            canvas.classList.add('is-fallback-active');
        }
        if (fallbackEl) {
            fallbackEl.style.display = 'block';
        }
        // Initialize lightweight 2D canvas stars fallback on mobile if canvas exists
        initMobileFallback();
        return;
    }

    if (!canvas) return;

    // 2. Three.js Scene Setup
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x070a14, 0.016);

    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
    });

    const dpr = Math.min(window.devicePixelRatio || 1, 1.8);
    renderer.setPixelRatio(dpr);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;

    // 3. Lighting (Atmospheric Cosmic Glow)
    const ambientLight = new THREE.AmbientLight(0x1e1b4b, 1.4);
    scene.add(ambientLight);

    const cyanLight = new THREE.DirectionalLight(0x38bdf8, 1.6);
    cyanLight.position.set(-15, 12, 10);
    scene.add(cyanLight);

    const purpleLight = new THREE.DirectionalLight(0xa855f7, 1.5);
    purpleLight.position.set(15, -10, 8);
    scene.add(purpleLight);

    const centerPointLight = new THREE.PointLight(0x818cf8, 2.0, 35);
    centerPointLight.position.set(0, 0, 5);
    scene.add(centerPointLight);

    // Group for all floating objects
    const floatingElements = [];

    // Helper: Create Glowing Edge Wireframe
    function createGlowEdges(geometry, colorHex = 0x38bdf8, opacity = 0.6) {
        const edges = new THREE.EdgesGeometry(geometry);
        const lineMat = new THREE.LineBasicMaterial({
            color: colorHex,
            transparent: true,
            opacity: opacity,
            linewidth: 1
        });
        return new THREE.LineSegments(edges, lineMat);
    }

    // 4. Procedural 3D Element Builders
    // ==========================================
    // 4A. 3D GRADUATION MORTARBOARD CAP
    // ==========================================
    function createGraduationCap(primaryColor = 0x111827, edgeColor = 0x38bdf8) {
        const capGroup = new THREE.Group();

        // Diamond Flat Top Cap
        const topGeo = new THREE.BoxGeometry(2.5, 0.08, 2.5);
        const topMat = new THREE.MeshStandardMaterial({
            color: primaryColor,
            roughness: 0.4,
            metalness: 0.2,
            emissive: 0x1e1b4b,
            emissiveIntensity: 0.2
        });
        const topMesh = new THREE.Mesh(topGeo, topMat);
        topMesh.rotation.y = Math.PI / 4;
        capGroup.add(topMesh);
        capGroup.add(createGlowEdges(topGeo, edgeColor, 0.75));

        // Skull Cap Base
        const skullGeo = new THREE.CylinderGeometry(0.72, 0.85, 0.65, 24);
        const skullMesh = new THREE.Mesh(skullGeo, topMat);
        skullMesh.position.y = -0.36;
        capGroup.add(skullMesh);

        // Cap Button
        const buttonGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.08, 16);
        const buttonMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, metalness: 0.8, roughness: 0.2 });
        const buttonMesh = new THREE.Mesh(buttonGeo, buttonMat);
        buttonMesh.position.y = 0.08;
        capGroup.add(buttonMesh);

        // Tassel Cord & Fringe
        const cordCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(0, 0.08, 0),
            new THREE.Vector3(0.6, 0.06, 0.6),
            new THREE.Vector3(1.3, -0.2, 1.1),
            new THREE.Vector3(1.4, -0.9, 1.2)
        ]);
        const cordGeo = new THREE.TubeGeometry(cordCurve, 16, 0.025, 8, false);
        const cordMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, metalness: 0.6, roughness: 0.3 });
        const cordMesh = new THREE.Mesh(cordGeo, cordMat);
        capGroup.add(cordMesh);

        // Tassel Head Cone
        const tasselHeadGeo = new THREE.ConeGeometry(0.1, 0.35, 12);
        const tasselHead = new THREE.Mesh(tasselHeadGeo, cordMat);
        tasselHead.position.set(1.4, -0.95, 1.2);
        tasselHead.rotation.x = Math.PI;
        capGroup.add(tasselHead);

        return capGroup;
    }

    // ==========================================
    // 4B. 3D OPEN ACADEMIC BOOK
    // ==========================================
    function createOpenBook(coverColor = 0x1e1b4b, pageGlow = 0x38bdf8) {
        const bookGroup = new THREE.Group();

        // Left & Right Covers
        const coverMat = new THREE.MeshStandardMaterial({
            color: coverColor,
            roughness: 0.5,
            metalness: 0.3,
            emissive: 0x0f172a
        });

        const coverGeo = new THREE.BoxGeometry(1.6, 0.06, 2.2);

        const leftCover = new THREE.Mesh(coverGeo, coverMat);
        leftCover.position.set(-0.82, -0.06, 0);
        leftCover.rotation.z = -0.2;
        bookGroup.add(leftCover);
        bookGroup.add(createGlowEdges(coverGeo, pageGlow, 0.5));

        const rightCover = new THREE.Mesh(coverGeo, coverMat);
        rightCover.position.set(0.82, -0.06, 0);
        rightCover.rotation.z = 0.2;
        bookGroup.add(rightCover);

        // Book Pages Block (Curved open fan)
        const pageMat = new THREE.MeshStandardMaterial({
            color: 0xe0e7ff,
            roughness: 0.3,
            transparent: true,
            opacity: 0.85,
            emissive: 0x312e81,
            emissiveIntensity: 0.35
        });

        const pageGeo = new THREE.BoxGeometry(1.5, 0.14, 2.1);
        const leftPages = new THREE.Mesh(pageGeo, pageMat);
        leftPages.position.set(-0.78, 0.03, 0);
        leftPages.rotation.z = -0.15;
        bookGroup.add(leftPages);

        const rightPages = new THREE.Mesh(pageGeo, pageMat);
        rightPages.position.set(0.78, 0.03, 0);
        rightPages.rotation.z = 0.15;
        bookGroup.add(rightPages);

        // Center Spine
        const spineGeo = new THREE.CylinderGeometry(0.12, 0.12, 2.2, 12);
        const spineMesh = new THREE.Mesh(spineGeo, coverMat);
        spineMesh.rotation.x = Math.PI / 2;
        spineMesh.position.set(0, -0.1, 0);
        bookGroup.add(spineMesh);

        return bookGroup;
    }

    // ==========================================
    // 4C. 3D DIPLOMA SCROLL
    // ==========================================
    function createDiplomaScroll() {
        const scrollGroup = new THREE.Group();

        // Parchment Roll Cylinder
        const rollGeo = new THREE.CylinderGeometry(0.38, 0.38, 2.4, 24);
        const rollMat = new THREE.MeshStandardMaterial({
            color: 0xf8fafc,
            roughness: 0.6,
            metalness: 0.1,
            emissive: 0x6366f1,
            emissiveIntensity: 0.25
        });
        const rollMesh = new THREE.Mesh(rollGeo, rollMat);
        scrollGroup.add(rollMesh);
        scrollGroup.add(createGlowEdges(rollGeo, 0xa855f7, 0.6));

        // Ribbon Band
        const ribbonGeo = new THREE.CylinderGeometry(0.40, 0.40, 0.32, 24);
        const ribbonMat = new THREE.MeshStandardMaterial({
            color: 0xef4444,
            roughness: 0.3,
            metalness: 0.6,
            emissive: 0x991b1b,
            emissiveIntensity: 0.3
        });
        const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
        scrollGroup.add(ribbonMesh);

        return scrollGroup;
    }

    // ==========================================
    // 4D. 3D MATH & DATA POLYHEDRA
    // ==========================================
    function createTechPolyhedron(type = 'icosa') {
        const polyGroup = new THREE.Group();
        let geo;
        if (type === 'icosa') {
            geo = new THREE.IcosahedronGeometry(1.3, 0);
        } else {
            geo = new THREE.OctahedronGeometry(1.2, 0);
        }

        // Wireframe Outer Shell
        const wireMat = new THREE.MeshBasicMaterial({
            color: type === 'icosa' ? 0x38bdf8 : 0xc084fc,
            wireframe: true,
            transparent: true,
            opacity: 0.65
        });
        const wireMesh = new THREE.Mesh(geo, wireMat);
        polyGroup.add(wireMesh);

        // Glowing Inner Core
        const coreGeo = new THREE.SphereGeometry(0.45, 16, 16);
        const coreMat = new THREE.MeshBasicMaterial({
            color: type === 'icosa' ? 0x60a5fa : 0xa855f7,
            transparent: true,
            opacity: 0.8
        });
        const coreMesh = new THREE.Mesh(coreGeo, coreMat);
        polyGroup.add(coreMesh);

        return polyGroup;
    }

    // 5. Populate the 3D Scene with Floating Academic Elements
    // Cap 1 (Upper Left)
    const cap1 = createGraduationCap(0x0f172a, 0x38bdf8);
    cap1.position.set(-11, 6, -6);
    cap1.rotation.set(0.3, 0.4, -0.2);
    scene.add(cap1);
    floatingElements.push({
        mesh: cap1,
        baseY: 6,
        baseX: -11,
        floatSpeed: 0.8,
        rotSpeedX: 0.25,
        rotSpeedY: 0.4,
        phase: 0.2
    });

    // Cap 2 (Mid Right)
    const cap2 = createGraduationCap(0x1e1b4b, 0xc084fc);
    cap2.position.set(12, -4, -8);
    cap2.rotation.set(-0.25, -0.6, 0.15);
    scene.add(cap2);
    floatingElements.push({
        mesh: cap2,
        baseY: -4,
        baseX: 12,
        floatSpeed: 0.7,
        rotSpeedX: -0.3,
        rotSpeedY: -0.35,
        phase: 2.1
    });

    // Book 1 (Lower Left)
    const book1 = createOpenBook(0x1e1b4b, 0x38bdf8);
    book1.position.set(-13, -7, -10);
    book1.rotation.set(0.4, -0.5, 0.3);
    scene.add(book1);
    floatingElements.push({
        mesh: book1,
        baseY: -7,
        baseX: -13,
        floatSpeed: 0.65,
        rotSpeedX: 0.2,
        rotSpeedY: 0.3,
        phase: 3.5
    });

    // Book 2 (Upper Right)
    const book2 = createOpenBook(0x0f172a, 0xa855f7);
    book2.position.set(13, 7, -11);
    book2.rotation.set(-0.35, 0.4, -0.25);
    scene.add(book2);
    floatingElements.push({
        mesh: book2,
        baseY: 7,
        baseX: 13,
        floatSpeed: 0.75,
        rotSpeedX: -0.2,
        rotSpeedY: 0.25,
        phase: 1.4
    });

    // Diploma Scroll (Bottom Center / Left)
    const diploma = createDiplomaScroll();
    diploma.position.set(-4, -9, -7);
    diploma.rotation.set(0.6, 0.2, -0.8);
    scene.add(diploma);
    floatingElements.push({
        mesh: diploma,
        baseY: -9,
        baseX: -4,
        floatSpeed: 0.85,
        rotSpeedX: 0.35,
        rotSpeedY: -0.4,
        phase: 4.8
    });

    // Tech Polyhedra (Math & Geometry)
    const poly1 = createTechPolyhedron('icosa');
    poly1.position.set(7, -8, -6);
    scene.add(poly1);
    floatingElements.push({
        mesh: poly1,
        baseY: -8,
        baseX: 7,
        floatSpeed: 0.9,
        rotSpeedX: 0.4,
        rotSpeedY: 0.5,
        phase: 0.9
    });

    const poly2 = createTechPolyhedron('octa');
    poly2.position.set(-6, 8, -8);
    scene.add(poly2);
    floatingElements.push({
        mesh: poly2,
        baseY: 8,
        baseX: -6,
        floatSpeed: 0.8,
        rotSpeedX: -0.45,
        rotSpeedY: 0.35,
        phase: 2.7
    });

    // 6. 3D AI Neural Data Nodes & Connecting Synapse Lines
    // ==========================================
    const nodeCount = 28;
    const nodeSpheres = [];
    const nodePositions = [];
    const nodeVelocities = [];

    const sphereGeo = new THREE.SphereGeometry(0.24, 12, 12);
    const sphereMatCyan = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.75 });
    const sphereMatPurple = new THREE.MeshBasicMaterial({ color: 0xc084fc, transparent: true, opacity: 0.75 });

    for (let i = 0; i < nodeCount; i++) {
        const mat = (i % 2 === 0) ? sphereMatCyan : sphereMatPurple;
        const sphere = new THREE.Mesh(sphereGeo, mat);

        const x = (Math.random() - 0.5) * 36;
        const y = (Math.random() - 0.5) * 22;
        const z = (Math.random() - 0.5) * 16 - 4;

        sphere.position.set(x, y, z);
        scene.add(sphere);

        nodeSpheres.push(sphere);
        nodePositions.push(sphere.position);
        nodeVelocities.push(new THREE.Vector3(
            (Math.random() - 0.5) * 0.012,
            (Math.random() - 0.5) * 0.012,
            (Math.random() - 0.5) * 0.008
        ));
    }

    // Dynamic Synaptic Connecting Lines
    const maxLineConnections = 70;
    const linePositions = new Float32Array(maxLineConnections * 6);
    const lineColors = new Float32Array(maxLineConnections * 6);

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

    const lineMat = new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.45,
        blending: THREE.AdditiveBlending
    });

    const synapseLines = new THREE.LineSegments(lineGeo, lineMat);
    scene.add(synapseLines);

    // 7. 3D Floating Particle Cloud (Soft Starfield)
    // ==========================================
    function createSoftParticleTexture() {
        const pCanvas = document.createElement('canvas');
        pCanvas.width = 64;
        pCanvas.height = 64;
        const pCtx = pCanvas.getContext('2d');

        const grad = pCtx.createRadialGradient(32, 32, 0, 32, 32, 32);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.3, 'rgba(56, 189, 248, 0.7)');
        grad.addColorStop(0.7, 'rgba(168, 85, 247, 0.25)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');

        pCtx.fillStyle = grad;
        pCtx.fillRect(0, 0, 64, 64);

        const tex = new THREE.CanvasTexture(pCanvas);
        tex.needsUpdate = true;
        return tex;
    }

    const particleCount = 380;
    const particleGeo = new THREE.BufferGeometry();
    const particleCoords = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
        particleCoords[i] = (Math.random() - 0.5) * 60;
        particleCoords[i + 1] = (Math.random() - 0.5) * 45;
        particleCoords[i + 2] = (Math.random() - 0.5) * 35 - 5;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(particleCoords, 3));

    const particleMat = new THREE.PointsMaterial({
        size: 0.65,
        map: createSoftParticleTexture(),
        transparent: true,
        opacity: 0.6,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });

    const particleCloud = new THREE.Points(particleGeo, particleMat);
    scene.add(particleCloud);

    // 8. Subtle Mouse Parallax & Smooth Damping
    // ==========================================
    let mouseX = 0;
    let mouseY = 0;
    let targetCameraX = 0;
    let targetCameraY = 0;

    window.addEventListener('mousemove', function (e) {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;

        // Subtle camera deflection (gentle tilt, non-distracting)
        targetCameraX = mouseX * 1.8;
        targetCameraY = mouseY * 1.2;
    }, { passive: true });

    // Window Resize Handler
    window.addEventListener('resize', function () {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }, { passive: true });

    // 9. Visibility & Animation Loop (Zero Waste)
    // ==========================================
    let isTabActive = !document.hidden;
    let animFrameId = null;

    document.addEventListener('visibilitychange', function () {
        isTabActive = !document.hidden;
        if (isTabActive) {
            lastTime = performance.now();
            requestAnimationFrame(animate);
        } else if (animFrameId) {
            cancelAnimationFrame(animFrameId);
        }
    });

    let lastTime = performance.now();

    function animate(currentTime) {
        if (!isTabActive) return;
        animFrameId = requestAnimationFrame(animate);

        const delta = Math.min((currentTime - lastTime) * 0.001, 0.1);
        lastTime = currentTime;
        const time = currentTime * 0.001;

        // Camera gentle parallax lerp
        camera.position.x += (targetCameraX - camera.position.x) * 0.02;
        camera.position.y += (targetCameraY - camera.position.y) * 0.02;
        camera.lookAt(0, 0, 0);

        // Slow-motion floating & rotation of Academic 3D Elements
        for (let i = 0; i < floatingElements.length; i++) {
            const item = floatingElements[i];
            item.mesh.position.y = item.baseY + Math.sin(time * item.floatSpeed + item.phase) * 0.35;
            item.mesh.position.x = item.baseX + Math.cos(time * item.floatSpeed * 0.6 + item.phase) * 0.15;

            item.mesh.rotation.x += item.rotSpeedX * 0.0035;
            item.mesh.rotation.y += item.rotSpeedY * 0.0045;
        }

        // Particle cloud slow drift
        particleCloud.rotation.y = time * 0.015;
        particleCloud.rotation.x = Math.sin(time * 0.01) * 0.03;

        // Animate Neural Data Nodes
        for (let i = 0; i < nodeCount; i++) {
            const pos = nodePositions[i];
            const vel = nodeVelocities[i];

            pos.add(vel);

            // Soft boundary bounce
            if (pos.x < -18 || pos.x > 18) vel.x = -vel.x;
            if (pos.y < -12 || pos.y > 12) vel.y = -vel.y;
            if (pos.z < -14 || pos.z > 4) vel.z = -vel.z;

            nodeSpheres[i].position.copy(pos);
        }

        // Compute Connecting Synapse Lines
        let lineIdx = 0;
        const maxDist = 7.5;
        const positions = lineGeo.attributes.position.array;
        const colors = lineGeo.attributes.color.array;

        for (let i = 0; i < nodeCount && lineIdx < maxLineConnections; i++) {
            for (let j = i + 1; j < nodeCount && lineIdx < maxLineConnections; j++) {
                const dist = nodePositions[i].distanceTo(nodePositions[j]);
                if (dist < maxDist) {
                    const p1 = nodePositions[i];
                    const p2 = nodePositions[j];

                    const base = lineIdx * 6;
                    positions[base] = p1.x;
                    positions[base + 1] = p1.y;
                    positions[base + 2] = p1.z;

                    positions[base + 3] = p2.x;
                    positions[base + 4] = p2.y;
                    positions[base + 5] = p2.z;

                    // Gradient alpha based on distance
                    const alpha = 1.0 - (dist / maxDist);
                    colors[base] = 0.22 * alpha;
                    colors[base + 1] = 0.74 * alpha;
                    colors[base + 2] = 0.97 * alpha;

                    colors[base + 3] = 0.65 * alpha;
                    colors[base + 4] = 0.33 * alpha;
                    colors[base + 5] = 0.96 * alpha;

                    lineIdx++;
                }
            }
        }

        lineGeo.setDrawRange(0, lineIdx * 2);
        lineGeo.attributes.position.needsUpdate = true;
        lineGeo.attributes.color.needsUpdate = true;

        renderer.render(scene, camera);
    }

    // Start 3D rendering loop
    requestAnimationFrame(animate);

    // ==========================================
    // 10. LIGHTWEIGHT MOBILE FALLBACK ENGINE
    // ==========================================
    function initMobileFallback() {
        const fallbackContainer = document.getElementById('education-mobile-fallback');
        if (!fallbackContainer) return;

        // Populate fallback container with an optimized SVG vector constellation and gentle CSS drift
        fallbackContainer.innerHTML = `
            <svg class="mobile-education-constellation" viewBox="0 0 800 1200" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <radialGradient id="mGradCyan" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
                        <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
                    </radialGradient>
                    <radialGradient id="mGradPurple" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#a855f7" stop-opacity="0.85"/>
                        <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
                    </radialGradient>
                    <linearGradient id="mLineGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5"/>
                        <stop offset="100%" stop-color="#a855f7" stop-opacity="0.5"/>
                    </linearGradient>
                </defs>
                <!-- Glowing Ambient Halos -->
                <circle cx="200" cy="300" r="180" fill="url(#mGradCyan)" opacity="0.25"/>
                <circle cx="650" cy="750" r="220" fill="url(#mGradPurple)" opacity="0.25"/>
                <!-- Synaptic Constellation Lines -->
                <line x1="120" y1="220" x2="350" y2="180" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <line x1="350" y1="180" x2="520" y2="340" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <line x1="520" y1="340" x2="280" y2="520" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <line x1="280" y1="520" x2="120" y2="220" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <line x1="280" y1="520" x2="450" y2="720" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <line x1="450" y1="720" x2="680" y2="620" stroke="url(#mLineGrad)" stroke-width="1.2"/>
                <!-- Constellation Nodes -->
                <circle cx="120" cy="220" r="4" fill="#38bdf8"/>
                <circle cx="350" cy="180" r="5" fill="#818cf8"/>
                <circle cx="520" cy="340" r="4" fill="#c084fc"/>
                <circle cx="280" cy="520" r="6" fill="#38bdf8"/>
                <circle cx="450" cy="720" r="5" fill="#a855f7"/>
                <circle cx="680" cy="620" r="4" fill="#38bdf8"/>
                <!-- 🎓 Stylized 3D Graduation Cap Silhouette (Floating Accent) -->
                <g transform="translate(560, 220) scale(0.75)" opacity="0.35">
                    <polygon points="60,10 120,40 60,70 0,40" fill="none" stroke="#38bdf8" stroke-width="2"/>
                    <path d="M 25,52 L 25,85 Q 60,110 95,85 L 95,52" fill="none" stroke="#818cf8" stroke-width="2"/>
                    <path d="M 120,40 L 135,75 L 138,100" fill="none" stroke="#fbbf24" stroke-width="1.8"/>
                    <circle cx="138" cy="104" r="3" fill="#fbbf24"/>
                </g>
                <!-- 📖 Stylized 3D Open Book Silhouette -->
                <g transform="translate(80, 780) scale(0.7)" opacity="0.3">
                    <path d="M 0,20 Q 50,0 100,20 L 100,90 Q 50,70 0,90 Z" fill="none" stroke="#c084fc" stroke-width="2"/>
                    <path d="M 100,20 Q 150,0 200,20 L 200,90 Q 150,70 100,90 Z" fill="none" stroke="#a855f7" stroke-width="2"/>
                </g>
            </svg>
        `;
    }

})();
