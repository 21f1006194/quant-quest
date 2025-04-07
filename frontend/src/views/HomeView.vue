<template>
    <div class="container">
      <nav class="navbar">
        <div class="logo">QuantQuest</div>
        <div class="nav-links">
          <a href="#">Home</a>
          <a href="#">About</a>
          <a href="#">Login</a>
        </div>
        <div class="theme-toggle">
          <label><input type="checkbox" /> Dark Mode</label>
        </div>
      </nav>
  
      <main class="main-content">
        <h1 class="hero-text">"QUANT QUEST"</h1>
        <p class="sub-text">The Smartest Minds. The Biggest Quest.</p>
        <button class="cta-button">Explore Events</button>
      </main>
    </div>
  </template>
  
  <script setup>
  // You can later use Vue reactivity for theme toggling here if needed
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
  
  .container {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
    min-height: 100vh;
  }
  
  /* Navbar */
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: rgba(15, 23, 42, 0.95);
    border-bottom: 1px solid #334155;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .logo {
    font-size: 2.8rem;
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(90deg, #00bcd4, #1e88e5, #8e24aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeInLogo 1.2s ease-out;
    text-shadow: 0 2px 10px rgba(0, 188, 212, 0.4);
    transition: transform 0.3s ease;
  }
  
  .logo:hover {
    transform: scale(1.06);
    text-shadow: 0 6px 12px rgba(0, 188, 212, 0.6);
  }
  
  .nav-links a {
    margin-left: 1.2rem;
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
  }
  
  .nav-links a:hover {
    color: #38bdf8;
  }
  
  .theme-toggle label {
    color: #94a3b8;
    font-size: 0.9rem;
  }
  
  /* Hero Section */
  .main-content {
    position: relative;
    height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-align: center;
  }
  
  .main-content::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url('/quantix-logo.jpg'); /* Make sure this is in /public folder */
    background-size: cover;
    background-position: center;
    opacity: 0.15;
    z-index: -2;
  }
  
  .main-content::after {
    content: '';
    position: absolute;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.6);
    z-index: -1;
  }
  
  .hero-text {
    font-size: 3rem;
    font-weight: 800;
    color: #67e8f9;
    margin-bottom: 1rem;
    animation: fadeUp 1s ease-out;
  }
  
  .sub-text {
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
    animation: fadeUp 1.4s ease-out;
  }
  
  .cta-button {
    padding: 0.8rem 2rem;
    background-color: #06b6d4;
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    transition: background 0.3s ease, transform 0.2s ease;
    animation: fadeUp 1.8s ease-out;
  }
  
  .cta-button:hover {
    background-color: #0891b2;
    transform: scale(1.05);
  }
  
  /* Animations */
  @keyframes fadeInLogo {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes fadeUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>
  