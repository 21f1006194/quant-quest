<template>
  <div class="home-container">
    <div class="banner-section">
      <img src="@/assets/images/home_banner.png" alt="Quant Quest Banner" class="banner-image">
      <div class="inauguration-overlay">
        <div class="overlay-content minimal">
          <div class="thumb-container">
            <a href="https://www.youtube.com/live/zgA83sge67Y?si=7aLOAJn1eBTTktrT" target="_blank" class="yt-thumb-link">
              <img src="/YTthumb.jpg" alt="Watch on YouTube" class="yt-thumb-large">
            </a>
          </div>
          <a href="https://meet.google.com/zch-zodn-wfa" target="_blank" class="btn btn-primary join-btn">Join Meet</a>
        </div>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="header-section text-center">
        <h1 class="main-title">Quant Quest</h1>
        <p class="tagline">Welcome to Quant Quest, where mathematics meets excitement.</p>
      </div>

      <div class="intro-section card">
        <p class="description">
          <strong>Quant Quest</strong> is an exclusive gaming event crafted for brilliant minds who thrive on mathematical challenges. Whether you're a math enthusiast, a quantitative analyst, a programmer, or a strategic thinker, this is your platform to shine.
        </p>
        <p class="emphasis text-center">Victory here isn't about luck. It's about <strong>strategy, analysis, and precision</strong>.</p>
        <p class="description">
          Each game is meticulously designed around core mathematical concepts: probability theory, statistical analysis, and strategic decision-making. This is where your analytical skills and coding expertise will be your greatest assets.
        </p>
      </div>

      <div class="how-to-play-section card">
        <h2 class="text-center">How to Play</h2>
        <ol class="steps-list">
          <li><strong>Register</strong> on the IITM Paradox Website</li>
          <li><strong>Login</strong> to Quant Quest using your registered email</li>
          <li><strong>Explore</strong> the available games</li>
          <li><strong>Analyze</strong> each game's mechanics and identify statistical advantages</li>
          <li><strong>Download</strong> the Python template code, and your API token</li>
          <li><strong>Develop</strong> your winning strategy through code</li>
          <li><strong>Monitor</strong> your progress (wallet balance) and optimize your approach</li>
        </ol>
        <p class="final-note text-center">Success in Quant Quest demands <strong>strategic thinking, mathematical precision, and algorithmic mastery</strong>.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Component logic can be added here if needed
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
  min-height: 100vh;
  color: var(--text-light);
}

.banner-section {
  width: 100%;
  height: 40vh;
  margin-bottom: var(--spacing-lg);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  position: relative;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.inauguration-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
  pointer-events: none;
  box-sizing: border-box;
}

.overlay-content.minimal {
  background: rgba(10, 25, 47, 0.12);
  border-radius: 0;
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  box-shadow: none;
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 0;
  position: relative;
  box-sizing: border-box;
}

.thumb-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  box-sizing: border-box;
}

.yt-thumb-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: auto;
  text-align: center;
  margin: 0;
}

.yt-thumb-large {
  max-width: 60%;
  max-height: 80%;
  width: auto;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
  object-fit: contain;
  transition: transform 0.18s;
  cursor: pointer;
  background: #222;
  margin: 0 auto;
  display: block;
  z-index: 1;
}

.yt-thumb-link:hover .yt-thumb-large {
  transform: scale(1.04);
}

.join-btn {
  position: absolute;
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  font-size: 1.2rem;
  padding: 1rem 2.8rem;
  border-radius: 12px;
  font-weight: bold;
  background: var(--primary-color);
  color: #0a192f;
  box-shadow: 0 2px 8px rgba(100,255,218,0.10);
  text-decoration: none;
  transition: background 0.2s;
  display: inline-block;
  pointer-events: auto;
  z-index: 10;
}

.join-btn:hover {
  background: #4cd8b2;
}

.content-wrapper {
  padding: 0 var(--spacing-lg) var(--spacing-lg);
}

.header-section {
  margin-bottom: var(--spacing-xl);
}

.main-title {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
  color: var(--primary-color);
}

.tagline {
  font-size: 1.4rem;
  color: var(--secondary-color);
}

.intro-section {
  margin-bottom: var(--spacing-xl);
  background-color: var(--card-dark);
}

.description {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: var(--spacing-md);
  color: var(--text-light);
}

.emphasis {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  margin: var(--spacing-lg) 0;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.2);
}

.how-to-play-section {
  margin-bottom: var(--spacing-xl);
  background-color: var(--card-dark);
}

.how-to-play-section h2 {
  margin-bottom: var(--spacing-lg);
  font-size: 2rem;
  color: var(--primary-color);
}

.steps-list {
  list-style-type: decimal;
  padding-left: var(--spacing-lg);
  line-height: 2;
  color: var(--text-light);
}

.steps-list li {
  margin-bottom: var(--spacing-sm);
  font-size: 1.1rem;
}

.final-note {
  font-style: italic;
  margin-top: var(--spacing-lg);
  color: var(--secondary-color);
  font-size: 1.2rem;
}

@media (max-width: 900px) {
  .join-btn {
    font-size: 1rem;
    padding: 0.7rem 1.5rem;
  }
}
</style>

